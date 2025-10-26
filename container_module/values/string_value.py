"""
String value implementation

Equivalent to C++ string_value.h/cpp
"""

from container_module.core.value import Value
from container_module.core.value_types import ValueTypes


class StringValue(Value):
    """
    UTF-8 string value implementation.

    Equivalent to C++ string_value class.
    """

    def __init__(self, name: str, value: str):
        """
        Initialize a StringValue.

        Args:
            name: The name/key of this value
            value: The string value
        """
        data = value.encode("utf-8")
        super().__init__(name, ValueTypes.STRING_VALUE, data)
        self._value = value

    @classmethod
    def from_data(cls, name: str, data: bytes) -> "StringValue":
        """
        Create StringValue from raw bytes.

        Args:
            name: The name/key
            data: Raw UTF-8 encoded bytes

        Returns:
            New StringValue instance
        """
        value = data.decode("utf-8")
        return cls(name, value)

    @classmethod
    def from_string(cls, name: str, value_str: str) -> "StringValue":
        """
        Create StringValue from string.

        Args:
            name: The name/key
            value_str: String value

        Returns:
            New StringValue instance
        """
        return cls(name, value_str)

    def to_string(self, original: bool = True) -> str:
        """
        Get string value.

        Args:
            original: Ignored for string values

        Returns:
            The string value
        """
        return self._value

    def to_boolean(self) -> bool:
        """Convert to boolean (non-empty strings are True)."""
        return bool(self._value)

    def to_int(self) -> int:
        """Convert to integer if possible."""
        try:
            return int(self._value)
        except ValueError:
            return 0

    def to_float(self) -> float:
        """Convert to float if possible."""
        try:
            return float(self._value)
        except ValueError:
            return 0.0

    def serialize(self) -> str:
        """
        Serialize to C++ compatible format: [name,type,value];

        Returns:
            Serialized format: "[name,type,value];"
        """
        from container_module.core.value_types import get_string_from_type

        type_code = get_string_from_type(self._type)
        # Escape special characters that could break parsing
        escaped_value = self._value.replace("];", "\\];")
        return f"[{self._name},{type_code},{escaped_value}];"

    def __len__(self) -> int:
        """Get string length."""
        return len(self._value)

    def __str__(self) -> str:
        """String representation."""
        return self._value
