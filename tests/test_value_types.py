"""
Tests for value_types module
"""

import pytest
from container_module.core.value_types import (
    ValueTypes,
    convert_value_type,
    get_type_from_string,
    get_string_from_type,
    is_numeric_type,
    is_integer_type,
    is_floating_type,
)


class TestValueTypes:
    """Test ValueTypes enumeration and conversion functions."""

    def test_value_types_enum(self):
        """Test ValueTypes enum values matching C++/.NET."""
        assert ValueTypes.NULL_VALUE.value == 0
        assert ValueTypes.BOOL_VALUE.value == 1
        assert ValueTypes.INT_VALUE.value == 4
        assert ValueTypes.STRING_VALUE.value == 12  # Matches C++ string_value position
        assert ValueTypes.BYTES_VALUE.value == 13  # Matches C++ bytes_value position
        assert ValueTypes.CONTAINER_VALUE.value == 14

    def test_convert_value_type_string_to_enum(self):
        """Test string to ValueTypes conversion."""
        assert convert_value_type("0") == ValueTypes.NULL_VALUE
        assert convert_value_type("1") == ValueTypes.BOOL_VALUE
        assert convert_value_type("4") == ValueTypes.INT_VALUE
        assert convert_value_type("12") == ValueTypes.STRING_VALUE  # Matches C++
        assert convert_value_type("13") == ValueTypes.BYTES_VALUE  # Matches C++
        assert convert_value_type("999") == ValueTypes.NULL_VALUE  # Invalid

    def test_convert_value_type_enum_to_string(self):
        """Test ValueTypes to string conversion."""
        assert convert_value_type(ValueTypes.NULL_VALUE) == "0"
        assert convert_value_type(ValueTypes.BOOL_VALUE) == "1"
        assert convert_value_type(ValueTypes.INT_VALUE) == "4"
        assert convert_value_type(ValueTypes.STRING_VALUE) == "12"  # Matches C++
        assert convert_value_type(ValueTypes.BYTES_VALUE) == "13"  # Matches C++

    def test_get_type_from_string(self):
        """Test get_type_from_string function."""
        assert get_type_from_string("10") == ValueTypes.FLOAT_VALUE
        assert get_type_from_string("11") == ValueTypes.DOUBLE_VALUE
        assert get_type_from_string("invalid") == ValueTypes.NULL_VALUE

    def test_get_string_from_type(self):
        """Test get_string_from_type function."""
        assert get_string_from_type(ValueTypes.FLOAT_VALUE) == "10"
        assert get_string_from_type(ValueTypes.DOUBLE_VALUE) == "11"

    def test_is_numeric_type(self):
        """Test is_numeric_type function."""
        assert is_numeric_type(ValueTypes.INT_VALUE) is True
        assert is_numeric_type(ValueTypes.FLOAT_VALUE) is True
        assert is_numeric_type(ValueTypes.DOUBLE_VALUE) is True
        assert is_numeric_type(ValueTypes.STRING_VALUE) is False
        assert is_numeric_type(ValueTypes.BOOL_VALUE) is False

    def test_is_integer_type(self):
        """Test is_integer_type function."""
        assert is_integer_type(ValueTypes.INT_VALUE) is True
        assert is_integer_type(ValueTypes.LLONG_VALUE) is True
        assert is_integer_type(ValueTypes.FLOAT_VALUE) is False
        assert is_integer_type(ValueTypes.STRING_VALUE) is False

    def test_is_floating_type(self):
        """Test is_floating_type function."""
        assert is_floating_type(ValueTypes.FLOAT_VALUE) is True
        assert is_floating_type(ValueTypes.DOUBLE_VALUE) is True
        assert is_floating_type(ValueTypes.INT_VALUE) is False
        assert is_floating_type(ValueTypes.STRING_VALUE) is False

    def test_convert_value_type_invalid_input(self):
        """Test convert_value_type with invalid input."""
        with pytest.raises(TypeError):
            convert_value_type(123)  # Not str or ValueTypes
