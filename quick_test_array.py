#!/usr/bin/env python3
"""Quick test for ArrayValue implementation."""

import sys
sys.path.insert(0, '.')

from container_module.values.array_value import ArrayValue
from container_module.values.numeric_value import IntValue, DoubleValue
from container_module.values.string_value import StringValue
from container_module.values.bool_value import BoolValue
from container_module.core.value_types import ValueTypes


def test_basic_creation():
    """Test basic array creation."""
    print("Test 1: Basic creation...")
    arr = ArrayValue("numbers")
    assert arr.name == "numbers"
    assert arr.type == ValueTypes.ARRAY_VALUE
    assert arr.size() == 0
    assert arr.empty()
    print("✓ Empty array created successfully")


def test_with_initial_values():
    """Test array with initial values."""
    print("\nTest 2: Array with initial values...")
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
    print("✓ Array with 3 integers created and accessed")


def test_heterogeneous():
    """Test heterogeneous array."""
    print("\nTest 3: Heterogeneous array...")
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
    print("✓ Mixed-type array works correctly")


def test_append():
    """Test append operation."""
    print("\nTest 4: Append elements...")
    arr = ArrayValue("items")
    arr.append(IntValue("", 10))
    arr.append(IntValue("", 20))
    arr.append(IntValue("", 30))

    assert arr.size() == 3
    assert arr.at(0).to_int() == 10
    assert arr.at(1).to_int() == 20
    assert arr.at(2).to_int() == 30
    print("✓ Appending elements works")


def test_python_interface():
    """Test Python list-like interface."""
    print("\nTest 5: Python list interface...")
    values = [IntValue("", i * 10) for i in range(5)]
    arr = ArrayValue("items", values)

    # len()
    assert len(arr) == 5

    # []
    assert arr[0].to_int() == 0
    assert arr[2].to_int() == 20
    assert arr[-1].to_int() == 40

    # iteration
    result = [v.to_int() for v in arr]
    assert result == [0, 10, 20, 30, 40]

    print("✓ Python list interface works")


def test_serialization():
    """Test serialization."""
    print("\nTest 6: Serialization...")
    arr = ArrayValue("numbers")
    arr.append(IntValue("value", 42))
    arr.append(IntValue("value", 100))

    result = arr.serialize()

    # Should contain header with count=2
    assert "[numbers,15,2];" in result
    print(f"  Serialized: {result[:50]}...")
    print("✓ Serialization works")


def test_nested():
    """Test nested in container."""
    print("\nTest 7: Nested in container...")
    from container_module.core.container import ValueContainer

    arr = ArrayValue("scores")
    arr.append(IntValue("", 95))
    arr.append(IntValue("", 87))
    arr.append(IntValue("", 92))

    container = ValueContainer("student")
    container.add(StringValue("name", "Alice"))
    container.add(arr)

    retrieved = container.get_value("scores")
    assert retrieved is not None
    assert isinstance(retrieved, ArrayValue)
    assert retrieved.size() == 3
    print("✓ Array can be nested in container")


def run_all_tests():
    """Run all tests."""
    print("=" * 60)
    print("Python ArrayValue Quick Tests")
    print("=" * 60)

    tests = [
        test_basic_creation,
        test_with_initial_values,
        test_heterogeneous,
        test_append,
        test_python_interface,
        test_serialization,
        test_nested,
    ]

    passed = 0
    failed = 0

    for test_func in tests:
        try:
            test_func()
            passed += 1
        except Exception as e:
            failed += 1
            print(f"✗ {test_func.__name__} failed: {e}")

    print("\n" + "=" * 60)
    print(f"Results: {passed} passed, {failed} failed")
    print("=" * 60)

    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
