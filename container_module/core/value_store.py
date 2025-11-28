"""
ValueStore class for domain-agnostic value storage

This module provides a pure value storage layer without messaging-specific fields.
Can be used as a general-purpose serialization container.

Equivalent to C++ value_store class.

Features:
- Type-safe value storage
- JSON/Binary serialization support
- Thread-safe operations (optional)
- Key-value storage interface
- Statistics tracking

Note: This class is part of domain separation initiative
See ValueContainer for messaging-specific wrapper
"""

from __future__ import annotations
from typing import Dict, Optional, List, Any, Iterator, Tuple
import json
import struct
from threading import RLock
from pathlib import Path

from container_module.core.value import Value
from container_module.core.value_types import (
    ValueTypes,
    get_string_from_type,
    get_type_from_string,
)


class ValueStore:
    """
    Domain-agnostic value storage.

    Pure value storage layer without messaging-specific fields.
    Can be used as a general-purpose serialization container.

    Attributes:
        values: Dictionary of stored values (key -> value)

    Example:
        >>> store = ValueStore()
        >>> store.add("name", StringValue("name", "John"))
        >>> store.add("age", IntValue("age", 30))
        >>> value = store.get("name")
        >>> print(value.to_string())  # "John"
        >>> json_str = store.serialize()
        >>> binary = store.serialize_binary()
    """

    # Binary format version for future compatibility
    BINARY_VERSION = 1

    def __init__(self) -> None:
        """Initialize an empty ValueStore."""
        # Key-value storage
        self._values: Dict[str, Value] = {}

        # Thread safety
        self._lock = RLock()
        self._thread_safe_enabled: bool = False

        # Statistics
        self._read_count: int = 0
        self._write_count: int = 0
        self._serialization_count: int = 0

    # =========================================================================
    # Value Management
    # =========================================================================

    def add(self, key: str, value: Value) -> None:
        """
        Add a value with a key.

        Args:
            key: The key for the value
            value: The Value object to add

        Note:
            Thread-safe if enable_thread_safety() was called.
            If key already exists, the value will be overwritten.
        """
        with self._get_write_lock():
            self._values[key] = value
            self._write_count += 1

    def get(self, key: str) -> Optional[Value]:
        """
        Get a value by key.

        Args:
            key: The key to look up

        Returns:
            Value if found, None otherwise

        Note:
            Thread-safe if enable_thread_safety() was called.
        """
        with self._get_read_lock():
            value = self._values.get(key)
            if value is not None:
                self._read_count += 1
            return value

    def contains(self, key: str) -> bool:
        """
        Check if a key exists.

        Args:
            key: The key to check

        Returns:
            True if key exists, False otherwise
        """
        with self._get_read_lock():
            return key in self._values

    def remove(self, key: str) -> bool:
        """
        Remove a value by key.

        Args:
            key: The key to remove

        Returns:
            True if removed, False if not found
        """
        with self._get_write_lock():
            if key in self._values:
                del self._values[key]
                return True
            return False

    def clear(self) -> None:
        """Clear all values."""
        with self._get_write_lock():
            self._values.clear()

    def size(self) -> int:
        """
        Get number of stored values.

        Returns:
            Number of values
        """
        with self._get_read_lock():
            return len(self._values)

    def empty(self) -> bool:
        """
        Check if store is empty.

        Returns:
            True if empty, False otherwise
        """
        return self.size() == 0

    def keys(self) -> List[str]:
        """
        Get all keys.

        Returns:
            List of keys
        """
        with self._get_read_lock():
            return list(self._values.keys())

    def values(self) -> List[Value]:
        """
        Get all values.

        Returns:
            List of values
        """
        with self._get_read_lock():
            return list(self._values.values())

    def items(self) -> List[Tuple[str, Value]]:
        """
        Get all key-value pairs.

        Returns:
            List of (key, value) tuples
        """
        with self._get_read_lock():
            return list(self._values.items())

    # =========================================================================
    # Serialization
    # =========================================================================

    def serialize(self) -> str:
        """
        Serialize to JSON string.

        Returns:
            JSON representation

        Raises:
            RuntimeError: If serialization fails
        """
        with self._get_read_lock():
            self._serialization_count += 1

            try:
                result = {}
                for key, value in self._values.items():
                    # Serialize each value to its JSON representation
                    result[key] = json.loads(value.to_json())
                return json.dumps(result, ensure_ascii=False, indent=2)
            except Exception as e:
                raise RuntimeError(f"Serialization failed: {e}") from e

    def serialize_binary(self) -> bytes:
        """
        Serialize to binary format.

        Binary format:
        - Version byte (1)
        - Number of entries (4 bytes, uint32)
        - For each entry:
            - Key length (4 bytes, uint32)
            - Key data (UTF-8)
            - Value type (1 byte)
            - Value length (4 bytes, uint32)
            - Value data

        Returns:
            Binary data

        Raises:
            RuntimeError: If serialization fails
        """
        with self._get_read_lock():
            self._serialization_count += 1

            try:
                result = bytearray()

                # Version byte
                result.append(self.BINARY_VERSION)

                # Number of entries
                count = len(self._values)
                result.extend(struct.pack("<I", count))

                # Serialize each key-value pair
                for key, value in self._values.items():
                    # Key length and key
                    key_bytes = key.encode("utf-8")
                    result.extend(struct.pack("<I", len(key_bytes)))
                    result.extend(key_bytes)

                    # Value type (access via .type property which returns ValueTypes enum)
                    result.append(value.type.value)

                    # Value data (access via .data property or .to_bytes())
                    value_data = value.data
                    result.extend(struct.pack("<I", len(value_data)))
                    result.extend(value_data)

                return bytes(result)
            except Exception as e:
                raise RuntimeError(f"Binary serialization failed: {e}") from e

    @classmethod
    def deserialize(cls, json_data: str) -> "ValueStore":
        """
        Deserialize from JSON string.

        Args:
            json_data: JSON string

        Returns:
            ValueStore instance

        Raises:
            RuntimeError: If deserialization fails
        """
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

        try:
            store = cls()
            data = json.loads(json_data)

            for key, value_data in data.items():
                if isinstance(value_data, dict) and "type" in value_data:
                    value_type_str = value_data.get("type", "")
                    value_type = get_type_from_string(value_type_str)
                    value_content = value_data.get("data", value_data.get("value", ""))

                    value = cls._create_value_from_type(
                        key,
                        value_type,
                        str(value_content) if value_content is not None else "",
                    )
                    if value:
                        store._values[key] = value
                else:
                    # Simple JSON value - infer type
                    value = cls._create_value_from_json(key, value_data)
                    if value:
                        store._values[key] = value

            return store
        except Exception as e:
            raise RuntimeError(f"Deserialization failed: {e}") from e

    @classmethod
    def deserialize_binary(cls, binary_data: bytes) -> "ValueStore":
        """
        Deserialize from binary format.

        Args:
            binary_data: Binary data

        Returns:
            ValueStore instance

        Raises:
            RuntimeError: If deserialization fails
        """
        try:
            store = cls()

            if len(binary_data) < 5:
                raise RuntimeError("Invalid data: too small")

            offset = 0

            # Read version byte
            version = binary_data[offset]
            offset += 1

            if version != cls.BINARY_VERSION:
                raise RuntimeError(f"Unsupported version: {version}")

            # Read number of entries
            count = struct.unpack_from("<I", binary_data, offset)[0]
            offset += 4

            # Read each key-value pair
            for i in range(count):
                if offset + 4 > len(binary_data):
                    raise RuntimeError(f"Truncated data at entry {i}")

                # Read key length
                key_len = struct.unpack_from("<I", binary_data, offset)[0]
                offset += 4

                if offset + key_len + 5 > len(binary_data):
                    raise RuntimeError("Truncated key data")

                # Read key
                key = binary_data[offset : offset + key_len].decode("utf-8")
                offset += key_len

                # Read value type
                value_type_code = binary_data[offset]
                offset += 1
                value_type = ValueTypes(value_type_code)

                # Read value length
                value_len = struct.unpack_from("<I", binary_data, offset)[0]
                offset += 4

                if offset + value_len > len(binary_data):
                    raise RuntimeError("Truncated value data")

                # Read value data
                value_data = binary_data[offset : offset + value_len]
                offset += value_len

                # Create value from binary data
                value = cls._create_value_from_binary(key, value_type, value_data)
                if value:
                    store._values[key] = value

            return store
        except Exception as e:
            raise RuntimeError(f"Binary deserialization failed: {e}") from e

    @staticmethod
    def _create_value_from_type(
        name: str, value_type: ValueTypes, value_str: str
    ) -> Optional[Value]:
        """Create a Value from type enum and string data."""
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

        try:
            if value_type == ValueTypes.BOOL_VALUE:
                return BoolValue.from_string(name, str(value_str))
            elif value_type == ValueTypes.SHORT_VALUE:
                return ShortValue.from_string(name, str(value_str))
            elif value_type == ValueTypes.USHORT_VALUE:
                return UShortValue.from_string(name, str(value_str))
            elif value_type == ValueTypes.INT_VALUE:
                return IntValue.from_string(name, str(value_str))
            elif value_type == ValueTypes.UINT_VALUE:
                return UIntValue.from_string(name, str(value_str))
            elif value_type == ValueTypes.LONG_VALUE:
                return LongValue.from_string(name, str(value_str))
            elif value_type == ValueTypes.ULONG_VALUE:
                return ULongValue.from_string(name, str(value_str))
            elif value_type == ValueTypes.LLONG_VALUE:
                return LLongValue.from_string(name, str(value_str))
            elif value_type == ValueTypes.ULLONG_VALUE:
                return ULLongValue.from_string(name, str(value_str))
            elif value_type == ValueTypes.FLOAT_VALUE:
                return FloatValue.from_string(name, str(value_str))
            elif value_type == ValueTypes.DOUBLE_VALUE:
                return DoubleValue.from_string(name, str(value_str))
            elif value_type == ValueTypes.STRING_VALUE:
                return StringValue.from_string(name, str(value_str))
            elif value_type == ValueTypes.BYTES_VALUE:
                return BytesValue.from_string(name, str(value_str))
            else:
                return None
        except Exception:
            return None

    @staticmethod
    def _create_value_from_json(name: str, value: Any) -> Optional[Value]:
        """Create a Value by inferring type from JSON value."""
        from container_module.values import (
            BoolValue,
            IntValue,
            DoubleValue,
            StringValue,
        )

        try:
            if isinstance(value, bool):
                return BoolValue(name, value)
            elif isinstance(value, int):
                return IntValue(name, value)
            elif isinstance(value, float):
                return DoubleValue(name, value)
            elif isinstance(value, str):
                return StringValue(name, value)
            else:
                return None
        except Exception:
            return None

    @staticmethod
    def _create_value_from_binary(
        name: str, value_type: ValueTypes, data: bytes
    ) -> Optional[Value]:
        """Create a Value from type enum and binary data."""
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

        try:
            if value_type == ValueTypes.BOOL_VALUE:
                return BoolValue.from_data(name, data)
            elif value_type == ValueTypes.SHORT_VALUE:
                return ShortValue.from_data(name, data)
            elif value_type == ValueTypes.USHORT_VALUE:
                return UShortValue.from_data(name, data)
            elif value_type == ValueTypes.INT_VALUE:
                return IntValue.from_data(name, data)
            elif value_type == ValueTypes.UINT_VALUE:
                return UIntValue.from_data(name, data)
            elif value_type == ValueTypes.LONG_VALUE:
                return LongValue.from_data(name, data)
            elif value_type == ValueTypes.ULONG_VALUE:
                return ULongValue.from_data(name, data)
            elif value_type == ValueTypes.LLONG_VALUE:
                return LLongValue.from_data(name, data)
            elif value_type == ValueTypes.ULLONG_VALUE:
                return ULLongValue.from_data(name, data)
            elif value_type == ValueTypes.FLOAT_VALUE:
                return FloatValue.from_data(name, data)
            elif value_type == ValueTypes.DOUBLE_VALUE:
                return DoubleValue.from_data(name, data)
            elif value_type == ValueTypes.STRING_VALUE:
                return StringValue.from_data(name, data)
            elif value_type == ValueTypes.BYTES_VALUE:
                return BytesValue.from_data(name, data)
            else:
                return None
        except Exception:
            return None

    # =========================================================================
    # File I/O
    # =========================================================================

    def save_to_file(self, file_path: str, binary: bool = False) -> None:
        """
        Save to file.

        Args:
            file_path: Path to save to
            binary: If True, use binary format; otherwise JSON
        """
        path = Path(file_path)
        if binary:
            path.write_bytes(self.serialize_binary())
        else:
            path.write_text(self.serialize(), encoding="utf-8")

    @classmethod
    def load_from_file(cls, file_path: str, binary: bool = False) -> "ValueStore":
        """
        Load from file.

        Args:
            file_path: Path to load from
            binary: If True, use binary format; otherwise JSON

        Returns:
            ValueStore instance
        """
        path = Path(file_path)
        if binary:
            return cls.deserialize_binary(path.read_bytes())
        else:
            return cls.deserialize(path.read_text(encoding="utf-8"))

    # =========================================================================
    # Thread Safety
    # =========================================================================

    def enable_thread_safety(self, enabled: bool = True) -> None:
        """
        Enable or disable thread-safe operations.

        Args:
            enabled: True to enable thread safety
        """
        self._thread_safe_enabled = enabled

    def is_thread_safe(self) -> bool:
        """
        Check if thread safety is enabled.

        Returns:
            True if enabled
        """
        return self._thread_safe_enabled

    def _get_read_lock(self) -> Any:
        """Get a read lock context manager."""
        if self._thread_safe_enabled:
            return self._lock
        return _DummyLock()

    def _get_write_lock(self) -> Any:
        """Get a write lock context manager."""
        if self._thread_safe_enabled:
            return self._lock
        return _DummyLock()

    # =========================================================================
    # Statistics
    # =========================================================================

    def get_read_count(self) -> int:
        """Get number of read operations."""
        return self._read_count

    def get_write_count(self) -> int:
        """Get number of write operations."""
        return self._write_count

    def get_serialization_count(self) -> int:
        """Get number of serialization operations."""
        return self._serialization_count

    def reset_statistics(self) -> None:
        """Reset all statistics to zero."""
        self._read_count = 0
        self._write_count = 0
        self._serialization_count = 0

    # =========================================================================
    # Python Special Methods
    # =========================================================================

    def __len__(self) -> int:
        """Return number of values."""
        return self.size()

    def __contains__(self, key: str) -> bool:
        """Check if key exists."""
        return self.contains(key)

    def __getitem__(self, key: str) -> Value:
        """Get value by key."""
        value = self.get(key)
        if value is None:
            raise KeyError(key)
        return value

    def __setitem__(self, key: str, value: Value) -> None:
        """Set value by key."""
        self.add(key, value)

    def __delitem__(self, key: str) -> None:
        """Delete value by key."""
        if not self.remove(key):
            raise KeyError(key)

    def __iter__(self) -> Iterator[str]:
        """Iterate over keys."""
        return iter(self.keys())

    def __str__(self) -> str:
        """String representation."""
        return f"ValueStore(size={self.size()})"

    def __repr__(self) -> str:
        """Detailed representation."""
        return f"ValueStore(values={list(self._values.keys())})"


class _DummyLock:
    """Dummy lock that does nothing (for when thread safety is disabled)."""

    def __enter__(self) -> "_DummyLock":
        return self

    def __exit__(self, *args: Any) -> None:
        pass
