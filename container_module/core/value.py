"""
Base Value class for container system

This module provides the abstract base class for all values stored
in the container system.

Equivalent to C++ core/value.h
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Optional, List, Any, Union, TypeVar
import json
import xml.etree.ElementTree as ET

from container_module.core.value_types import ValueTypes, get_string_from_type

T = TypeVar("T")


class Value(ABC):
    """
    The base class for all values stored in the container system.

    Equivalent to C++ value class. This is an abstract base class that
    defines the interface for all value types.

    Attributes:
        _name: The name/key of this value
        _type: The ValueTypes enum indicating the type
        _data: The raw data as bytes
        _size: Size of the data in bytes
        _parent: Weak reference to parent value (for nested containers)
        _units: List of child values (for container values)
    """

    def __init__(
        self,
        name: str = "",
        value_type: ValueTypes = ValueTypes.NULL_VALUE,
        data: Union[bytes, str] = b"",
    ):
        """
        Initialize a Value.

        Args:
            name: The name/key of this value
            value_type: The type of this value
            data: The data as bytes or string
        """
        self._name: str = name
        self._type: ValueTypes = value_type
        self._data: bytes = data if isinstance(data, bytes) else data.encode("utf-8")
        self._size: int = len(self._data)
        self._parent: Optional[Value] = None
        self._units: List[Value] = []

    @property
    def name(self) -> str:
        """Get the name of this value."""
        return self._name

    @property
    def type(self) -> ValueTypes:
        """Get the type of this value."""
        return self._type

    @property
    def data(self) -> bytes:
        """Get the raw data as bytes."""
        return self._data

    @property
    def size(self) -> int:
        """Get the size of the data in bytes."""
        return self._size

    @property
    def parent(self) -> Optional[Value]:
        """Get the parent value."""
        return self._parent

    @property
    def units(self) -> List[Value]:
        """Get the list of child values."""
        return self._units

    def set_parent(self, parent: Optional[Any]) -> None:
        """
        Set the parent value.

        Args:
            parent: The parent value (Value or ValueContainer)
        """
        self._parent = parent

    def set_data(
        self,
        name: str,
        value_type: ValueTypes,
        data: Union[bytes, str],
    ) -> None:
        """
        Set the data with type information.

        Args:
            name: The name of this value
            value_type: The type of this value
            data: The data as bytes or string
        """
        self._name = name
        self._type = value_type
        self._data = data if isinstance(data, bytes) else data.encode("utf-8")
        self._size = len(self._data)

    def child_count(self) -> int:
        """
        Get the number of child values.

        Returns:
            Number of child values
        """
        return len(self._units)

    def children(self, only_container: bool = False) -> List[Value]:
        """
        Get child values, optionally filtered to only containers.

        Args:
            only_container: If True, return only container-type children

        Returns:
            List of child values
        """
        if only_container:
            return [
                unit for unit in self._units if unit.type == ValueTypes.CONTAINER_VALUE
            ]
        return self._units.copy()

    def value_array(self, key: str) -> List[Value]:
        """
        Get all child values with the given name.

        Args:
            key: The name to search for

        Returns:
            List of matching child values
        """
        return [unit for unit in self._units if unit.name == key]

    def to_bytes(self) -> bytes:
        """
        Convert this value to bytes.

        Returns:
            Byte representation of this value
        """
        return self._data

    # Type checking methods
    def is_null(self) -> bool:
        """Check if this is a null value."""
        return self._type == ValueTypes.NULL_VALUE

    def is_bytes(self) -> bool:
        """Check if this is a bytes value."""
        return self._type == ValueTypes.BYTES_VALUE

    def is_boolean(self) -> bool:
        """Check if this is a boolean value."""
        return self._type == ValueTypes.BOOL_VALUE

    def is_numeric(self) -> bool:
        """Check if this is a numeric value."""
        from container_module.core.value_types import is_numeric_type

        return is_numeric_type(self._type)

    def is_string(self) -> bool:
        """Check if this is a string value."""
        return self._type == ValueTypes.STRING_VALUE

    def is_container(self) -> bool:
        """Check if this is a container value."""
        return self._type == ValueTypes.CONTAINER_VALUE

    # Serialization methods
    @abstractmethod
    def serialize(self) -> str:
        """
        Serialize this value to a string.

        Returns:
            Serialized string representation
        """
        pass

    def to_json(self) -> str:
        """
        Convert this value to JSON format.

        Returns:
            JSON string representation
        """
        data_dict = {
            "name": self._name,
            "type": get_string_from_type(self._type),
            "data": self.to_string(),
        }
        return json.dumps(data_dict, ensure_ascii=False)

    def to_xml(self) -> str:
        """
        Convert this value to XML format.

        Returns:
            XML string representation
        """
        root = ET.Element("value")
        root.set("name", self._name)
        root.set("type", get_string_from_type(self._type))
        root.text = self.to_string()
        return ET.tostring(root, encoding="unicode")

    # Type conversion methods with safe_convert pattern
    def _safe_convert(self, type_name: str, default_value: T) -> T:
        """
        Template method for safe type conversion with null checking.

        Args:
            type_name: Human-readable name of target type
            default_value: Default value to return

        Returns:
            Converted value or default_value

        Raises:
            ValueError: If trying to convert from null_value
        """
        if self._type == ValueTypes.NULL_VALUE:
            raise ValueError(f"Cannot convert null_value to {type_name}")
        return default_value

    def to_boolean(self) -> bool:
        """Convert to boolean. Override in subclasses."""
        return self._safe_convert("boolean", False)

    def to_short(self) -> int:
        """Convert to short integer. Override in subclasses."""
        return self._safe_convert("short", 0)

    def to_ushort(self) -> int:
        """Convert to unsigned short integer. Override in subclasses."""
        return self._safe_convert("ushort", 0)

    def to_int(self) -> int:
        """Convert to integer. Override in subclasses."""
        return self._safe_convert("int", 0)

    def to_uint(self) -> int:
        """Convert to unsigned integer. Override in subclasses."""
        return self._safe_convert("uint", 0)

    def to_long(self) -> int:
        """Convert to long integer. Override in subclasses."""
        return self._safe_convert("long", 0)

    def to_ulong(self) -> int:
        """Convert to unsigned long integer. Override in subclasses."""
        return self._safe_convert("ulong", 0)

    def to_llong(self) -> int:
        """Convert to long long integer. Override in subclasses."""
        return self._safe_convert("llong", 0)

    def to_ullong(self) -> int:
        """Convert to unsigned long long integer. Override in subclasses."""
        return self._safe_convert("ullong", 0)

    def to_float(self) -> float:
        """Convert to float. Override in subclasses."""
        return self._safe_convert("float", 0.0)

    def to_double(self) -> float:
        """Convert to double. Override in subclasses."""
        return self._safe_convert("double", 0.0)

    def to_string(self, original: bool = True) -> str:
        """
        Convert to string representation.

        Args:
            original: If True, return original format; otherwise human-readable

        Returns:
            String representation
        """
        if self._type == ValueTypes.NULL_VALUE:
            return ""
        return self._data.decode("utf-8", errors="replace")

    # Child manipulation methods (throw exceptions by default, override in container)
    def add(self, item: Value, update_count: bool = True) -> Value:
        """
        Add a child value. Only valid for container values.

        Args:
            item: Value to add
            update_count: Whether to update count immediately

        Returns:
            The added value

        Raises:
            NotImplementedError: This is not a container value
        """
        raise NotImplementedError("Cannot add to this base value")

    def remove(self, name: str, update_count: bool = True) -> None:
        """
        Remove a child value by name. Only valid for container values.

        Args:
            name: Name of the value to remove
            update_count: Whether to update count immediately

        Raises:
            NotImplementedError: This is not a container value
        """
        raise NotImplementedError("Cannot remove from this base value")

    def remove_all(self) -> None:
        """
        Remove all child values. Only valid for container values.

        Raises:
            NotImplementedError: This is not a container value
        """
        raise NotImplementedError("Cannot remove all from this base value")

    # Operator overloads
    def __getitem__(self, key: str) -> Optional[Value]:
        """
        Get the first child value with the given name.

        Args:
            key: The name to search for

        Returns:
            First matching value or None
        """
        values = self.value_array(key)
        return values[0] if values else None

    def __str__(self) -> str:
        """String representation of this value."""
        return f"{self._name}={self.to_string()}"

    def __repr__(self) -> str:
        """Detailed representation of this value."""
        return f"Value(name={self._name!r}, type={self._type}, size={self._size})"
