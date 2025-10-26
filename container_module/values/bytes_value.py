"""
Bytes value implementation

Equivalent to C++ bytes_value.h/cpp
"""

import base64
from container_module.core.value import Value
from container_module.core.value_types import ValueTypes


class BytesValue(Value):
    """
    Raw byte array value implementation.

    Equivalent to C++ bytes_value class.
    Stores arbitrary binary data.
    """

    def __init__(self, name: str, value: bytes):
        """
        Initialize a BytesValue.

        Args:
            name: The name/key of this value
            value: The raw bytes
        """
        super().__init__(name, ValueTypes.BYTES_VALUE, value)
        self._value = value

    @classmethod
    def from_data(cls, name: str, data: bytes) -> "BytesValue":
        """
        Create BytesValue from raw bytes.

        Args:
            name: The name/key
            data: Raw bytes

        Returns:
            New BytesValue instance
        """
        return cls(name, data)

    @classmethod
    def from_string(cls, name: str, value_str: str) -> "BytesValue":
        """
        Create BytesValue from base64-encoded string.

        Args:
            name: The name/key
            value_str: Base64-encoded string

        Returns:
            New BytesValue instance
        """
        data = base64.b64decode(value_str)
        return cls(name, data)

    @classmethod
    def from_hex(cls, name: str, hex_str: str) -> "BytesValue":
        """
        Create BytesValue from hex string.

        Args:
            name: The name/key
            hex_str: Hexadecimal string

        Returns:
            New BytesValue instance
        """
        data = bytes.fromhex(hex_str)
        return cls(name, data)

    def to_bytes(self) -> bytes:
        """Get raw bytes."""
        return self._value

    def to_string(self, original: bool = True) -> str:
        """
        Convert to string representation.

        Args:
            original: If True, return base64; otherwise hex

        Returns:
            String representation
        """
        if original:
            return base64.b64encode(self._value).decode("ascii")
        return self._value.hex()

    def to_hex(self) -> str:
        """Get hex representation."""
        return self._value.hex()

    def to_base64(self) -> str:
        """Get base64 representation."""
        return base64.b64encode(self._value).decode("ascii")

    def serialize(self) -> str:
        """
        Serialize to C++ compatible format: [name,type,value];

        Returns:
            Serialized format: "[name,type,base64_data];"
        """
        from container_module.core.value_types import get_string_from_type

        type_code = get_string_from_type(self._type)
        b64_data = self.to_base64()
        return f"[{self._name},{type_code},{b64_data}];"

    def __len__(self) -> int:
        """Get byte length."""
        return len(self._value)

    def __bytes__(self) -> bytes:
        """Python bytes conversion."""
        return self._value

    def __getitem__(self, index: int) -> int:
        """Get byte at index."""
        return self._value[index]
