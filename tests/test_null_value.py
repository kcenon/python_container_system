"""
Tests for NullValue implementation

Ensures NullValue works correctly and maintains C++ compatibility.
"""

import pytest
from container_module.values import NullValue
from container_module.core.value_types import ValueTypes


class TestNullValue:
    """Test cases for NullValue class."""

    def test_creation(self):
        """Test NullValue creation."""
        null_val = NullValue("test_null")
        assert null_val.name == "test_null"
        assert null_val.type == ValueTypes.NULL_VALUE

    def test_is_null(self):
        """Test is_null returns True."""
        null_val = NullValue("optional_field")
        assert null_val.is_null() is True

    def test_size_is_zero(self):
        """Test that NullValue has zero size."""
        null_val = NullValue("empty")
        assert null_val.size == 0

    def test_to_string(self):
        """Test to_string returns 'null'."""
        null_val = NullValue("test")
        assert null_val.to_string() == "null"
        assert null_val.to_string(original=False) == "null"

    def test_serialize(self):
        """Test serialize produces C++ compatible format."""
        null_val = NullValue("field_name")
        serialized = null_val.serialize()
        assert serialized == "[field_name,0,null];"

    def test_to_json(self):
        """Test JSON conversion."""
        import json

        null_val = NullValue("json_field")
        json_str = null_val.to_json()
        json_dict = json.loads(json_str)
        assert json_dict["name"] == "json_field"
        assert json_dict["type"] == "null"
        assert json_dict["value"] is None

    def test_to_xml(self):
        """Test XML conversion."""
        null_val = NullValue("xml_field")
        xml = null_val.to_xml()
        assert 'name="xml_field"' in xml
        assert 'type="null"' in xml

    def test_from_data(self):
        """Test creation from data bytes."""
        null_val = NullValue.from_data("from_bytes", b"ignored")
        assert null_val.name == "from_bytes"
        assert null_val.is_null() is True

    def test_from_string(self):
        """Test creation from string."""
        null_val = NullValue.from_string("from_str", "any_value")
        assert null_val.name == "from_str"
        assert null_val.is_null() is True

    def test_bool_conversion(self):
        """Test Python bool conversion (null is falsy)."""
        null_val = NullValue("falsy")
        assert bool(null_val) is False

    def test_equality(self):
        """Test equality comparison."""
        null1 = NullValue("same_name")
        null2 = NullValue("same_name")
        null3 = NullValue("different_name")

        assert null1 == null2
        assert null1 != null3
        assert null1 != "not_a_null_value"

    def test_repr(self):
        """Test string representation."""
        null_val = NullValue("debug_field")
        repr_str = repr(null_val)
        assert "NullValue" in repr_str
        assert "debug_field" in repr_str

    def test_data_is_empty(self):
        """Test that underlying data is empty bytes."""
        null_val = NullValue("empty_data")
        assert null_val.data == b""


class TestNullValueCrossLanguage:
    """Cross-language compatibility tests for NullValue."""

    def test_type_code(self):
        """Test that type code matches C++ (0)."""
        null_val = NullValue("cross_lang")
        assert null_val.type.value == 0

    def test_serialization_format(self):
        """Test serialization matches C++ format."""
        null_val = NullValue("cpp_compat")
        serialized = null_val.serialize()
        # Format: [name,type_code,value];
        parts = serialized.strip(";").strip("[]").split(",")
        assert len(parts) == 3
        assert parts[0] == "cpp_compat"
        assert parts[1] == "0"  # NULL_VALUE type code
        assert parts[2] == "null"
