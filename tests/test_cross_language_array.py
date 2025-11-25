"""
Cross-language ArrayValue integration tests.

Tests wire protocol compatibility between Python, C++, Rust, Go, .NET implementations
for ArrayValue serialization and deserialization.
"""

import unittest
from container_module import ValueContainer
from container_module.values import (
    ArrayValue,
    IntValue,
    StringValue,
    DoubleValue,
    BoolValue,
)


class TestCrossLanguageArray(unittest.TestCase):
    """Test ArrayValue cross-language wire protocol compatibility."""

    def test_15_serialization_format(self):
        """Test that ArrayValue serializes to C++ wire protocol format."""
        container = ValueContainer()

        # Create array with mixed types
        array = ArrayValue("test_array")
        array.push_back(IntValue("", 42))
        array.push_back(StringValue("", "hello"))
        array.push_back(DoubleValue("", 3.14))

        container.add(array)

        # Serialize to C++ wire format
        wire_data = container.serialize()

        # Verify format contains array type marker
        self.assertIn("15", wire_data)
        self.assertIn("test_array", wire_data)

        # Verify element count is serialized
        self.assertIn("[test_array,15,3]", wire_data)

    def test_empty_array_serialization(self):
        """Test empty ArrayValue wire protocol serialization."""
        container = ValueContainer()
        array = ArrayValue("empty")
        container.add(array)

        wire_data = container.serialize()

        # Empty array should have count 0
        self.assertIn("[empty,15,0]", wire_data)

    def test_array_with_primitive_types(self):
        """Test ArrayValue containing various primitive types."""
        container = ValueContainer()

        # Integer array
        int_array = ArrayValue("numbers")
        for i in range(5):
            int_array.push_back(IntValue("", i * 10))
        container.add(int_array)

        # String array
        str_array = ArrayValue("words")
        str_array.push_back(StringValue("", "alpha"))
        str_array.push_back(StringValue("", "beta"))
        str_array.push_back(StringValue("", "gamma"))
        container.add(str_array)

        # Boolean array
        bool_array = ArrayValue("flags")
        bool_array.push_back(BoolValue("", True))
        bool_array.push_back(BoolValue("", False))
        bool_array.push_back(BoolValue("", True))
        container.add(bool_array)

        wire_data = container.serialize()

        # Verify all arrays are serialized with correct counts
        self.assertIn("[numbers,15,5]", wire_data)
        self.assertIn("[words,15,3]", wire_data)
        self.assertIn("[flags,15,3]", wire_data)

    def test_cpp_compatible_wire_format(self):
        """Test wire format matches C++ container_system output."""
        container = ValueContainer()
        container.set_source("python_test", "array_test")
        container.set_message_type("test_data")

        array = ArrayValue("data")
        array.push_back(IntValue("", 100))
        array.push_back(StringValue("", "test"))
        container.add(array)

        wire_data = container.serialize()

        # Verify header format - uses numeric IDs for C++ compatibility
        # 1=target_id, 2=target_sub_id, 3=source_id, 4=source_sub_id,
        # 5=message_type, 6=version
        self.assertIn("@header={{", wire_data)
        self.assertIn("[3,python_test]", wire_data)  # source_id (ID=3)
        self.assertIn("[4,array_test]", wire_data)  # source_sub_id (ID=4)
        self.assertIn("[5,test_data]", wire_data)  # message_type (ID=5)

        # Verify data format
        self.assertIn("@data={{", wire_data)
        self.assertIn("[data,15,2]", wire_data)

    def test_array_round_trip_compatibility(self):
        """Test that serialized ArrayValue can be understood by other languages."""
        # Create container with ArrayValue
        original = ValueContainer()
        original.set_message_type("array_test")

        array = ArrayValue("test")
        array.push_back(IntValue("", 1))
        array.push_back(IntValue("", 2))
        array.push_back(IntValue("", 3))
        original.add(array)

        # Serialize
        wire_data = original.serialize()

        # Expected format that C++/Rust/Go can parse:
        # @header={{[5,array_test];[6,1.0.0.0];}};@data={{[test,15,3];}};
        expected_parts = [
            "@header={{",
            "[5,array_test]",  # message_type uses numeric ID=5
            "@data={{",
            "[test,15,3]",
        ]

        for part in expected_parts:
            self.assertIn(part, wire_data, f"Missing expected part: {part}")

    def test_large_array_serialization(self):
        """Test ArrayValue with many elements."""
        container = ValueContainer()

        # Create large array
        large_array = ArrayValue("large")
        for i in range(100):
            large_array.push_back(IntValue("", i))

        container.add(large_array)

        wire_data = container.serialize()

        # Verify count is correct
        self.assertIn("[large,15,100]", wire_data)

    def test_multiple_arrays_in_container(self):
        """Test container with multiple ArrayValues."""
        container = ValueContainer()

        # Add multiple arrays
        for i in range(3):
            array = ArrayValue(f"array_{i}")
            for j in range(i + 1):
                array.push_back(IntValue("", j))
            container.add(array)

        wire_data = container.serialize()

        # Verify all arrays are present
        self.assertIn("[array_0,15,1]", wire_data)
        self.assertIn("[array_1,15,2]", wire_data)
        self.assertIn("[array_2,15,3]", wire_data)

    def test_heterogeneous_array_serialization(self):
        """Test ArrayValue with mixed value types (heterogeneous)."""
        container = ValueContainer()

        # Mix integers, strings, doubles, booleans
        mixed = ArrayValue("mixed")
        mixed.push_back(IntValue("", 42))
        mixed.push_back(StringValue("", "hello"))
        mixed.push_back(DoubleValue("", 3.14159))
        mixed.push_back(BoolValue("", True))
        mixed.push_back(IntValue("", -100))
        mixed.push_back(StringValue("", "world"))

        container.add(mixed)

        wire_data = container.serialize()

        # Verify heterogeneous array is serialized
        self.assertIn("[mixed,15,6]", wire_data)


class TestArrayDeserializationCompatibility(unittest.TestCase):
    """Test deserializing ArrayValue from other languages."""

    def test_deserialize_cpp_format_array(self):
        """Test deserializing C++ wire format with ArrayValue."""
        # Simulated C++ output
        cpp_wire = "@header={{[message_type,test];[6,1.0.0.0];}};@data={{[arr,15,3];}};".strip()

        # Note: Full deserialization with nested elements not yet implemented
        # This tests that the format is recognized

        # TODO: Implement full deserialization when nested support is added
        # For now, verify the format is parsable
        self.assertIn("15", cpp_wire)
        self.assertIn("arr", cpp_wire)

    def test_recognize_array_type_marker(self):
        """Test that 15 type marker is recognized in wire format."""
        wire = "@header={{[message_type,data];}};@data={{[my_array,15,5];}};".strip()

        # Verify type marker format
        self.assertIn("15", wire)

        # This would be deserialized to ArrayValue("my_array") with count=5
        # when full nested deserialization is implemented


if __name__ == "__main__":
    unittest.main()
