"""
ValueContainer class for container system

This module provides the main container class for managing messages
with source/target information and value storage.

Equivalent to C++ core/container.h
"""

from __future__ import annotations
from typing import List, Optional, Tuple, Dict, Any, Union
import json
import xml.etree.ElementTree as ET
from threading import RLock
from pathlib import Path

from container_module.core.value import Value
from container_module.core.value_types import ValueTypes, get_string_from_type


# Header field IDs matching C++ container_module constants
# These ensure cross-language compatibility with C++/.NET container systems
TARGET_ID = 1
TARGET_SUB_ID = 2
SOURCE_ID = 3
SOURCE_SUB_ID = 4
MESSAGE_TYPE = 5
MESSAGE_VERSION = 6


class ValueContainer:
    """
    A high-level container for messages with source/target IDs,
    message type, and a list of values.

    Equivalent to C++ value_container class.

    Attributes:
        source_id: Source identifier
        source_sub_id: Source sub-identifier
        target_id: Target identifier
        target_sub_id: Target sub-identifier
        message_type: Type of message
        version: Protocol version (default: "1.0.0.0")
        units: List of child values
    """

    DEFAULT_VERSION = "1.0.0.0"
    DEFAULT_MESSAGE_TYPE = "data_container"

    def __init__(
        self,
        source_id: str = "",
        source_sub_id: str = "",
        target_id: str = "",
        target_sub_id: str = "",
        message_type: str = "",
        units: Optional[List[Value]] = None,
        data_string: Optional[str] = None,
        data_array: Optional[bytes] = None,
        parse_only_header: bool = True,
    ):
        """
        Initialize a ValueContainer.

        Args:
            source_id: Source identifier
            source_sub_id: Source sub-identifier
            target_id: Target identifier
            target_sub_id: Target sub-identifier
            message_type: Type of message
            units: Initial list of values
            data_string: Serialized data to deserialize from
            data_array: Serialized byte array to deserialize from
            parse_only_header: If True, only parse header when deserializing
        """
        # Header fields
        self._source_id: str = source_id
        self._source_sub_id: str = source_sub_id
        self._target_id: str = target_id
        self._target_sub_id: str = target_sub_id
        self._message_type: str = message_type or self.DEFAULT_MESSAGE_TYPE
        self._version: str = self.DEFAULT_VERSION

        # Value storage
        self._units: List[Value] = units.copy() if units else []

        # Serialization state
        self._parsed_data: bool = True
        self._changed_data: bool = False
        self._data_string: str = ""

        # Thread safety
        self._lock = RLock()
        self._thread_safe_enabled: bool = False

        # Statistics
        self._read_count: int = 0
        self._write_count: int = 0
        self._serialization_count: int = 0

        # Deserialize if data provided
        if data_string is not None:
            self.deserialize(data_string, parse_only_header)
        elif data_array is not None:
            self.deserialize_array(data_array, parse_only_header)

    # Property accessors
    @property
    def source_id(self) -> str:
        """Get source ID."""
        return self._source_id

    @property
    def source_sub_id(self) -> str:
        """Get source sub-ID."""
        return self._source_sub_id

    @property
    def target_id(self) -> str:
        """Get target ID."""
        return self._target_id

    @property
    def target_sub_id(self) -> str:
        """Get target sub-ID."""
        return self._target_sub_id

    @property
    def message_type(self) -> str:
        """Get message type."""
        return self._message_type

    @property
    def version(self) -> str:
        """Get protocol version."""
        return self._version

    @property
    def units(self) -> List[Value]:
        """Get list of values."""
        return self._units.copy()

    # Setters
    def set_source(self, source_id: str, source_sub_id: str = "") -> None:
        """
        Set source identifiers.

        Args:
            source_id: Source identifier
            source_sub_id: Source sub-identifier
        """
        with self._get_write_lock():
            self._source_id = source_id
            self._source_sub_id = source_sub_id
            self._changed_data = True

    def set_target(self, target_id: str, target_sub_id: str = "") -> None:
        """
        Set target identifiers.

        Args:
            target_id: Target identifier
            target_sub_id: Target sub-identifier
        """
        with self._get_write_lock():
            self._target_id = target_id
            self._target_sub_id = target_sub_id
            self._changed_data = True

    def set_message_type(self, message_type: str) -> None:
        """
        Set message type.

        Args:
            message_type: Type of message
        """
        with self._get_write_lock():
            self._message_type = message_type
            self._changed_data = True

    def swap_header(self) -> None:
        """
        Swap source and target identifiers.

        Equivalent to C++ swap_header().
        """
        with self._get_write_lock():
            self._source_id, self._target_id = self._target_id, self._source_id
            self._source_sub_id, self._target_sub_id = (
                self._target_sub_id,
                self._source_sub_id,
            )
            self._changed_data = True

    # Value management
    def add(self, target_value: Value, update_immediately: bool = False) -> Value:
        """
        Add a value to this container.

        Args:
            target_value: Value to add
            update_immediately: Whether to update serialization immediately

        Returns:
            The added value
        """
        with self._get_write_lock():
            self._units.append(target_value)
            target_value.set_parent(self)
            self._changed_data = True
            if update_immediately:
                self._update_data_string()
            return target_value

    def set_units(
        self, target_values: List[Value], update_immediately: bool = False
    ) -> None:
        """
        Set or merge multiple values.

        Args:
            target_values: List of values to set/merge
            update_immediately: Whether to update serialization immediately
        """
        with self._get_write_lock():
            self._units.clear()
            for value in target_values:
                self._units.append(value)
                value.set_parent(self)
            self._changed_data = True
            if update_immediately:
                self._update_data_string()

    def remove(
        self, target: Union[str, Value], update_immediately: bool = False
    ) -> None:
        """
        Remove a value by name or reference.

        Args:
            target: Either a name string or a Value object
            update_immediately: Whether to update serialization immediately
        """
        with self._get_write_lock():
            if isinstance(target, str):
                # Remove by name
                self._units = [v for v in self._units if v.name != target]
            else:
                # Remove by reference
                self._units = [v for v in self._units if v is not target]
            self._changed_data = True
            if update_immediately:
                self._update_data_string()

    def clear_value(self) -> None:
        """Clear all stored values."""
        with self._get_write_lock():
            self._units.clear()
            self._changed_data = True

    def value_array(self, target_name: str) -> List[Value]:
        """
        Get all values with the given name.

        Args:
            target_name: Name to search for

        Returns:
            List of matching values
        """
        with self._get_read_lock():
            return [v for v in self._units if v.name == target_name]

    def get_value(self, target_name: str, index: int = 0) -> Optional[Value]:
        """
        Get the first (or indexed) value with the given name.

        Args:
            target_name: Name to search for
            index: Index of value to return if multiple matches

        Returns:
            Matching value or None
        """
        with self._get_read_lock():
            matches = self.value_array(target_name)
            return matches[index] if index < len(matches) else None

    # Serialization
    def serialize(self) -> str:
        """
        Serialize this container to C++ compatible format.

        Format: @header={{[id,value];...}}@data={{[name,type,value];...}};

        Header field IDs (matching C++):
        - 1: TARGET_ID
        - 2: TARGET_SUB_ID
        - 3: SOURCE_ID
        - 4: SOURCE_SUB_ID
        - 5: MESSAGE_TYPE
        - 6: MESSAGE_VERSION

        Returns:
            Serialized string representation
        """
        with self._get_read_lock():
            self._serialization_count += 1
            if not self._changed_data and self._data_string:
                return self._data_string

            # Build header section using numeric IDs for C++ compatibility
            # Always include all header fields for cross-language compatibility
            header_items = [
                f"[{TARGET_ID},{self._target_id}];",
                f"[{TARGET_SUB_ID},{self._target_sub_id}];",
                f"[{SOURCE_ID},{self._source_id}];",
                f"[{SOURCE_SUB_ID},{self._source_sub_id}];",
                f"[{MESSAGE_TYPE},{self._message_type}];",
                f"[{MESSAGE_VERSION},{self._version}];",
            ]

            header = "@header={{" + "".join(header_items) + "}}"

            # Build data section
            data_items = "".join(unit.serialize() for unit in self._units)
            data = "@data={{" + data_items + "}};"

            # Combine
            result = header + data
            self._data_string = result
            self._changed_data = False
            return result

    def serialize_array(self) -> bytes:
        """
        Serialize to a raw byte array.

        Returns:
            Serialized byte array
        """
        return self.serialize().encode("utf-8")

    def deserialize(self, data_string: str, parse_only_header: bool = True) -> bool:
        """
        Deserialize from C++ compatible format.

        Format: @header={{[id,value];...}}@data={{[name,type,value];...}};

        Supports both:
        - Numeric IDs (C++ format): [1,value], [2,value], etc.
        - String keys (legacy Python format): [target_id,value], [source_id,value], etc.

        Args:
            data_string: Serialized data
            parse_only_header: If True, only parse header

        Returns:
            True if successful, False otherwise
        """
        try:
            import re

            with self._get_write_lock():
                self._data_string = data_string

                # Parse @header section
                header_pattern = r"@header=\s*\{\{(.*?)\}\}"
                header_match = re.search(header_pattern, data_string)
                if not header_match:
                    return False

                header_content = header_match.group(1)

                # Parse header items: [key,value];
                item_pattern = r"\[([^,]+),\s*([^\]]*)\];"
                header_fields = {}
                for match in re.finditer(item_pattern, header_content):
                    key, value = match.groups()
                    header_fields[key] = value

                # Support both numeric IDs (C++ format) and string keys (legacy format)
                # Numeric ID mapping: 1=target_id, 2=target_sub_id, 3=source_id,
                #                     4=source_sub_id, 5=message_type, 6=version
                self._target_id = header_fields.get(
                    str(TARGET_ID), header_fields.get("target_id", "")
                )
                self._target_sub_id = header_fields.get(
                    str(TARGET_SUB_ID), header_fields.get("target_sub_id", "")
                )
                self._source_id = header_fields.get(
                    str(SOURCE_ID), header_fields.get("source_id", "")
                )
                self._source_sub_id = header_fields.get(
                    str(SOURCE_SUB_ID), header_fields.get("source_sub_id", "")
                )
                self._message_type = header_fields.get(
                    str(MESSAGE_TYPE),
                    header_fields.get("message_type", self.DEFAULT_MESSAGE_TYPE),
                )
                self._version = header_fields.get(
                    str(MESSAGE_VERSION),
                    header_fields.get("version", self.DEFAULT_VERSION),
                )

                # Parse @data section if requested
                if not parse_only_header:
                    data_pattern = r"@data=\s*\{\{?(.*?)\}\}?;"
                    data_match = re.search(data_pattern, data_string)
                    if data_match:
                        data_content = data_match.group(1)
                        self._deserialize_values(data_content)
                        self._parsed_data = True
                    else:
                        self._parsed_data = True
                else:
                    self._parsed_data = False

                self._changed_data = False
                return True

        except Exception as e:
            print(f"Deserialization error: {e}")
            import traceback

            traceback.print_exc()
            return False

    def deserialize_array(
        self, data_array: bytes, parse_only_header: bool = True
    ) -> bool:
        """
        Deserialize from a byte array.

        Args:
            data_array: Serialized byte data
            parse_only_header: If True, only parse header

        Returns:
            True if successful, False otherwise
        """
        try:
            data_string = data_array.decode("utf-8")
            return self.deserialize(data_string, parse_only_header)
        except Exception as e:
            print(f"Deserialization error: {e}")
            return False

    def _deserialize_values(self, data_part: str) -> None:
        """
        Internal method to deserialize values from data part.

        Parses format with nested container support:
        [name,type,value]; for simple values
        [name,CONTAINER,child_count];[child1...];[child2...]; for containers

        Args:
            data_part: The data portion of serialized string
        """
        import re
        from container_module.core.value_types import get_type_from_string, ValueTypes
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

        # Clear existing values
        self._units.clear()

        if not data_part or not data_part.strip():
            return

        # Replace escaped ]; with placeholder to avoid regex issues
        ESCAPED_DELIMITER = "__ESCAPED_SEMICOLON_BRACKET__"
        safe_data = data_part.replace("\\];", ESCAPED_DELIMITER)

        # Parse all items into a list first
        item_pattern = r"\[([^,]+),\s*([^,]+),\s*(.*?)\];"
        matches = [
            (m.group(1), m.group(2), m.group(3).replace(ESCAPED_DELIMITER, "];"))
            for m in re.finditer(item_pattern, safe_data)
        ]

        # Process matches recursively
        index_ref = [0]  # Use list for mutable reference

        while index_ref[0] < len(matches):
            name, type_str, value_str = matches[index_ref[0]]

            try:
                value_type = get_type_from_string(type_str)
                value = self._parse_value_recursive(
                    matches, index_ref, name, value_type, value_str
                )

                if value:
                    self._units.append(value)
                    value.set_parent(self)

            except Exception as e:
                print(f"Error deserializing value {name}: {e}")

            index_ref[0] += 1

    def _parse_value_recursive(
        self,
        matches: List[tuple],
        index_ref: List[int],
        name: str,
        value_type: ValueTypes,
        value_str: str,
    ) -> Optional[Value]:
        """
        Recursively parse a value, handling nested containers.

        Args:
            matches: List of (name, type_str, value_str) tuples
            index_ref: Mutable reference to current index
            name: Value name
            value_type: Value type
            value_str: Value string

        Returns:
            Parsed Value object or None
        """
        from container_module.core.value_types import ValueTypes, get_type_from_string
        from container_module.values import ContainerValue

        if value_type == ValueTypes.CONTAINER_VALUE:
            # Parse child count
            try:
                child_count = int(value_str) if value_str.strip() else 0
            except ValueError:
                child_count = 0

            # Recursively parse children
            children = []
            for _ in range(child_count):
                index_ref[0] += 1
                if index_ref[0] < len(matches):
                    child_name, child_type_str, child_value_str = matches[index_ref[0]]
                    child_type = get_type_from_string(child_type_str)

                    # Recursively parse child (may be another container)
                    child_val = self._parse_value_recursive(
                        matches, index_ref, child_name, child_type, child_value_str
                    )
                    if child_val:
                        children.append(child_val)

            return ContainerValue(name, children)

        else:
            # Create simple value
            return self._create_value(name, value_type, value_str)

    def _create_value(
        self, name: str, value_type: ValueTypes, value_str: str
    ) -> Optional[Value]:
        """
        Helper method to create a value from type and string.

        Args:
            name: Value name
            value_type: Value type enum
            value_str: String representation of value

        Returns:
            Created Value object or None
        """
        from container_module.core.value_types import ValueTypes
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
        )

        try:
            if value_type == ValueTypes.BOOL_VALUE:
                return BoolValue.from_string(name, value_str)
            elif value_type == ValueTypes.SHORT_VALUE:
                return ShortValue.from_string(name, value_str)
            elif value_type == ValueTypes.USHORT_VALUE:
                return UShortValue.from_string(name, value_str)
            elif value_type == ValueTypes.INT_VALUE:
                return IntValue.from_string(name, value_str)
            elif value_type == ValueTypes.UINT_VALUE:
                return UIntValue.from_string(name, value_str)
            elif value_type == ValueTypes.LONG_VALUE:
                return LongValue.from_string(name, value_str)
            elif value_type == ValueTypes.ULONG_VALUE:
                return ULongValue.from_string(name, value_str)
            elif value_type == ValueTypes.LLONG_VALUE:
                return LLongValue.from_string(name, value_str)
            elif value_type == ValueTypes.ULLONG_VALUE:
                return ULLongValue.from_string(name, value_str)
            elif value_type == ValueTypes.FLOAT_VALUE:
                return FloatValue.from_string(name, value_str)
            elif value_type == ValueTypes.DOUBLE_VALUE:
                return DoubleValue.from_string(name, value_str)
            elif value_type == ValueTypes.STRING_VALUE:
                return StringValue.from_string(name, value_str)
            elif value_type == ValueTypes.BYTES_VALUE:
                return BytesValue.from_string(name, value_str)
            else:
                return None
        except Exception as e:
            print(f"Error creating value {name}: {e}")
            return None

    # JSON/XML conversion
    def to_json(self) -> str:
        """
        Convert to JSON format.

        Returns:
            JSON string representation
        """
        with self._get_read_lock():
            data = {
                "source_id": self._source_id,
                "source_sub_id": self._source_sub_id,
                "target_id": self._target_id,
                "target_sub_id": self._target_sub_id,
                "message_type": self._message_type,
                "version": self._version,
                "values": [json.loads(unit.to_json()) for unit in self._units],
            }
            return json.dumps(data, ensure_ascii=False, indent=2)

    def to_xml(self) -> str:
        """
        Convert to XML format.

        Returns:
            XML string representation
        """
        with self._get_read_lock():
            root = ET.Element("container")
            root.set("message_type", self._message_type)
            root.set("version", self._version)

            # Source
            source = ET.SubElement(root, "source")
            source.set("id", self._source_id)
            source.set("sub_id", self._source_sub_id)

            # Target
            target = ET.SubElement(root, "target")
            target.set("id", self._target_id)
            target.set("sub_id", self._target_sub_id)

            # Values
            values = ET.SubElement(root, "values")
            for unit in self._units:
                # Parse the value's XML and append
                value_elem = ET.fromstring(unit.to_xml())
                values.append(value_elem)

            return ET.tostring(root, encoding="unicode")

    # File I/O
    def load_packet(self, file_path: str) -> None:
        """
        Load from a file.

        Args:
            file_path: Path to file to load
        """
        path = Path(file_path)
        data = path.read_bytes()
        self.deserialize_array(data)

    def save_packet(self, file_path: str) -> None:
        """
        Save to a file.

        Args:
            file_path: Path to file to save
        """
        path = Path(file_path)
        data = self.serialize_array()
        path.write_bytes(data)

    # Utility methods
    def copy(self, containing_values: bool = True) -> ValueContainer:
        """
        Create a copy of this container.

        Args:
            containing_values: If False, only copy header

        Returns:
            New ValueContainer instance
        """
        with self._get_read_lock():
            new_container = ValueContainer(
                source_id=self._source_id,
                source_sub_id=self._source_sub_id,
                target_id=self._target_id,
                target_sub_id=self._target_sub_id,
                message_type=self._message_type,
            )
            new_container._version = self._version

            if containing_values:
                new_container._units = self._units.copy()

            return new_container

    def initialize(self) -> None:
        """Reinitialize container to defaults."""
        with self._get_write_lock():
            self._source_id = ""
            self._source_sub_id = ""
            self._target_id = ""
            self._target_sub_id = ""
            self._message_type = self.DEFAULT_MESSAGE_TYPE
            self._version = self.DEFAULT_VERSION
            self._units.clear()
            self._parsed_data = True
            self._changed_data = False
            self._data_string = ""

    # Thread safety
    def enable_thread_safety(self, enabled: bool = True) -> None:
        """
        Enable or disable thread-safe operations.

        Args:
            enabled: True to enable thread safety
        """
        self._thread_safe_enabled = enabled

    def _get_read_lock(self) -> Any:
        """Get a read lock context manager."""
        if self._thread_safe_enabled:
            self._read_count += 1
            return self._lock
        return _DummyLock()

    def _get_write_lock(self) -> Any:
        """Get a write lock context manager."""
        if self._thread_safe_enabled:
            self._write_count += 1
            return self._lock
        return _DummyLock()

    def _update_data_string(self) -> None:
        """Internal method to update cached serialization."""
        self._data_string = self.serialize()
        self._changed_data = False

    # Operator overloads
    def __getitem__(self, key: str) -> List[Value]:
        """Get all values with the given name."""
        return self.value_array(key)

    def __str__(self) -> str:
        """String representation of this container."""
        return f"ValueContainer({self._message_type}, values={len(self._units)})"

    def __repr__(self) -> str:
        """Detailed representation of this container."""
        return (
            f"ValueContainer("
            f"source={self._source_id}/{self._source_sub_id}, "
            f"target={self._target_id}/{self._target_sub_id}, "
            f"type={self._message_type}, "
            f"values={len(self._units)})"
        )


class _DummyLock:
    """Dummy lock that does nothing (for when thread safety is disabled)."""

    def __enter__(self) -> "_DummyLock":
        return self

    def __exit__(self, *args: Any) -> None:
        pass
