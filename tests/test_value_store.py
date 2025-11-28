"""
Unit tests for ValueStore class

Tests the domain-agnostic value storage functionality
that mirrors the C++ value_store implementation.
"""

import pytest
import json
import tempfile
import os
from pathlib import Path

from container_module.core.value_store import ValueStore
from container_module.values import (
    BoolValue,
    ShortValue,
    UShortValue,
    IntValue,
    UIntValue,
    LongValue,
    ULongValue,
    LLongValue,
    ULLongValue,
    FloatValue,
    DoubleValue,
    StringValue,
    BytesValue,
)


class TestValueStoreBasics:
    """Basic ValueStore functionality tests."""

    def test_create_empty_store(self):
        """Test creating an empty ValueStore."""
        store = ValueStore()
        assert store.size() == 0
        assert store.empty()
        assert len(store) == 0

    def test_add_and_get_value(self):
        """Test adding and retrieving a value."""
        store = ValueStore()
        value = IntValue("count", 42)
        store.add("count", value)

        assert store.size() == 1
        assert not store.empty()

        retrieved = store.get("count")
        assert retrieved is not None
        assert retrieved.to_int() == 42

    def test_contains(self):
        """Test checking if key exists."""
        store = ValueStore()
        store.add("name", StringValue("name", "test"))

        assert store.contains("name")
        assert "name" in store
        assert not store.contains("missing")
        assert "missing" not in store

    def test_remove(self):
        """Test removing values."""
        store = ValueStore()
        store.add("key1", IntValue("key1", 1))
        store.add("key2", IntValue("key2", 2))

        assert store.size() == 2

        result = store.remove("key1")
        assert result is True
        assert store.size() == 1
        assert not store.contains("key1")

        result = store.remove("nonexistent")
        assert result is False

    def test_clear(self):
        """Test clearing all values."""
        store = ValueStore()
        store.add("a", IntValue("a", 1))
        store.add("b", IntValue("b", 2))
        store.add("c", IntValue("c", 3))

        assert store.size() == 3

        store.clear()
        assert store.size() == 0
        assert store.empty()

    def test_keys_values_items(self):
        """Test getting keys, values, and items."""
        store = ValueStore()
        store.add("name", StringValue("name", "John"))
        store.add("age", IntValue("age", 30))

        keys = store.keys()
        assert "name" in keys
        assert "age" in keys

        values = store.values()
        assert len(values) == 2

        items = store.items()
        assert len(items) == 2


class TestValueStoreTypes:
    """Tests for different value types in ValueStore."""

    def test_bool_value(self):
        """Test storing boolean values."""
        store = ValueStore()
        store.add("flag", BoolValue("flag", True))

        value = store.get("flag")
        assert value is not None
        assert value.to_boolean() is True

    def test_numeric_values(self):
        """Test storing various numeric types."""
        store = ValueStore()

        store.add("short", ShortValue("short", -100))
        store.add("ushort", UShortValue("ushort", 100))
        store.add("int", IntValue("int", -1000))
        store.add("uint", UIntValue("uint", 1000))
        store.add("long", LongValue("long", -100000))
        store.add("ulong", ULongValue("ulong", 100000))
        store.add("llong", LLongValue("llong", -10000000000))
        store.add("ullong", ULLongValue("ullong", 10000000000))
        store.add("float", FloatValue("float", 3.14))
        store.add("double", DoubleValue("double", 3.14159265359))

        assert store.get("short").to_short() == -100
        assert store.get("ushort").to_ushort() == 100
        assert store.get("int").to_int() == -1000
        assert store.get("uint").to_uint() == 1000
        assert store.get("long").to_long() == -100000
        assert store.get("ulong").to_ulong() == 100000
        assert store.get("llong").to_llong() == -10000000000
        assert store.get("ullong").to_ullong() == 10000000000
        assert abs(store.get("float").to_float() - 3.14) < 0.01
        assert abs(store.get("double").to_double() - 3.14159265359) < 0.0001

    def test_string_value(self):
        """Test storing string values."""
        store = ValueStore()
        store.add("message", StringValue("message", "Hello, World!"))

        value = store.get("message")
        assert value is not None
        assert value.to_string() == "Hello, World!"

    def test_bytes_value(self):
        """Test storing binary data."""
        store = ValueStore()
        data = bytes([0x01, 0x02, 0x03, 0x04])
        store.add("data", BytesValue("data", data))

        value = store.get("data")
        assert value is not None
        assert value.to_bytes() == data


class TestValueStoreSerialization:
    """Tests for ValueStore serialization."""

    def test_json_serialization(self):
        """Test JSON serialization round-trip."""
        store = ValueStore()
        store.add("name", StringValue("name", "Alice"))
        store.add("age", IntValue("age", 25))
        store.add("active", BoolValue("active", True))

        # Serialize
        json_str = store.serialize()
        assert json_str is not None
        assert len(json_str) > 0

        # Verify it's valid JSON
        parsed = json.loads(json_str)
        assert "name" in parsed
        assert "age" in parsed
        assert "active" in parsed

    def test_binary_serialization(self):
        """Test binary serialization round-trip."""
        store = ValueStore()
        store.add("count", IntValue("count", 42))
        store.add("message", StringValue("message", "test"))
        store.add("flag", BoolValue("flag", True))

        # Serialize
        binary = store.serialize_binary()
        assert binary is not None
        assert len(binary) > 0

        # Deserialize
        restored = ValueStore.deserialize_binary(binary)
        assert restored.size() == 3
        assert restored.get("count").to_int() == 42
        assert restored.get("message").to_string() == "test"
        assert restored.get("flag").to_boolean() is True

    def test_binary_format_version(self):
        """Test binary format includes version byte."""
        store = ValueStore()
        store.add("test", IntValue("test", 1))

        binary = store.serialize_binary()
        # First byte should be version
        assert binary[0] == ValueStore.BINARY_VERSION


class TestValueStoreFileIO:
    """Tests for file I/O operations."""

    def test_save_load_json(self):
        """Test saving and loading JSON files."""
        store = ValueStore()
        store.add("user", StringValue("user", "Bob"))
        store.add("score", IntValue("score", 100))

        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            temp_path = f.name

        try:
            store.save_to_file(temp_path, binary=False)

            loaded = ValueStore.load_from_file(temp_path, binary=False)
            assert loaded.size() == 2
        finally:
            os.unlink(temp_path)

    def test_save_load_binary(self):
        """Test saving and loading binary files."""
        store = ValueStore()
        store.add("data", BytesValue("data", bytes([1, 2, 3, 4, 5])))
        store.add("label", StringValue("label", "binary test"))

        with tempfile.NamedTemporaryFile(mode='wb', suffix='.bin', delete=False) as f:
            temp_path = f.name

        try:
            store.save_to_file(temp_path, binary=True)

            loaded = ValueStore.load_from_file(temp_path, binary=True)
            assert loaded.size() == 2
            assert loaded.get("data").to_bytes() == bytes([1, 2, 3, 4, 5])
        finally:
            os.unlink(temp_path)


class TestValueStoreThreadSafety:
    """Tests for thread safety features."""

    def test_enable_thread_safety(self):
        """Test enabling thread safety."""
        store = ValueStore()

        assert not store.is_thread_safe()

        store.enable_thread_safety(True)
        assert store.is_thread_safe()

        store.enable_thread_safety(False)
        assert not store.is_thread_safe()

    def test_thread_safe_operations(self):
        """Test operations with thread safety enabled."""
        store = ValueStore()
        store.enable_thread_safety(True)

        store.add("key", IntValue("key", 1))
        value = store.get("key")
        assert value is not None
        assert value.to_int() == 1

        store.remove("key")
        assert not store.contains("key")


class TestValueStoreStatistics:
    """Tests for statistics tracking."""

    def test_read_write_counts(self):
        """Test read and write count tracking."""
        store = ValueStore()

        assert store.get_read_count() == 0
        assert store.get_write_count() == 0

        store.add("a", IntValue("a", 1))
        assert store.get_write_count() == 1

        store.add("b", IntValue("b", 2))
        assert store.get_write_count() == 2

        store.get("a")
        assert store.get_read_count() == 1

        store.get("b")
        assert store.get_read_count() == 2

    def test_serialization_count(self):
        """Test serialization count tracking."""
        store = ValueStore()
        store.add("x", IntValue("x", 10))

        assert store.get_serialization_count() == 0

        store.serialize()
        assert store.get_serialization_count() == 1

        store.serialize_binary()
        assert store.get_serialization_count() == 2

    def test_reset_statistics(self):
        """Test resetting statistics."""
        store = ValueStore()
        store.add("test", IntValue("test", 1))
        store.get("test")
        store.serialize()

        assert store.get_write_count() > 0
        assert store.get_read_count() > 0
        assert store.get_serialization_count() > 0

        store.reset_statistics()

        assert store.get_write_count() == 0
        assert store.get_read_count() == 0
        assert store.get_serialization_count() == 0


class TestValueStorePythonInterface:
    """Tests for Python special methods."""

    def test_len(self):
        """Test __len__ method."""
        store = ValueStore()
        assert len(store) == 0

        store.add("a", IntValue("a", 1))
        assert len(store) == 1

    def test_getitem_setitem(self):
        """Test __getitem__ and __setitem__."""
        store = ValueStore()

        store["name"] = StringValue("name", "Test")
        assert store["name"].to_string() == "Test"

    def test_getitem_keyerror(self):
        """Test __getitem__ raises KeyError for missing key."""
        store = ValueStore()

        with pytest.raises(KeyError):
            _ = store["missing"]

    def test_delitem(self):
        """Test __delitem__."""
        store = ValueStore()
        store.add("key", IntValue("key", 1))

        del store["key"]
        assert not store.contains("key")

        with pytest.raises(KeyError):
            del store["missing"]

    def test_iter(self):
        """Test iteration over keys."""
        store = ValueStore()
        store.add("a", IntValue("a", 1))
        store.add("b", IntValue("b", 2))
        store.add("c", IntValue("c", 3))

        keys = list(store)
        assert len(keys) == 3
        assert "a" in keys
        assert "b" in keys
        assert "c" in keys

    def test_str_repr(self):
        """Test string representations."""
        store = ValueStore()
        store.add("test", IntValue("test", 1))

        assert "ValueStore" in str(store)
        assert "ValueStore" in repr(store)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
