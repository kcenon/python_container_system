"""
Array value implementation

Equivalent to C++ array_value.h/cpp
"""

from typing import List, Optional, Any
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

        Args:
            name: The name/key
            data: Serialized data

        Returns:
            New ArrayValue instance

        Note:
            This requires full binary deserialization support.
            Currently returns empty array as placeholder.
        """
        # TODO: Implement full binary deserialization
        return cls(name, [])

    @classmethod
    def from_string(cls, name: str, value_str: str) -> "ArrayValue":
        """
        Create ArrayValue from serialized string.

        Args:
            name: The name/key
            value_str: Serialized string

        Returns:
            New ArrayValue instance

        Note:
            This requires full text deserialization support.
            Currently returns empty array as placeholder.
        """
        # TODO: Implement full text deserialization
        return cls(name, [])

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
            raise IndexError(f"ArrayValue index {index} out of range (size: {len(self._values)})")
        return self._values[index]

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

    def __getitem__(self, index: int) -> Value:
        """Get element at index (supports Python indexing)."""
        return self._values[index]

    def __setitem__(self, index: int, value: Value) -> None:
        """Set element at index."""
        if index < 0 or index >= len(self._values):
            raise IndexError(f"ArrayValue index {index} out of range (size: {len(self._values)})")
        value.set_parent(self)
        self._values[index] = value

    def __iter__(self):
        """Iterate over elements."""
        return iter(self._values)

    def __contains__(self, value: Value) -> bool:
        """Check if value is in array."""
        return value in self._values

    def __repr__(self) -> str:
        """Detailed representation."""
        return f"ArrayValue(name={self._name!r}, size={len(self._values)})"
