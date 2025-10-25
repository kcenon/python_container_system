"""
Numeric value implementations

Equivalent to C++ numeric value templates and implementations
"""

import struct
from abc import ABC
from typing import Union
from container_module.core.value import Value
from container_module.core.value_types import ValueTypes


class NumericValue(Value, ABC):
    """
    Base class for numeric values.

    Provides common functionality for all numeric types.
    """

    def __init__(
        self,
        name: str,
        value_type: ValueTypes,
        value: Union[int, float],
        format_char: str,
    ):
        """
        Initialize a NumericValue.

        Args:
            name: The name/key
            value_type: The specific numeric type
            value: The numeric value
            format_char: struct format character for packing
        """
        data = struct.pack(format_char, value)
        super().__init__(name, value_type, data)
        self._value = value
        self._format_char = format_char

    @classmethod
    def from_data(cls, name: str, data: bytes):
        """Create from raw bytes."""
        raise NotImplementedError("Subclasses must implement from_data")

    @classmethod
    def from_string(cls, name: str, value_str: str):
        """Create from string."""
        raise NotImplementedError("Subclasses must implement from_string")

    def to_int(self) -> int:
        """Convert to integer."""
        return int(self._value)

    def to_float(self) -> float:
        """Convert to float."""
        return float(self._value)

    def to_double(self) -> float:
        """Convert to double (same as float in Python)."""
        return float(self._value)

    def to_string(self, original: bool = True) -> str:
        """Convert to string."""
        return str(self._value)

    def serialize(self) -> str:
        """Serialize to string format."""
        from container_module.core.value_types import get_string_from_type

        type_code = get_string_from_type(self._type)
        return f"{self._name}|{type_code}|{self._value}"


# Integer types
class ShortValue(NumericValue):
    """16-bit signed integer (-32768 to 32767)."""

    def __init__(self, name: str, value: int):
        super().__init__(name, ValueTypes.SHORT_VALUE, value, "h")

    @classmethod
    def from_data(cls, name: str, data: bytes) -> "ShortValue":
        value = struct.unpack("h", data)[0]
        return cls(name, value)

    @classmethod
    def from_string(cls, name: str, value_str: str) -> "ShortValue":
        return cls(name, int(value_str))

    def to_short(self) -> int:
        return self._value


class UShortValue(NumericValue):
    """16-bit unsigned integer (0 to 65535)."""

    def __init__(self, name: str, value: int):
        super().__init__(name, ValueTypes.USHORT_VALUE, value, "H")

    @classmethod
    def from_data(cls, name: str, data: bytes) -> "UShortValue":
        value = struct.unpack("H", data)[0]
        return cls(name, value)

    @classmethod
    def from_string(cls, name: str, value_str: str) -> "UShortValue":
        return cls(name, int(value_str))

    def to_ushort(self) -> int:
        return self._value


class IntValue(NumericValue):
    """32-bit signed integer."""

    def __init__(self, name: str, value: int):
        super().__init__(name, ValueTypes.INT_VALUE, value, "i")

    @classmethod
    def from_data(cls, name: str, data: bytes) -> "IntValue":
        value = struct.unpack("i", data)[0]
        return cls(name, value)

    @classmethod
    def from_string(cls, name: str, value_str: str) -> "IntValue":
        return cls(name, int(value_str))


class UIntValue(NumericValue):
    """32-bit unsigned integer."""

    def __init__(self, name: str, value: int):
        super().__init__(name, ValueTypes.UINT_VALUE, value, "I")

    @classmethod
    def from_data(cls, name: str, data: bytes) -> "UIntValue":
        value = struct.unpack("I", data)[0]
        return cls(name, value)

    @classmethod
    def from_string(cls, name: str, value_str: str) -> "UIntValue":
        return cls(name, int(value_str))

    def to_uint(self) -> int:
        return self._value


class LongValue(NumericValue):
    """Platform-dependent signed long."""

    def __init__(self, name: str, value: int):
        super().__init__(name, ValueTypes.LONG_VALUE, value, "l")

    @classmethod
    def from_data(cls, name: str, data: bytes) -> "LongValue":
        value = struct.unpack("l", data)[0]
        return cls(name, value)

    @classmethod
    def from_string(cls, name: str, value_str: str) -> "LongValue":
        return cls(name, int(value_str))

    def to_long(self) -> int:
        return self._value


class ULongValue(NumericValue):
    """Platform-dependent unsigned long."""

    def __init__(self, name: str, value: int):
        super().__init__(name, ValueTypes.ULONG_VALUE, value, "L")

    @classmethod
    def from_data(cls, name: str, data: bytes) -> "ULongValue":
        value = struct.unpack("L", data)[0]
        return cls(name, value)

    @classmethod
    def from_string(cls, name: str, value_str: str) -> "ULongValue":
        return cls(name, int(value_str))

    def to_ulong(self) -> int:
        return self._value


class LLongValue(NumericValue):
    """64-bit signed integer."""

    def __init__(self, name: str, value: int):
        super().__init__(name, ValueTypes.LLONG_VALUE, value, "q")

    @classmethod
    def from_data(cls, name: str, data: bytes) -> "LLongValue":
        value = struct.unpack("q", data)[0]
        return cls(name, value)

    @classmethod
    def from_string(cls, name: str, value_str: str) -> "LLongValue":
        return cls(name, int(value_str))

    def to_llong(self) -> int:
        return self._value


class ULLongValue(NumericValue):
    """64-bit unsigned integer."""

    def __init__(self, name: str, value: int):
        super().__init__(name, ValueTypes.ULLONG_VALUE, value, "Q")

    @classmethod
    def from_data(cls, name: str, data: bytes) -> "ULLongValue":
        value = struct.unpack("Q", data)[0]
        return cls(name, value)

    @classmethod
    def from_string(cls, name: str, value_str: str) -> "ULLongValue":
        return cls(name, int(value_str))

    def to_ullong(self) -> int:
        return self._value


# Floating-point types
class FloatValue(NumericValue):
    """32-bit floating point."""

    def __init__(self, name: str, value: float):
        super().__init__(name, ValueTypes.FLOAT_VALUE, value, "f")

    @classmethod
    def from_data(cls, name: str, data: bytes) -> "FloatValue":
        value = struct.unpack("f", data)[0]
        return cls(name, value)

    @classmethod
    def from_string(cls, name: str, value_str: str) -> "FloatValue":
        return cls(name, float(value_str))


class DoubleValue(NumericValue):
    """64-bit floating point."""

    def __init__(self, name: str, value: float):
        super().__init__(name, ValueTypes.DOUBLE_VALUE, value, "d")

    @classmethod
    def from_data(cls, name: str, data: bytes) -> "DoubleValue":
        value = struct.unpack("d", data)[0]
        return cls(name, value)

    @classmethod
    def from_string(cls, name: str, value_str: str) -> "DoubleValue":
        return cls(name, float(value_str))
