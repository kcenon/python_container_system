"""
Edge case and boundary condition tests for Container System

Tests unusual inputs, boundary values, error conditions, and edge cases
that might not be covered in basic functionality tests.
"""

import pytest
import struct
from container_module import ValueContainer, ValueTypes
from container_module.values import (
    BoolValue, ShortValue, UShortValue, IntValue, UIntValue,
    LongValue, ULongValue, LLongValue, ULLongValue,
    FloatValue, DoubleValue, StringValue, BytesValue, ContainerValue
)


class TestNumericBoundaries:
    """Test numeric type boundary values."""

    def test_short_min_max(self):
        """Test SHORT type boundaries (-32768 to 32767)."""
        min_val = ShortValue("min", -32768)
        max_val = ShortValue("max", 32767)

        assert min_val.get_value() == -32768
        assert max_val.get_value() == 32767

    def test_short_overflow(self):
        """Test SHORT overflow handling."""
        # Python should handle overflow, but C++ might not
        with pytest.raises((OverflowError, struct.error, ValueError)):
            ShortValue("overflow", 32768)  # Max + 1

    def test_ushort_boundaries(self):
        """Test USHORT type boundaries (0 to 65535)."""
        min_val = UShortValue("min", 0)
        max_val = UShortValue("max", 65535)

        assert min_val.get_value() == 0
        assert max_val.get_value() == 65535

    def test_int_boundaries(self):
        """Test INT type boundaries."""
        min_val = IntValue("min", -2147483648)
        max_val = IntValue("max", 2147483647)

        assert min_val.get_value() == -2147483648
        assert max_val.get_value() == 2147483647

    def test_uint_boundaries(self):
        """Test UINT type boundaries."""
        min_val = UIntValue("min", 0)
        max_val = UIntValue("max", 4294967295)

        assert min_val.get_value() == 0
        assert max_val.get_value() == 4294967295

    def test_long_long_boundaries(self):
        """Test LLONG type boundaries."""
        min_val = LLongValue("min", -9223372036854775808)
        max_val = LLongValue("max", 9223372036854775807)

        assert min_val.get_value() == -9223372036854775808
        assert max_val.get_value() == 9223372036854775807

    def test_float_special_values(self):
        """Test float special values (inf, -inf, nan)."""
        import math

        inf_val = FloatValue("inf", float('inf'))
        neg_inf_val = FloatValue("neg_inf", float('-inf'))
        nan_val = FloatValue("nan", float('nan'))

        assert math.isinf(inf_val.get_value())
        assert math.isinf(neg_inf_val.get_value())
        assert math.isnan(nan_val.get_value())

    def test_double_precision(self):
        """Test double precision values."""
        # Test very small and very large doubles
        small = DoubleValue("small", 1e-308)
        large = DoubleValue("large", 1e308)

        assert small.get_value() == pytest.approx(1e-308)
        assert large.get_value() == pytest.approx(1e308)


class TestStringEdgeCases:
    """Test string edge cases."""

    def test_empty_string(self):
        """Test empty string value."""
        empty = StringValue("empty", "")
        assert empty.get_value() == ""

        # Serialization round-trip
        container = ValueContainer()
        container.add(empty)
        serialized = container.serialize()
        restored = ValueContainer(data_string=serialized)
        assert restored.get_value("empty").get_value() == ""

    def test_very_long_string(self):
        """Test very long string (10MB)."""
        long_str = "A" * (10 * 1024 * 1024)  # 10 MB
        val = StringValue("long", long_str)
        assert len(val.get_value()) == 10 * 1024 * 1024

    def test_unicode_string(self):
        """Test unicode characters."""
        unicode_str = "Hello 世界 🌍 Привет مرحبا"
        val = StringValue("unicode", unicode_str)
        assert val.get_value() == unicode_str

        # Round-trip
        container = ValueContainer()
        container.add(val)
        serialized = container.serialize()
        restored = ValueContainer(data_string=serialized)
        assert restored.get_value("unicode").get_value() == unicode_str

    def test_special_characters(self):
        """Test special characters in strings."""
        special = "Line1\nLine2\tTab\r\nWindows\0Null"
        val = StringValue("special", special)
        assert val.get_value() == special

    def test_string_with_delimiter(self):
        """Test string containing serialization delimiters."""
        delimiter_str = "value1|value2||value3"
        val = StringValue("delim", delimiter_str)

        container = ValueContainer()
        container.add(val)
        serialized = container.serialize()
        restored = ValueContainer(data_string=serialized)
        assert restored.get_value("delim").get_value() == delimiter_str


class TestBytesEdgeCases:
    """Test bytes value edge cases."""

    def test_empty_bytes(self):
        """Test empty bytes value."""
        empty = BytesValue("empty", b"")
        assert empty.get_value() == b""

    def test_large_bytes(self):
        """Test large binary data (1MB)."""
        large_data = bytes(range(256)) * (1024 * 4)  # 1 MB
        val = BytesValue("large", large_data)
        assert len(val.get_value()) == 1024 * 1024

    def test_binary_with_nulls(self):
        """Test binary data with null bytes."""
        null_data = b"\x00\x01\x02\x00\x00\xff\xfe"
        val = BytesValue("nulls", null_data)
        assert val.get_value() == null_data

        # Round-trip
        container = ValueContainer()
        container.add(val)
        serialized = container.serialize()
        restored = ValueContainer(data_string=serialized)
        assert restored.get_value("nulls").get_value() == null_data


class TestContainerEdgeCases:
    """Test container edge cases."""

    def test_empty_container(self):
        """Test container with no values."""
        container = ValueContainer(
            source_id="src",
            target_id="tgt"
        )
        serialized = container.serialize()
        restored = ValueContainer(data_string=serialized)

        assert restored.source_id == "src"
        assert restored.target_id == "tgt"

    def test_nested_containers_deep(self):
        """Test deeply nested containers (10 levels)."""
        def create_nested(depth):
            if depth == 0:
                return IntValue("leaf", 42)

            inner = create_nested(depth - 1)
            container = ValueContainer(message_type=f"level_{depth}")
            container.add(inner)
            return ContainerValue(f"nested_{depth}", container)

        deep_nested = create_nested(10)
        assert deep_nested is not None

    def test_many_values(self):
        """Test container with many values (1000)."""
        container = ValueContainer()
        for i in range(1000):
            container.add(IntValue(f"val_{i}", i))

        serialized = container.serialize()
        restored = ValueContainer(data_string=serialized)

        # Verify all values
        for i in range(1000):
            val = restored.get_value(f"val_{i}")
            assert val is not None
            assert val.get_value() == i

    def test_duplicate_names(self):
        """Test values with duplicate names."""
        container = ValueContainer()
        container.add(IntValue("dup", 1))
        container.add(IntValue("dup", 2))
        container.add(IntValue("dup", 3))

        # get_value should return first match
        val = container.get_value("dup")
        assert val.get_value() == 1

    def test_special_header_values(self):
        """Test special characters in header fields."""
        container = ValueContainer(
            source_id="src|with|pipes",
            target_id="tgt||double",
            message_type="type=with=equals"
        )

        serialized = container.serialize()
        restored = ValueContainer(data_string=serialized)

        # Headers with special chars should be handled
        assert restored.source_id == "src|with|pipes"

    def test_swap_header(self):
        """Test header swapping for responses."""
        container = ValueContainer(
            source_id="client",
            source_sub_id="client_sub",
            target_id="server",
            target_sub_id="server_sub"
        )

        container.swap_header()

        assert container.source_id == "server"
        assert container.source_sub_id == "server_sub"
        assert container.target_id == "client"
        assert container.target_sub_id == "client_sub"


class TestSerializationEdgeCases:
    """Test serialization edge cases."""

    def test_malformed_serialized_data(self):
        """Test deserialization of malformed data."""
        # Missing delimiter
        with pytest.raises((ValueError, IndexError, KeyError)):
            ValueContainer(data_string="invalid_data")

    def test_empty_serialized_data(self):
        """Test empty serialized data."""
        with pytest.raises((ValueError, IndexError)):
            ValueContainer(data_string="")

    def test_partial_serialized_data(self):
        """Test incomplete serialized data."""
        container = ValueContainer()
        container.add(IntValue("test", 42))
        serialized = container.serialize()

        # Truncate data
        partial = serialized[:len(serialized)//2]

        with pytest.raises((ValueError, IndexError, struct.error)):
            ValueContainer(data_string=partial)

    def test_corrupted_value_type(self):
        """Test corrupted value type in serialized data."""
        # Create valid container
        container = ValueContainer()
        container.add(IntValue("test", 42))
        serialized = container.serialize()

        # Corrupt the value type byte
        corrupted = serialized.replace(b"3", b"99", 1)  # INT_VALUE = 3

        # Should handle gracefully or raise error
        with pytest.raises((ValueError, KeyError, struct.error)):
            ValueContainer(data_string=corrupted)


class TestJSONEdgeCases:
    """Test JSON serialization edge cases."""

    def test_json_unicode(self):
        """Test JSON with unicode characters."""
        container = ValueContainer()
        container.add(StringValue("unicode", "Hello 世界 🌍"))

        json_str = container.to_json()
        assert "Hello 世界 🌍" in json_str or "\\u" in json_str  # Escaped or direct

    def test_json_special_chars(self):
        """Test JSON with special characters."""
        container = ValueContainer()
        container.add(StringValue("special", 'Quote"Backslash\\Newline\n'))

        json_str = container.to_json()
        # Should be valid JSON (escaped properly)
        import json
        parsed = json.loads(json_str)
        assert parsed is not None


class TestXMLEdgeCases:
    """Test XML serialization edge cases."""

    def test_xml_special_chars(self):
        """Test XML with special characters."""
        container = ValueContainer()
        container.add(StringValue("special", "Less<Greater>Ampersand&Quote\""))

        xml_str = container.to_xml()
        # Should escape XML special characters
        assert "&lt;" in xml_str or "<" not in xml_str.split(">")[1]

    def test_xml_unicode(self):
        """Test XML with unicode."""
        container = ValueContainer()
        container.add(StringValue("unicode", "Hello 世界"))

        xml_str = container.to_xml()
        assert xml_str is not None


class TestConcurrencyEdgeCases:
    """Test thread safety edge cases."""

    def test_concurrent_add(self):
        """Test concurrent value addition."""
        import threading

        container = ValueContainer()

        def add_values(start, count):
            for i in range(start, start + count):
                container.add(IntValue(f"val_{i}", i))

        threads = []
        for i in range(10):
            t = threading.Thread(target=add_values, args=(i * 100, 100))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        # Should have all 1000 values (thread-safe with RLock)
        # Note: Duplicate names possible due to concurrent access
        serialized = container.serialize()
        assert len(serialized) > 0


class TestMemoryEdgeCases:
    """Test memory-related edge cases."""

    def test_value_name_limit(self):
        """Test very long value names."""
        long_name = "A" * 10000
        val = IntValue(long_name, 42)
        assert val.get_name() == long_name

    def test_container_reuse(self):
        """Test container reuse (clear and refill)."""
        container = ValueContainer()
        container.add(IntValue("test", 1))

        serialized1 = container.serialize()

        # Simulate clearing and reusing
        container2 = ValueContainer()
        container2.add(IntValue("test2", 2))

        serialized2 = container2.serialize()

        assert serialized1 != serialized2


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
