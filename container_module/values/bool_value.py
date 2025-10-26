"""
Boolean value implementation

Equivalent to C++ bool_value.h/cpp
"""

import struct
from container_module.core.value import Value
from container_module.core.value_types import ValueTypes


class BoolValue(Value):
    """
    Boolean value implementation.

    Equivalent to C++ bool_value class.
    """

    def __init__(self, name: str, value: bool):
        """
        Initialize a BoolValue.

        Args:
            name: The name/key of this value
            value: The boolean value
        """
        # Pack boolean as a byte (0 or 1)
        data = struct.pack("?", value)
        super().__init__(name, ValueTypes.BOOL_VALUE, data)
        self._value = value

    @classmethod
    def from_data(cls, name: str, data: bytes) -> "BoolValue":
        """
        Create BoolValue from raw bytes.

        Args:
            name: The name/key
            data: Raw bytes

        Returns:
            New BoolValue instance
        """
        value = struct.unpack("?", data)[0]
        return cls(name, value)

    @classmethod
    def from_string(cls, name: str, value_str: str) -> "BoolValue":
        """
        Create BoolValue from string.

        Args:
            name: The name/key
            value_str: String representation ("true", "1", etc.)

        Returns:
            New BoolValue instance
        """
        value = value_str.lower() in ("true", "1", "yes", "on")
        return cls(name, value)

    def to_boolean(self) -> bool:
        """Get boolean value."""
        return self._value

    def to_int(self) -> int:
        """Convert to integer (0 or 1)."""
        return 1 if self._value else 0

    def to_string(self, original: bool = True) -> str:
        """
        Convert to string.

        Args:
            original: If True, return "true"/"false"; otherwise "1"/"0"

        Returns:
            String representation
        """
        if original:
            return "true" if self._value else "false"
        return "1" if self._value else "0"

    def serialize(self) -> str:
        """
        Serialize to C++ compatible format: [name,type,value];

        Returns:
            Serialized format: "[name,type,value];"
        """
        from container_module.core.value_types import get_string_from_type

        type_code = get_string_from_type(self._type)
        value_str = "true" if self._value else "false"
        return f"[{self._name},{type_code},{value_str}];"

    def __bool__(self) -> bool:
        """Python boolean conversion."""
        return self._value
