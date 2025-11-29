"""
Null value implementation

Equivalent to C++ null_value.h/cpp

This module provides the NullValue type which represents an absent or
undefined value. This is useful for optional fields or placeholder values.

Wire Protocol:
- Type code: 0
- Payload size: 0 bytes (no payload)
- JSON representation: null

C++ Compatibility:
This type corresponds to `null_value` in the C++ container system,
which uses `std::monostate` as the underlying type.
"""

from container_module.core.value import Value
from container_module.core.value_types import ValueTypes


class NullValue(Value):
    """
    Null value implementation.

    Represents the absence of a value. This type has no payload and is used
    to represent optional or missing data in a type-safe manner.

    Equivalent to C++ null_value class.

    Example:
        >>> null_val = NullValue("optional_field")
        >>> null_val.is_null()
        True
        >>> null_val.to_string()
        'null'
    """

    def __init__(self, name: str):
        """
        Initialize a NullValue.

        Args:
            name: The name/key of this value
        """
        # Null values have no data payload
        super().__init__(name, ValueTypes.NULL_VALUE, b"")

    @classmethod
    def from_data(cls, name: str, data: bytes) -> "NullValue":
        """
        Create NullValue from raw bytes.

        Args:
            name: The name/key
            data: Raw bytes (ignored for null values)

        Returns:
            New NullValue instance
        """
        return cls(name)

    @classmethod
    def from_string(cls, name: str, value_str: str) -> "NullValue":
        """
        Create NullValue from string.

        Args:
            name: The name/key
            value_str: String representation (ignored for null values)

        Returns:
            New NullValue instance
        """
        return cls(name)

    def is_null(self) -> bool:
        """
        Check if this value is null.

        Returns:
            Always True for NullValue
        """
        return True

    def to_string(self, original: bool = True) -> str:
        """
        Convert to string representation.

        Args:
            original: Ignored for null values

        Returns:
            Always returns "null"
        """
        return "null"

    def serialize(self) -> str:
        """
        Serialize to C++ compatible format: [name,type,value];

        Returns:
            Serialized format: "[name,0,null];"
        """
        from container_module.core.value_types import get_string_from_type

        type_code = get_string_from_type(self._type)
        return f"[{self._name},{type_code},null];"

    def to_json(self) -> dict:
        """
        Convert to JSON-compatible dictionary.

        Returns:
            Dictionary with name, type, and null value
        """
        return {"name": self._name, "type": "null", "value": None}

    def to_xml(self) -> str:
        """
        Convert to XML representation.

        Returns:
            XML string representation
        """
        return f'<value name="{self._name}" type="null"/>'

    def __repr__(self) -> str:
        """Return string representation for debugging."""
        return f"NullValue(name='{self._name}')"

    def __bool__(self) -> bool:
        """
        Python boolean conversion.

        Returns:
            Always False (null is falsy)
        """
        return False

    def __eq__(self, other: object) -> bool:
        """
        Compare equality.

        Args:
            other: Other object to compare

        Returns:
            True if other is also a NullValue with same name
        """
        if isinstance(other, NullValue):
            return self._name == other._name
        return False
