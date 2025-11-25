"""
BSD 3-Clause License

Copyright (c) 2025, kcenon
All rights reserved.

JSON v2.0 Adapter for cross-language compatibility

This adapter implements the unified JSON v2.0 format for data interchange
between C++, Python, and .NET container system implementations.

Unified JSON v2.0 Format:
{
  "container": {
    "version": "2.0",
    "metadata": {
      "message_type": "user_profile",
      "protocol_version": "1.0.0.0",
      "source": {
        "id": "client",
        "sub_id": "session"
      },
      "target": {
        "id": "server",
        "sub_id": "handler"
      }
    },
    "values": [
      {
        "name": "username",
        "type": 12,
        "type_name": "string",
        "data": "john_doe"
      }
    ]
  }
}
"""

from __future__ import annotations
from typing import Any, Dict, List, Optional, Union
import json
import base64

from container_module.core.container import ValueContainer
from container_module.core.value import Value
from container_module.core.value_types import (
    ValueTypes,
    get_string_from_type,
    get_type_from_string,
)
from container_module.values import (
    BoolValue,
    ShortValue,
    UShortValue,
    IntValue,
    UIntValue,
    LongValue,
    ULongValue,
    LLongValue,
    ULLongValue,
    FloatValue,
    DoubleValue,
    StringValue,
    BytesValue,
    ContainerValue,
)


class JsonV2Adapter:
    """
    Adapter for unified JSON v2.0 format compatible across C++, Python, and .NET.

    This adapter provides methods to:
    - Convert ValueContainer to unified JSON v2.0 format
    - Parse JSON v2.0 format into ValueContainer
    - Convert between different JSON formats (C++ nested, Python/NET flat, v2.0 unified)
    - Handle backward compatibility with legacy formats
    """

    # JSON format version constants
    V2_FORMAT_VERSION = "2.0"
    V1_FORMAT_VERSION = "1.0"

    # Type name mapping for human-readable type names
    TYPE_NAME_MAP: Dict[ValueTypes, str] = {
        ValueTypes.NULL_VALUE: "null",
        ValueTypes.BOOL_VALUE: "bool",
        ValueTypes.SHORT_VALUE: "short",
        ValueTypes.USHORT_VALUE: "ushort",
        ValueTypes.INT_VALUE: "int",
        ValueTypes.UINT_VALUE: "uint",
        ValueTypes.LONG_VALUE: "long",
        ValueTypes.ULONG_VALUE: "ulong",
        ValueTypes.LLONG_VALUE: "llong",
        ValueTypes.ULLONG_VALUE: "ullong",
        ValueTypes.FLOAT_VALUE: "float",
        ValueTypes.DOUBLE_VALUE: "double",
        ValueTypes.BYTES_VALUE: "bytes",
        ValueTypes.STRING_VALUE: "string",
        ValueTypes.CONTAINER_VALUE: "container",
    }

    REVERSE_TYPE_NAME_MAP: Dict[str, ValueTypes] = {
        v: k for k, v in TYPE_NAME_MAP.items()
    }

    @classmethod
    def to_v2_json(cls, container: ValueContainer, pretty: bool = False) -> str:
        """
        Convert ValueContainer to unified JSON v2.0 format.

        Args:
            container: ValueContainer to convert
            pretty: If True, format with indentation for readability

        Returns:
            JSON string in v2.0 unified format

        Example:
            >>> container = ValueContainer(message_type="test")
            >>> container.add(IntValue("count", 42))
            >>> json_str = JsonV2Adapter.to_v2_json(container, pretty=True)
        """
        v2_data: Dict[str, Any] = {
            "container": {
                "version": cls.V2_FORMAT_VERSION,
                "metadata": {
                    "message_type": container.message_type,
                    "protocol_version": container.version,
                    "source": {
                        "id": container.source_id,
                        "sub_id": container.source_sub_id,
                    },
                    "target": {
                        "id": container.target_id,
                        "sub_id": container.target_sub_id,
                    },
                },
                "values": [],
            }
        }

        # Convert all values
        for value in container.units:
            v2_value = cls._value_to_v2_dict(value)
            v2_data["container"]["values"].append(v2_value)

        if pretty:
            return json.dumps(v2_data, indent=2, ensure_ascii=False)
        else:
            return json.dumps(v2_data, separators=(",", ":"), ensure_ascii=False)

    @classmethod
    def from_v2_json(cls, json_str: str) -> ValueContainer:
        """
        Parse JSON v2.0 format into ValueContainer.

        Args:
            json_str: JSON string in v2.0 unified format

        Returns:
            ValueContainer object populated with parsed data

        Raises:
            ValueError: If JSON format is invalid or incompatible

        Example:
            >>> json_str = '{"container": {"version": "2.0", ...}}'
            >>> container = JsonV2Adapter.from_v2_json(json_str)
        """
        try:
            data = json.loads(json_str)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON: {e}")

        if "container" not in data:
            raise ValueError("Missing 'container' root element in JSON v2.0")

        container_data = data["container"]

        # Check version
        version = container_data.get("version", "1.0")
        if version != cls.V2_FORMAT_VERSION:
            raise ValueError(
                f"Unsupported JSON version: {version} (expected {cls.V2_FORMAT_VERSION})"
            )

        # Parse metadata
        metadata = container_data.get("metadata", {})
        source = metadata.get("source", {})
        target = metadata.get("target", {})

        # Create container
        container = ValueContainer(
            source_id=source.get("id", ""),
            source_sub_id=source.get("sub_id", ""),
            target_id=target.get("id", ""),
            target_sub_id=target.get("sub_id", ""),
            message_type=metadata.get("message_type", ""),
        )

        # Set protocol version
        protocol_version = metadata.get("protocol_version", "1.0.0.0")
        container._version = protocol_version

        # Parse values
        values_data = container_data.get("values", [])
        for value_data in values_data:
            value = cls._v2_dict_to_value(value_data)
            if value:
                container.add(value)

        return container

    @classmethod
    def _value_to_v2_dict(cls, value: Value) -> Dict[str, Any]:
        """
        Convert a Value object to v2.0 dictionary representation.

        Args:
            value: Value object to convert

        Returns:
            Dictionary with name, type, type_name, and data fields
        """
        value_dict: Dict[str, Any] = {
            "name": value.name,
            "type": value.type.value,  # Numeric type ID
            "type_name": cls.TYPE_NAME_MAP.get(value.type, "unknown"),
        }

        # Handle different value types
        if value.is_null():
            value_dict["data"] = None

        elif value.type == ValueTypes.BOOL_VALUE:
            value_dict["data"] = value.to_boolean()

        elif value.type in {
            ValueTypes.SHORT_VALUE,
            ValueTypes.USHORT_VALUE,
            ValueTypes.INT_VALUE,
            ValueTypes.UINT_VALUE,
        }:
            value_dict["data"] = value.to_int()

        elif value.type in {
            ValueTypes.LONG_VALUE,
            ValueTypes.ULONG_VALUE,
            ValueTypes.LLONG_VALUE,
            ValueTypes.ULLONG_VALUE,
        }:
            value_dict["data"] = value.to_long()

        elif value.type in {ValueTypes.FLOAT_VALUE, ValueTypes.DOUBLE_VALUE}:
            value_dict["data"] = value.to_double()

        elif value.type == ValueTypes.STRING_VALUE:
            value_dict["data"] = str(value)

        elif value.type == ValueTypes.BYTES_VALUE:
            # Base64 encode binary data
            bytes_data = value.to_bytes()
            value_dict["data"] = base64.b64encode(bytes_data).decode("ascii")
            value_dict["encoding"] = "base64"

        elif value.type == ValueTypes.CONTAINER_VALUE:
            # Nested container
            if isinstance(value, ContainerValue):
                nested_values = []
                for child in value.children():
                    nested_values.append(cls._value_to_v2_dict(child))
                value_dict["data"] = nested_values
                value_dict["child_count"] = value.child_count()
            else:
                value_dict["data"] = []
                value_dict["child_count"] = 0

        else:
            # Fallback: convert to string
            value_dict["data"] = str(value)

        return value_dict

    @classmethod
    def _v2_dict_to_value(cls, value_data: Dict[str, Any]) -> Optional[Value]:
        """
        Convert v2.0 dictionary representation to Value object.

        Args:
            value_data: Dictionary with name, type, type_name, and data fields

        Returns:
            Value object, or None if conversion fails
        """
        name = value_data.get("name", "")
        type_id = value_data.get("type", 0)
        data = value_data.get("data")

        # Convert type ID to ValueTypes
        try:
            value_type = ValueTypes(type_id)
        except ValueError:
            # Try type_name if type ID is invalid
            type_name = value_data.get("type_name", "")
            value_type = cls.REVERSE_TYPE_NAME_MAP.get(type_name, ValueTypes.NULL_VALUE)

        # Create appropriate Value subclass
        try:
            if value_type == ValueTypes.NULL_VALUE:
                # NULL_VALUE represented as empty StringValue
                return StringValue(name, "")

            elif value_type == ValueTypes.BOOL_VALUE:
                return BoolValue(name, bool(data) if data is not None else False)

            elif value_type == ValueTypes.SHORT_VALUE:
                return ShortValue(name, int(data) if data is not None else 0)

            elif value_type == ValueTypes.USHORT_VALUE:
                return UShortValue(name, int(data) if data is not None else 0)

            elif value_type == ValueTypes.INT_VALUE:
                return IntValue(name, int(data) if data is not None else 0)

            elif value_type == ValueTypes.UINT_VALUE:
                return UIntValue(name, int(data) if data is not None else 0)

            elif value_type == ValueTypes.LONG_VALUE:
                return LongValue(name, int(data) if data is not None else 0)

            elif value_type == ValueTypes.ULONG_VALUE:
                return ULongValue(name, int(data) if data is not None else 0)

            elif value_type == ValueTypes.LLONG_VALUE:
                return LLongValue(name, int(data) if data is not None else 0)

            elif value_type == ValueTypes.ULLONG_VALUE:
                return ULLongValue(name, int(data) if data is not None else 0)

            elif value_type == ValueTypes.FLOAT_VALUE:
                return FloatValue(name, float(data) if data is not None else 0.0)

            elif value_type == ValueTypes.DOUBLE_VALUE:
                return DoubleValue(name, float(data) if data is not None else 0.0)

            elif value_type == ValueTypes.STRING_VALUE:
                return StringValue(name, str(data) if data is not None else "")

            elif value_type == ValueTypes.BYTES_VALUE:
                # Decode base64
                if data is None:
                    return BytesValue(name, b"")
                encoding = value_data.get("encoding", "base64")
                if encoding == "base64":
                    bytes_data = base64.b64decode(str(data))
                else:
                    bytes_data = bytes(str(data), "utf-8")
                return BytesValue(name, bytes_data)

            elif value_type == ValueTypes.CONTAINER_VALUE:
                # Nested container
                container_value = ContainerValue(name)
                if isinstance(data, list):
                    for child_data in data:
                        child = cls._v2_dict_to_value(child_data)
                        if child:
                            container_value.add(child)
                return container_value

            else:
                print(f"Warning: Unknown value type {value_type}")
                return None

        except Exception as e:
            print(f"Error converting value '{name}': {e}")
            return None

    @classmethod
    def from_cpp_json(cls, json_str: str) -> ValueContainer:
        """
        Convert C++ nested JSON format to ValueContainer.

        C++ JSON format has "header" object and "values" object (not array).

        Args:
            json_str: JSON string in C++ format

        Returns:
            ValueContainer object

        Example:
            >>> cpp_json = '{"header": {...}, "values": {"key": {...}}}'
            >>> container = JsonV2Adapter.from_cpp_json(cpp_json)
        """
        try:
            data = json.loads(json_str)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON: {e}")

        # Parse header
        header = data.get("header", {})
        container = ValueContainer(
            source_id=header.get("source_id", ""),
            source_sub_id=header.get("source_sub_id", ""),
            target_id=header.get("target_id", ""),
            target_sub_id=header.get("target_sub_id", ""),
            message_type=header.get("message_type", ""),
        )
        container._version = header.get("version", "1.0.0.0")

        # Parse values (object format)
        values_obj = data.get("values", {})
        for value_name, value_data in values_obj.items():
            value = cls._cpp_value_to_value(value_name, value_data)
            if value:
                container.add(value)

        return container

    @classmethod
    def _cpp_value_to_value(
        cls, name: str, value_data: Dict[str, Any]
    ) -> Optional[Value]:
        """
        Convert C++ JSON value format to Value object.

        Args:
            name: Value name
            value_data: Dictionary with "type" and "data" fields

        Returns:
            Value object or None
        """
        type_id = value_data.get("type", 0)
        data_str = value_data.get("data", "")

        try:
            value_type = ValueTypes(type_id)
        except ValueError:
            value_type = ValueTypes.NULL_VALUE

        # Create value based on type (similar to _v2_dict_to_value but with string data)
        try:
            if value_type == ValueTypes.BOOL_VALUE:
                bool_val = data_str.lower() in ("true", "1", "yes")
                return BoolValue(name, bool_val)

            elif value_type in {
                ValueTypes.SHORT_VALUE,
                ValueTypes.USHORT_VALUE,
                ValueTypes.INT_VALUE,
                ValueTypes.UINT_VALUE,
            }:
                return IntValue(name, int(data_str))

            elif value_type in {
                ValueTypes.LONG_VALUE,
                ValueTypes.ULONG_VALUE,
                ValueTypes.LLONG_VALUE,
                ValueTypes.ULLONG_VALUE,
            }:
                return LongValue(name, int(data_str))

            elif value_type in {ValueTypes.FLOAT_VALUE, ValueTypes.DOUBLE_VALUE}:
                return DoubleValue(name, float(data_str))

            elif value_type == ValueTypes.STRING_VALUE:
                return StringValue(name, data_str)

            elif value_type == ValueTypes.BYTES_VALUE:
                bytes_data = base64.b64decode(data_str)
                return BytesValue(name, bytes_data)

            else:
                return None

        except Exception as e:
            print(f"Error parsing C++ value '{name}': {e}")
            return None

    @classmethod
    def to_cpp_json(cls, container: ValueContainer, pretty: bool = False) -> str:
        """
        Convert ValueContainer to C++ nested JSON format.

        Args:
            container: ValueContainer to convert
            pretty: If True, format with indentation

        Returns:
            JSON string in C++ format
        """
        cpp_data: Dict[str, Any] = {
            "header": {
                "target_id": container.target_id,
                "target_sub_id": container.target_sub_id,
                "source_id": container.source_id,
                "source_sub_id": container.source_sub_id,
                "message_type": container.message_type,
                "version": container.version,
            },
            "values": {},
        }

        # Convert values to object format
        for value in container.units:
            value_name = value.name
            cpp_data["values"][value_name] = {
                "type": value.type.value,
                "data": cls._value_to_string_data(value),
            }

        if pretty:
            return json.dumps(cpp_data, indent=2)
        else:
            return json.dumps(cpp_data, separators=(",", ":"))

    @classmethod
    def _value_to_string_data(cls, value: Value) -> str:
        """
        Convert Value to string representation for C++ JSON format.

        Args:
            value: Value to convert

        Returns:
            String representation of data
        """
        if value.is_null():
            return ""
        elif value.type == ValueTypes.BOOL_VALUE:
            return "true" if value.to_boolean() else "false"
        elif value.type == ValueTypes.BYTES_VALUE:
            return base64.b64encode(value.to_bytes()).decode("ascii")
        else:
            return str(value)

    @classmethod
    def detect_format(cls, json_str: str) -> str:
        """
        Detect JSON format version.

        Args:
            json_str: JSON string to analyze

        Returns:
            Format identifier: "v2.0", "cpp", "python", or "unknown"
        """
        try:
            data = json.loads(json_str)

            # Check for v2.0 format
            if "container" in data:
                container_data = data["container"]
                version = container_data.get("version", "")
                if version == "2.0":
                    return "v2.0"

            # Check for C++ format (has "header" object)
            if "header" in data and isinstance(data.get("values"), dict):
                return "cpp"

            # Check for Python/.NET format (flat structure with values array)
            if "message_type" in data and isinstance(data.get("values"), list):
                return "python"

            return "unknown"

        except json.JSONDecodeError:
            return "invalid"

    @classmethod
    def convert_format(
        cls, json_str: str, target_format: str, pretty: bool = False
    ) -> str:
        """
        Convert between different JSON formats.

        Args:
            json_str: Input JSON string
            target_format: Target format ("v2.0", "cpp", or "python")
            pretty: If True, format output with indentation

        Returns:
            JSON string in target format

        Raises:
            ValueError: If source or target format is unsupported

        Example:
            >>> cpp_json = '{"header": {...}, "values": {...}}'
            >>> v2_json = JsonV2Adapter.convert_format(cpp_json, "v2.0", pretty=True)
        """
        # Detect source format
        source_format = cls.detect_format(json_str)

        # Parse to container based on source format
        if source_format == "v2.0":
            container = cls.from_v2_json(json_str)
        elif source_format == "cpp":
            container = cls.from_cpp_json(json_str)
        elif source_format == "python":
            container = ValueContainer(data_string=json_str)
        else:
            raise ValueError(f"Unsupported source format: {source_format}")

        # Convert to target format
        if target_format == "v2.0":
            return cls.to_v2_json(container, pretty)
        elif target_format == "cpp":
            return cls.to_cpp_json(container, pretty)
        elif target_format == "python":
            # Use container's built-in to_json()
            return (
                container.to_json()
                if not pretty
                else json.dumps(json.loads(container.to_json()), indent=2)
            )
        else:
            raise ValueError(f"Unsupported target format: {target_format}")
