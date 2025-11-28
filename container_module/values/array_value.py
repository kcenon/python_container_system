"""
Array value implementation

Equivalent to C++ array_value.h/cpp
"""

from typing import List, Optional, Iterator
from container_module.core.value import Value
from container_module.core.value_types import ValueTypes


class ArrayValue(Value):
    """
    Array/list value implementation.

    ArrayValue (type 15) is an extension to support homogeneous or heterogeneous
    collections of values, similar to JSON arrays. This enables cross-language
    compatibility with array structures in Node.js, Python, C++, etc.

    Wire format (binary):
    [type:1=15][name_len:4 LE][name:UTF-8][value_size:4 LE][count:4 LE][values...]

    Text format:
    [name,15,count];[element1][element2]...
    """

    def __init__(self, name: str, values: Optional[List[Value]] = None):
        """
        Initialize an ArrayValue.

        Args:
            name: The name/key of this array value
            values: List of values to store (optional)
        """
        super().__init__(name, ValueTypes.ARRAY_VALUE, b"")
        self._values: List[Value] = values.copy() if values else []

        # Update parent references
        for value in self._values:
            value.set_parent(self)

    @classmethod
    def from_data(cls, name: str, data: bytes) -> "ArrayValue":
        """
        Create ArrayValue from serialized bytes.

        Binary format for array data:
        [count:4 LE][element1_type:1][element1_name_len:4][element1_name][element1_data_len:4][element1_data]...

        Args:
            name: The name/key
            data: Serialized data containing count followed by serialized elements

        Returns:
            New ArrayValue instance
        """
        import struct
        from container_module.core.value_types import ValueTypes

        if len(data) < 4:
            return cls(name, [])

        offset = 0
        count = struct.unpack("<I", data[offset : offset + 4])[0]
        offset += 4

        values: List[Value] = []
        for _ in range(count):
            if offset >= len(data):
                break

            # Read element type
            if offset + 1 > len(data):
                break
            elem_type = ValueTypes(data[offset])
            offset += 1

            # Read element name length
            if offset + 4 > len(data):
                break
            elem_name_len = struct.unpack("<I", data[offset : offset + 4])[0]
            offset += 4

            # Read element name
            if offset + elem_name_len > len(data):
                break
            elem_name = data[offset : offset + elem_name_len].decode("utf-8")
            offset += elem_name_len

            # Read element data length
            if offset + 4 > len(data):
                break
            elem_data_len = struct.unpack("<I", data[offset : offset + 4])[0]
            offset += 4

            # Read element data
            if offset + elem_data_len > len(data):
                break
            elem_data = data[offset : offset + elem_data_len]
            offset += elem_data_len

            # Create element using factory
            value = cls._create_value_from_binary(elem_name, elem_type, elem_data)
            if value:
                values.append(value)

        return cls(name, values)

    @classmethod
    def from_string(cls, name: str, value_str: str) -> "ArrayValue":
        """
        Create ArrayValue from serialized string.

        Text format: The value_str contains the serialized elements after the header.
        Each element is in format [name,type,data]; or [name,type,count]; for complex types.

        Args:
            name: The name/key
            value_str: Serialized string containing element data

        Returns:
            New ArrayValue instance
        """
        import re
        from container_module.core.value_types import get_type_from_string

        if not value_str:
            return cls(name, [])

        values: List[Value] = []

        # Parse elements in format [name,type,data]; or [name,type,count];...
        # Use regex to find bracketed elements
        pattern = r"\[([^\]]+)\];"
        matches = re.findall(pattern, value_str)

        for match in matches:
            parts = match.split(",", 2)
            if len(parts) >= 3:
                elem_name = parts[0]
                elem_type = get_type_from_string(parts[1])
                elem_data = parts[2]

                value = cls._create_value_from_string(elem_name, elem_type, elem_data)
                if value:
                    values.append(value)

        return cls(name, values)

    @staticmethod
    def _create_value_from_binary(
        name: str, value_type: "ValueTypes", data: bytes
    ) -> Optional[Value]:
        """
        Factory method to create a Value from binary data.

        Args:
            name: The value name
            value_type: The ValueType enum
            data: Binary data for the value

        Returns:
            Created Value or None if type not supported
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
            ContainerValue,
        )

        try:
            if value_type == ValueTypes.BOOL_VALUE:
                return BoolValue.from_data(name, data)
            elif value_type == ValueTypes.SHORT_VALUE:
                return ShortValue.from_data(name, data)
            elif value_type == ValueTypes.USHORT_VALUE:
                return UShortValue.from_data(name, data)
            elif value_type == ValueTypes.INT_VALUE:
                return IntValue.from_data(name, data)
            elif value_type == ValueTypes.UINT_VALUE:
                return UIntValue.from_data(name, data)
            elif value_type == ValueTypes.LONG_VALUE:
                return LongValue.from_data(name, data)
            elif value_type == ValueTypes.ULONG_VALUE:
                return ULongValue.from_data(name, data)
            elif value_type == ValueTypes.LLONG_VALUE:
                return LLongValue.from_data(name, data)
            elif value_type == ValueTypes.ULLONG_VALUE:
                return ULLongValue.from_data(name, data)
            elif value_type == ValueTypes.FLOAT_VALUE:
                return FloatValue.from_data(name, data)
            elif value_type == ValueTypes.DOUBLE_VALUE:
                return DoubleValue.from_data(name, data)
            elif value_type == ValueTypes.STRING_VALUE:
                return StringValue.from_data(name, data)
            elif value_type == ValueTypes.BYTES_VALUE:
                return BytesValue.from_data(name, data)
            elif value_type == ValueTypes.CONTAINER_VALUE:
                return ContainerValue.from_data(name, data)
            elif value_type == ValueTypes.ARRAY_VALUE:
                return ArrayValue.from_data(name, data)
            else:
                return None
        except Exception:
            return None

    @staticmethod
    def _create_value_from_string(
        name: str, value_type: "ValueTypes", value_str: str
    ) -> Optional[Value]:
        """
        Factory method to create a Value from string data.

        Args:
            name: The value name
            value_type: The ValueType enum
            value_str: String data for the value

        Returns:
            Created Value or None if type not supported
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
            ContainerValue,
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
            elif value_type == ValueTypes.CONTAINER_VALUE:
                return ContainerValue.from_string(name, value_str)
            elif value_type == ValueTypes.ARRAY_VALUE:
                return ArrayValue.from_string(name, value_str)
            else:
                return None
        except Exception:
            return None

    def append(self, value: Value) -> None:
        """
        Add a value to the end of the array.

        Args:
            value: The value to add
        """
        self._values.append(value)
        value.set_parent(self)

    def push_back(self, value: Value) -> None:
        """
        Add a value to the end (C++ compatibility name).

        Args:
            value: The value to add
        """
        self.append(value)

    def at(self, index: int) -> Value:
        """
        Get value at index.

        Args:
            index: The index to retrieve

        Returns:
            The value at index

        Raises:
            IndexError: If index is out of range
        """
        if index < 0 or index >= len(self._values):
            raise IndexError(
                f"ArrayValue index {index} out of range (size: {len(self._values)})"
            )
        return self._values[index]

    @property
    def size(self) -> int:
        """
        Get the number of elements in the array.

        Returns:
            The size of the array
        """
        return len(self._values)

    def empty(self) -> bool:
        """
        Check if the array is empty.

        Returns:
            True if empty, False otherwise
        """
        return len(self._values) == 0

    def clear(self) -> None:
        """Clear all elements from the array."""
        self._values.clear()

    def values(self) -> List[Value]:
        """
        Get all values in the array.

        Returns:
            Copy of the internal list of values
        """
        return self._values.copy()

    def to_string(self, original: bool = True) -> str:
        """
        Convert to string representation.

        Args:
            original: Formatting flag

        Returns:
            String representation
        """
        return f"Array({len(self._values)} elements)"

    def serialize(self) -> str:
        """
        Serialize to text format: [name,type,count];[element1][element2]...

        Returns:
            Serialized format with element count and all elements appended
        """
        from container_module.core.value_types import get_string_from_type

        type_code = get_string_from_type(self._type)
        count = len(self._values)

        # Array header with count
        result = f"[{self._name},{type_code},{count}];"

        # Append all element serializations
        for value in self._values:
            result += value.serialize()

        return result

    def to_json(self) -> str:
        """Convert to JSON format."""
        import json

        data = {
            "name": self._name,
            "type": "array",
            "elements": [json.loads(value.to_json()) for value in self._values],
        }
        return json.dumps(data, ensure_ascii=False)

    def to_xml(self) -> str:
        """Convert to XML format."""
        import xml.etree.ElementTree as ET

        root = ET.Element("array")
        root.set("name", self._name)
        root.set("count", str(len(self._values)))

        for value in self._values:
            child_elem = ET.fromstring(value.to_xml())
            root.append(child_elem)

        return ET.tostring(root, encoding="unicode")

    # Python list-like interface
    def __len__(self) -> int:
        """Get number of elements."""
        return len(self._values)

    def __getitem__(self, index: int) -> Value:  # type: ignore[override]
        """Get element at index (supports Python indexing)."""
        return self._values[index]

    def __setitem__(self, index: int, value: Value) -> None:
        """Set element at index."""
        if index < 0 or index >= len(self._values):
            raise IndexError(
                f"ArrayValue index {index} out of range (size: {len(self._values)})"
            )
        value.set_parent(self)
        self._values[index] = value

    def __iter__(self) -> Iterator[Value]:
        """Iterate over elements."""
        return iter(self._values)

    def __contains__(self, value: Value) -> bool:
        """Check if value is in array."""
        return value in self._values

    def __repr__(self) -> str:
        """Detailed representation."""
        return f"ArrayValue(name={self._name!r}, size={len(self._values)})"
