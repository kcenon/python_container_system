"""
Unit tests for ArrayValue implementation

Tests array creation, element access, serialization, and integration.
"""

import pytest
from container_module.values.array_value import ArrayValue
from container_module.values.numeric_value import IntValue, DoubleValue
from container_module.values.string_value import StringValue
from container_module.values.bool_value import BoolValue
from container_module.values.container_value import ContainerValue
from container_module.core.value_types import ValueTypes


class TestArrayValueCreation:
    """Test ArrayValue construction and basic properties."""

    def test_empty_array_creation(self):
        """Test creating an empty array."""
        arr = ArrayValue("numbers")
        assert arr.name == "numbers"
        assert arr.type == ValueTypes.ARRAY_VALUE
        assert arr.size() == 0
        assert arr.empty()

    def test_array_with_initial_values(self):
        """Test creating array with initial values."""
        values = [
            IntValue("", 1),
            IntValue("", 2),
            IntValue("", 3),
        ]
        arr = ArrayValue("numbers", values)
        assert arr.size() == 3
        assert not arr.empty()
        assert arr.at(0).to_int() == 1
        assert arr.at(1).to_int() == 2
        assert arr.at(2).to_int() == 3

    def test_heterogeneous_array(self):
        """Test array with different value types."""
        values = [
            IntValue("", 42),
            StringValue("", "hello"),
            DoubleValue("", 3.14),
            BoolValue("", True),
        ]
        arr = ArrayValue("mixed", values)
        assert arr.size() == 4
        assert arr.at(0).to_int() == 42
        assert arr.at(1).to_string() == "hello"
        assert abs(arr.at(2).to_double() - 3.14) < 0.01
        assert arr.at(3).to_boolean()


class TestArrayValueOperations:
    """Test array operations like append, access, clear."""

    def test_append_elements(self):
        """Test adding elements to array."""
        arr = ArrayValue("items")
        arr.append(IntValue("", 10))
        arr.append(IntValue("", 20))
        arr.append(IntValue("", 30))

        assert arr.size() == 3
        assert arr.at(0).to_int() == 10
        assert arr.at(1).to_int() == 20
        assert arr.at(2).to_int() == 30

    def test_push_back_compatibility(self):
        """Test C++-style push_back method."""
        arr = ArrayValue("items")
        arr.push_back(StringValue("", "first"))
        arr.push_back(StringValue("", "second"))

        assert arr.size() == 2
        assert arr.at(0).to_string() == "first"
        assert arr.at(1).to_string() == "second"

    def test_index_out_of_range(self):
        """Test accessing invalid indices."""
        arr = ArrayValue("items")
        arr.append(IntValue("", 1))

        with pytest.raises(IndexError):
            arr.at(-1)
        with pytest.raises(IndexError):
            arr.at(1)
        with pytest.raises(IndexError):
            arr.at(100)

    def test_clear_array(self):
        """Test clearing all elements."""
        arr = ArrayValue("items", [IntValue("", i) for i in range(5)])
        assert arr.size() == 5

        arr.clear()
        assert arr.size() == 0
        assert arr.empty()

    def test_values_returns_copy(self):
        """Test that values() returns a copy."""
        arr = ArrayValue("items")
        arr.append(IntValue("", 1))
        arr.append(IntValue("", 2))

        copy = arr.values()
        assert len(copy) == 2

        # Modifying copy should not affect original
        copy.clear()
        assert arr.size() == 2


class TestArrayValuePythonInterface:
    """Test Python list-like interface."""

    def test_len_operator(self):
        """Test len() operator."""
        arr = ArrayValue("items")
        assert len(arr) == 0

        arr.append(IntValue("", 1))
        arr.append(IntValue("", 2))
        assert len(arr) == 2

    def test_getitem_operator(self):
        """Test [] operator for reading."""
        values = [IntValue("", i * 10) for i in range(5)]
        arr = ArrayValue("items", values)

        assert arr[0].to_int() == 0
        assert arr[2].to_int() == 20
        assert arr[4].to_int() == 40

        # Python-style negative indexing
        assert arr[-1].to_int() == 40

    def test_setitem_operator(self):
        """Test [] operator for writing."""
        arr = ArrayValue("items", [IntValue("", 1), IntValue("", 2)])

        arr[0] = IntValue("", 100)
        assert arr[0].to_int() == 100

        arr[1] = StringValue("", "replaced")
        assert arr[1].to_string() == "replaced"

    def test_setitem_out_of_range(self):
        """Test [] operator with invalid index."""
        arr = ArrayValue("items", [IntValue("", 1)])

        with pytest.raises(IndexError):
            arr[5] = IntValue("", 10)

    def test_iteration(self):
        """Test iterating over array."""
        values = [IntValue("", i) for i in range(5)]
        arr = ArrayValue("items", values)

        result = [v.to_int() for v in arr]
        assert result == [0, 1, 2, 3, 4]

    def test_contains_operator(self):
        """Test 'in' operator."""
        val1 = IntValue("", 42)
        val2 = IntValue("", 100)
        arr = ArrayValue("items", [val1])

        assert val1 in arr
        assert val2 not in arr


class TestArrayValueSerialization:
    """Test text serialization."""

    def test_serialize_empty_array(self):
        """Test serializing empty array."""
        arr = ArrayValue("empty")
        result = arr.serialize()

        # Format: [name,type,count];
        assert result.startswith("[empty,15,0];")

    def test_serialize_array_with_elements(self):
        """Test serializing array with elements."""
        arr = ArrayValue("numbers")
        arr.append(IntValue("value", 42))
        arr.append(IntValue("value", 100))

        result = arr.serialize()

        # Should contain header with count=2
        assert "[numbers,15,2];" in result
        # Should contain serialized elements
        assert "[value,4," in result  # IntValue type code is 4

    def test_json_conversion(self):
        """Test JSON conversion."""
        arr = ArrayValue("data")
        arr.append(IntValue("num", 42))
        arr.append(StringValue("text", "hello"))

        json_str = arr.to_json()
        assert '"name": "data"' in json_str
        assert '"type": "array"' in json_str
        assert '"elements"' in json_str

    def test_xml_conversion(self):
        """Test XML conversion."""
        arr = ArrayValue("items")
        arr.append(IntValue("num", 10))
        arr.append(StringValue("text", "test"))

        xml_str = arr.to_xml()
        assert "<array" in xml_str
        assert 'name="items"' in xml_str
        assert 'count="2"' in xml_str


class TestArrayValueIntegration:
    """Test integration with container system."""

    def test_nested_in_container(self):
        """Test array nested in container."""
        from container_module.core.container import ValueContainer

        arr = ArrayValue("scores")
        arr.append(IntValue("", 95))
        arr.append(IntValue("", 87))
        arr.append(IntValue("", 92))

        container = ValueContainer("student")
        container.add(StringValue("name", "Alice"))
        container.add(arr)

        # Verify nested structure
        retrieved = container.get_value("scores")
        assert retrieved is not None
        assert isinstance(retrieved, ArrayValue)
        assert retrieved.size() == 3

    def test_array_of_containers(self):
        """Test array containing container values."""
        user1 = ContainerValue("user")
        user1.add(StringValue("name", "Alice"))
        user1.add(IntValue("age", 30))

        user2 = ContainerValue("user")
        user2.add(StringValue("name", "Bob"))
        user2.add(IntValue("age", 25))

        users_array = ArrayValue("users", [user1, user2])

        assert users_array.size() == 2
        assert users_array[0].get_value("name").to_string() == "Alice"
        assert users_array[1].get_value("name").to_string() == "Bob"

    def test_parent_references(self):
        """Test that array elements have correct parent references."""
        arr = ArrayValue("items")
        val1 = IntValue("first", 1)
        val2 = IntValue("second", 2)

        arr.append(val1)
        arr.append(val2)

        assert val1.parent == arr
        assert val2.parent == arr


class TestArrayValueEdgeCases:
    """Test edge cases and error conditions."""

    def test_to_string_representation(self):
        """Test string representation."""
        arr = ArrayValue("test", [IntValue("", i) for i in range(3)])
        assert "Array(3 elements)" in arr.to_string()

    def test_repr(self):
        """Test repr()."""
        arr = ArrayValue("test", [IntValue("", 1), IntValue("", 2)])
        repr_str = repr(arr)
        assert "ArrayValue" in repr_str
        assert "name='test'" in repr_str
        assert "size=2" in repr_str

    def test_large_array(self):
        """Test array with many elements."""
        values = [IntValue("", i) for i in range(1000)]
        arr = ArrayValue("large", values)

        assert arr.size() == 1000
        assert arr.at(0).to_int() == 0
        assert arr.at(999).to_int() == 999

    def test_deeply_nested_arrays(self):
        """Test arrays containing arrays."""
        inner1 = ArrayValue("inner", [IntValue("", 1), IntValue("", 2)])
        inner2 = ArrayValue("inner", [IntValue("", 3), IntValue("", 4)])
        outer = ArrayValue("outer", [inner1, inner2])

        assert outer.size() == 2
        assert outer[0].size() == 2
        assert outer[0][0].to_int() == 1
        assert outer[1][1].to_int() == 4


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
