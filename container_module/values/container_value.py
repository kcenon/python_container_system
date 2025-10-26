"""
Container value implementation

Equivalent to C++ container_value.h/cpp
"""

from typing import List, Optional
from container_module.core.value import Value
from container_module.core.value_types import ValueTypes


class ContainerValue(Value):
    """
    Nested container value implementation.

    Equivalent to C++ container_value class.
    Allows hierarchical data structures.
    """

    def __init__(self, name: str, units: Optional[List[Value]] = None):
        """
        Initialize a ContainerValue.

        Args:
            name: The name/key of this value
            units: List of child values
        """
        super().__init__(name, ValueTypes.CONTAINER_VALUE, b"")
        self._units = units.copy() if units else []
        # Update parent references
        for unit in self._units:
            unit.set_parent(self)

    @classmethod
    def from_data(cls, name: str, data: bytes) -> "ContainerValue":
        """
        Create ContainerValue from serialized bytes.

        Args:
            name: The name/key
            data: Serialized data

        Returns:
            New ContainerValue instance
        """
        # This would need proper deserialization logic
        # For now, create empty container
        return cls(name, [])

    @classmethod
    def from_string(cls, name: str, value_str: str) -> "ContainerValue":
        """
        Create ContainerValue from serialized string.

        Args:
            name: The name/key
            value_str: Serialized string

        Returns:
            New ContainerValue instance
        """
        # This would need proper deserialization logic
        # For now, create empty container
        return cls(name, [])

    def add(self, item: Value, update_count: bool = True) -> Value:
        """
        Add a child value.

        Args:
            item: Value to add
            update_count: Whether to update count (compatibility parameter)

        Returns:
            The added value
        """
        self._units.append(item)
        item.set_parent(self)
        return item

    def remove(self, name: str, update_count: bool = True) -> None:
        """
        Remove a child value by name.

        Args:
            name: Name of value to remove
            update_count: Whether to update count (compatibility parameter)
        """
        self._units = [v for v in self._units if v.name != name]

    def remove_all(self) -> None:
        """Remove all child values."""
        self._units.clear()

    def child_count(self) -> int:
        """Get number of child values."""
        return len(self._units)

    def children(self, only_container: bool = False) -> List[Value]:
        """
        Get child values.

        Args:
            only_container: If True, return only container-type children

        Returns:
            List of child values
        """
        if only_container:
            return [
                unit
                for unit in self._units
                if unit.type == ValueTypes.CONTAINER_VALUE
            ]
        return self._units.copy()

    def value_array(self, key: str) -> List[Value]:
        """
        Get all child values with the given name.

        Args:
            key: Name to search for

        Returns:
            List of matching values
        """
        return [unit for unit in self._units if unit.name == key]

    def get_value(self, name: str, index: int = 0) -> Optional[Value]:
        """
        Get child value by name.

        Args:
            name: Name to search for
            index: Index if multiple matches

        Returns:
            Matching value or None
        """
        matches = self.value_array(name)
        return matches[index] if index < len(matches) else None

    def to_string(self, original: bool = True) -> str:
        """
        Convert to string representation.

        Args:
            original: Formatting flag

        Returns:
            String representation
        """
        return f"Container({len(self._units)} values)"

    def serialize(self) -> str:
        """
        Serialize to C++ compatible format: [name,type,value];

        Returns:
            Serialized format with all child values appended
        """
        from container_module.core.value_types import get_string_from_type

        type_code = get_string_from_type(self._type)

        # Container header with empty value field
        result = f"[{self._name},{type_code},];"

        # Append all child serializations (recursive)
        for unit in self._units:
            result += unit.serialize()

        return result

    def to_json(self) -> str:
        """Convert to JSON format."""
        import json

        data = {
            "name": self._name,
            "type": "container",
            "children": [json.loads(unit.to_json()) for unit in self._units],
        }
        return json.dumps(data, ensure_ascii=False)

    def to_xml(self) -> str:
        """Convert to XML format."""
        import xml.etree.ElementTree as ET

        root = ET.Element("container")
        root.set("name", self._name)

        for unit in self._units:
            child_elem = ET.fromstring(unit.to_xml())
            root.append(child_elem)

        return ET.tostring(root, encoding="unicode")

    def __len__(self) -> int:
        """Get number of children."""
        return len(self._units)

    def __getitem__(self, key: str) -> Optional[Value]:
        """Get first child with given name."""
        return self.get_value(key)

    def __iter__(self):
        """Iterate over child values."""
        return iter(self._units)
