"""
Value types enumeration and conversion utilities

This module provides the enumeration of all supported value types
and conversion functions between string representations and enum values.

Equivalent to C++ core/value_types.h
"""

from enum import Enum, auto
from typing import Dict, Union


class ValueTypes(Enum):
    """
    Enumeration of available value types in the container system.

    Maps to C++ value_types enum:
    - NULL_VALUE: Null/empty value (code: "0")
    - BOOL_VALUE: Boolean true/false (code: "1")
    - SHORT_VALUE: 16-bit signed integer (code: "2")
    - USHORT_VALUE: 16-bit unsigned integer (code: "3")
    - INT_VALUE: 32-bit signed integer (code: "4")
    - UINT_VALUE: 32-bit unsigned integer (code: "5")
    - LONG_VALUE: Platform-dependent signed long (code: "6")
    - ULONG_VALUE: Platform-dependent unsigned long (code: "7")
    - LLONG_VALUE: 64-bit signed integer (code: "8")
    - ULLONG_VALUE: 64-bit unsigned integer (code: "9")
    - FLOAT_VALUE: 32-bit floating point (code: "10")
    - DOUBLE_VALUE: 64-bit floating point (code: "11")
    - STRING_VALUE: UTF-8 string (code: "12") - matches C++ std::string position
    - BYTES_VALUE: Raw byte array (code: "13") - matches C++ std::vector<uint8_t> position
    - CONTAINER_VALUE: Nested container (code: "14")
    - ARRAY_VALUE: Array/list of values (code: "15")
    """

    NULL_VALUE = 0
    BOOL_VALUE = 1
    SHORT_VALUE = 2
    USHORT_VALUE = 3
    INT_VALUE = 4
    UINT_VALUE = 5
    LONG_VALUE = 6
    ULONG_VALUE = 7
    LLONG_VALUE = 8
    ULLONG_VALUE = 9
    FLOAT_VALUE = 10
    DOUBLE_VALUE = 11
    STRING_VALUE = 12  # Matches C++ string_value and ValueVariant std::string position
    BYTES_VALUE = 13   # Matches C++ bytes_value and ValueVariant std::vector<uint8_t> position
    CONTAINER_VALUE = 14
    ARRAY_VALUE = 15


# Type mapping: string code -> ValueTypes (equivalent to C++ type_map)
_TYPE_MAP: Dict[str, ValueTypes] = {
    "0": ValueTypes.NULL_VALUE,
    "1": ValueTypes.BOOL_VALUE,
    "2": ValueTypes.SHORT_VALUE,
    "3": ValueTypes.USHORT_VALUE,
    "4": ValueTypes.INT_VALUE,
    "5": ValueTypes.UINT_VALUE,
    "6": ValueTypes.LONG_VALUE,
    "7": ValueTypes.ULONG_VALUE,
    "8": ValueTypes.LLONG_VALUE,
    "9": ValueTypes.ULLONG_VALUE,
    "10": ValueTypes.FLOAT_VALUE,
    "11": ValueTypes.DOUBLE_VALUE,
    "12": ValueTypes.STRING_VALUE,  # Matches C++ string_value position
    "13": ValueTypes.BYTES_VALUE,   # Matches C++ bytes_value position
    "14": ValueTypes.CONTAINER_VALUE,
    "15": ValueTypes.ARRAY_VALUE,
}

# Reverse mapping: ValueTypes -> string code
_REVERSE_TYPE_MAP: Dict[ValueTypes, str] = {v: k for k, v in _TYPE_MAP.items()}


def convert_value_type(target: Union[str, ValueTypes]) -> Union[ValueTypes, str]:
    """
    Convert between string representation and ValueTypes enum.

    Equivalent to C++ convert_value_type() overloads.

    Args:
        target: Either a string code ("0"-"14") or a ValueTypes enum

    Returns:
        If target is str: Returns corresponding ValueTypes
        If target is ValueTypes: Returns corresponding string code

    Examples:
        >>> convert_value_type("4")
        ValueTypes.INT_VALUE
        >>> convert_value_type(ValueTypes.INT_VALUE)
        "4"
    """
    if isinstance(target, str):
        # String -> ValueTypes
        return _TYPE_MAP.get(target, ValueTypes.NULL_VALUE)
    elif isinstance(target, ValueTypes):
        # ValueTypes -> String
        return _REVERSE_TYPE_MAP.get(target, "0")
    else:
        raise TypeError(f"Expected str or ValueTypes, got {type(target)}")


def get_type_from_string(type_str: str) -> ValueTypes:
    """
    Convert string code to ValueTypes enum.

    Equivalent to C++ get_type_from_string().

    Args:
        type_str: String code ("0"-"14")

    Returns:
        Corresponding ValueTypes, or NULL_VALUE if not found
    """
    return _TYPE_MAP.get(type_str, ValueTypes.NULL_VALUE)


def get_string_from_type(value_type: ValueTypes) -> str:
    """
    Convert ValueTypes enum to string code.

    Equivalent to C++ get_string_from_type().

    Args:
        value_type: ValueTypes enum

    Returns:
        Corresponding string code, or "0" if not found
    """
    return _REVERSE_TYPE_MAP.get(value_type, "0")


def is_numeric_type(value_type: ValueTypes) -> bool:
    """
    Check if a ValueTypes represents a numeric type.

    Args:
        value_type: ValueTypes to check

    Returns:
        True if numeric (short, int, long, float, double), False otherwise
    """
    numeric_types = {
        ValueTypes.SHORT_VALUE,
        ValueTypes.USHORT_VALUE,
        ValueTypes.INT_VALUE,
        ValueTypes.UINT_VALUE,
        ValueTypes.LONG_VALUE,
        ValueTypes.ULONG_VALUE,
        ValueTypes.LLONG_VALUE,
        ValueTypes.ULLONG_VALUE,
        ValueTypes.FLOAT_VALUE,
        ValueTypes.DOUBLE_VALUE,
    }
    return value_type in numeric_types


def is_integer_type(value_type: ValueTypes) -> bool:
    """
    Check if a ValueTypes represents an integer type.

    Args:
        value_type: ValueTypes to check

    Returns:
        True if integer type, False otherwise
    """
    integer_types = {
        ValueTypes.SHORT_VALUE,
        ValueTypes.USHORT_VALUE,
        ValueTypes.INT_VALUE,
        ValueTypes.UINT_VALUE,
        ValueTypes.LONG_VALUE,
        ValueTypes.ULONG_VALUE,
        ValueTypes.LLONG_VALUE,
        ValueTypes.ULLONG_VALUE,
    }
    return value_type in integer_types


def is_floating_type(value_type: ValueTypes) -> bool:
    """
    Check if a ValueTypes represents a floating-point type.

    Args:
        value_type: ValueTypes to check

    Returns:
        True if float or double, False otherwise
    """
    return value_type in {ValueTypes.FLOAT_VALUE, ValueTypes.DOUBLE_VALUE}
