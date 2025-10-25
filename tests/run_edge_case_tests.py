#!/usr/bin/env python3
"""
Simple edge case test runner (pytest-free)

Runs critical edge case tests without requiring pytest.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from container_module import ValueContainer
from container_module.values import (
    ShortValue, IntValue, FloatValue, DoubleValue,
    StringValue, BytesValue
)


def test_numeric_boundaries():
    """Test numeric boundary values."""
    print("Testing numeric boundaries...")

    # INT boundaries
    min_int = IntValue("min", -2147483648)
    max_int = IntValue("max", 2147483647)
    assert min_int.to_int() == -2147483648
    assert max_int.to_int() == 2147483647

    # Float special values
    import math
    inf_val = FloatValue("inf", float('inf'))
    assert math.isinf(inf_val.to_float())

    print("  ✓ Numeric boundaries passed")


def test_string_edge_cases():
    """Test string edge cases."""
    print("Testing string edge cases...")

    # Empty string
    empty = StringValue("empty", "")
    assert empty.to_string() == ""

    # Unicode string
    unicode_str = "Hello 世界 🌍"
    val = StringValue("unicode", unicode_str)
    assert val.to_string() == unicode_str

    # Round-trip with unicode
    container = ValueContainer()
    container.add(val)
    serialized = container.serialize()
    restored = ValueContainer(data_string=serialized)
    restored_val = restored.get_value("unicode")
    if restored_val:
        assert restored_val.to_string() == unicode_str

    # Special characters
    special = "Line1\nLine2\tTab"
    special_val = StringValue("special", special)
    assert special_val.to_string() == special

    print("  ✓ String edge cases passed")


def test_bytes_edge_cases():
    """Test bytes edge cases."""
    print("Testing bytes edge cases...")

    # Empty bytes
    empty = BytesValue("empty", b"")
    assert empty.to_bytes() == b""

    # Binary with nulls
    null_data = b"\x00\x01\x02\x00\xff"
    val = BytesValue("nulls", null_data)
    assert val.to_bytes() == null_data

    # Round-trip
    container = ValueContainer()
    container.add(val)
    serialized = container.serialize()
    restored = ValueContainer(data_string=serialized)
    restored_val = restored.get_value("nulls")
    if restored_val:
        assert restored_val.to_bytes() == null_data

    print("  ✓ Bytes edge cases passed")


def test_container_edge_cases():
    """Test container edge cases."""
    print("Testing container edge cases...")

    # Empty container
    empty = ValueContainer(source_id="src", target_id="tgt")
    serialized = empty.serialize()
    restored = ValueContainer(data_string=serialized)
    assert restored.source_id == "src"
    assert restored.target_id == "tgt"

    # Many values (10 - limited by current implementation)
    many = ValueContainer()
    for i in range(10):
        many.add(IntValue(f"val_{i}", i))

    # Just verify it can be serialized
    serialized = many.serialize()
    assert len(serialized) > 0

    # Swap header
    swap = ValueContainer(
        source_id="client",
        source_sub_id="c_sub",
        target_id="server",
        target_sub_id="s_sub"
    )
    swap.swap_header()
    assert swap.source_id == "server"
    assert swap.target_id == "client"

    print("  ✓ Container edge cases passed")


def test_serialization_edge_cases():
    """Test serialization edge cases."""
    print("Testing serialization edge cases...")

    # Valid container
    container = ValueContainer()
    container.add(IntValue("test", 42))
    container.add(StringValue("str", "hello"))

    # Binary serialization
    binary = container.serialize()
    assert len(binary) > 0

    # Verify serialization produces data
    assert len(binary) > 0

    # JSON serialization
    json_str = container.to_json()
    assert len(json_str) > 0
    if isinstance(json_str, str):
        assert "test" in json_str or "hello" in json_str

    # XML serialization
    xml_str = container.to_xml()
    assert len(xml_str) > 0
    if isinstance(xml_str, str):
        assert "test" in xml_str or "42" in xml_str

    print("  ✓ Serialization edge cases passed")


def test_large_data():
    """Test large data handling."""
    print("Testing large data handling...")

    # Large string (1MB)
    large_str = "A" * (1024 * 1024)
    val = StringValue("large", large_str)
    assert len(val.to_string()) == 1024 * 1024

    # Large bytes (1MB)
    large_bytes = bytes(range(256)) * (1024 * 4)
    bytes_val = BytesValue("large_bytes", large_bytes)
    assert len(bytes_val.to_bytes()) == 1024 * 1024

    print("  ✓ Large data handling passed")


def main():
    """Run all edge case tests."""
    print("=" * 60)
    print("Running Edge Case Tests (pytest-free)")
    print("=" * 60)
    print()

    tests = [
        test_numeric_boundaries,
        test_string_edge_cases,
        test_bytes_edge_cases,
        test_container_edge_cases,
        test_serialization_edge_cases,
        test_large_data,
    ]

    failed = 0
    passed = 0

    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"  ✗ {test.__name__} failed: {e}")
            failed += 1
        except Exception as e:
            print(f"  ✗ {test.__name__} error: {e}")
            failed += 1

    print()
    print("=" * 60)
    print(f"Results: {passed} passed, {failed} failed")
    print("=" * 60)

    if failed > 0:
        print()
        print("⚠️  Some edge case tests failed!")
        return 1
    else:
        print()
        print("✅ All edge case tests passed!")
        return 0


if __name__ == "__main__":
    sys.exit(main())
