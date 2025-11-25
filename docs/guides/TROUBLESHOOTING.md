# Python Container System - Troubleshooting Guide

> **Version:** 1.0
> **Last Updated:** 2025-11-26

This guide consolidates the most common issues reported while using the Python Container System and explains how to resolve them.

---

## Table of Contents

1. [Installation Issues](#1-installation-issues)
2. [Serialization Issues](#2-serialization-issues)
3. [Type Conversion Errors](#3-type-conversion-errors)
4. [Cross-Language Compatibility](#4-cross-language-compatibility)
5. [Performance Issues](#5-performance-issues)
6. [Thread Safety Issues](#6-thread-safety-issues)
7. [Common Error Messages](#7-common-error-messages)

---

## 1. Installation Issues

### ModuleNotFoundError: No module named 'container_module'

**Symptoms:**
- Import fails with ModuleNotFoundError
- Package not recognized

**Solution:**
```bash
# Install in development mode
cd python_container_system
pip install -e .

# Or install from package
pip install python-container-system

# Verify installation
python -c "from container_module import ValueContainer; print('OK')"
```

### ImportError: cannot import name 'X'

**Symptoms:**
- Specific class import fails
- Version mismatch

**Solution:**
```python
# Check correct import paths
from container_module import ValueContainer
from container_module.values import StringValue, IntValue, BoolValue

# NOT:
# from container_module.core import ValueContainer  # Wrong path
```

### Type Hints Not Working

**Symptoms:**
- IDE doesn't recognize types
- mypy errors

**Solution:**
```bash
# Ensure Python 3.8+ is used
python --version

# Install type stubs if available
pip install types-container-module  # If published

# Run mypy with proper config
mypy container_module --ignore-missing-imports
```

---

## 2. Serialization Issues

### Serialization Returns Empty or Invalid Data

**Symptoms:**
- `serialize()` returns empty string
- `serialize_to_bytes()` returns empty bytes
- Deserialization fails

**Checklist:**
1. Ensure the container has values before serialization
2. Check that value names are not empty strings
3. Verify data encoding (UTF-8)

```python
# Good: Non-empty name
c.add(StringValue("name", "Alice"))

# Problematic: Empty name (use with caution)
c.add(StringValue("", "value"))

# Check before serialization
if c.get_value("name"):
    serialized = c.serialize()
else:
    print("Warning: Container may be empty")
```

### JSON Serialization Fails

**Symptoms:**
- `to_json()` raises exception
- Special characters cause issues

**Solution:**
```python
# Ensure strings are valid UTF-8
name = "Hello\x00World"  # Contains null byte
clean_name = name.replace("\x00", "")  # Remove invalid chars
c.add(StringValue("name", clean_name))

# For binary data, use BytesValue (auto base64 encoded in JSON)
c.add(BytesValue("data", binary_data))

# Check JSON output
try:
    json_str = c.to_json()
    import json
    json.loads(json_str)  # Validate JSON
except json.JSONDecodeError as e:
    print(f"Invalid JSON: {e}")
```

### Deserialization Fails with Type Mismatch

**Symptoms:**
- Values have wrong types after deserialization
- Type information lost

**Solution:**
```python
# Use correct deserialization method for format
if data.startswith('{'):
    c.from_json(data)  # JSON format
elif isinstance(data, bytes):
    c.deserialize_from_bytes(data)  # Binary format
else:
    c.deserialize(data)  # String format

# Verify types after deserialization
value = c.get_value("count")
print(f"Type: {value.value_type}, Value: {value.to_int()}")
```

---

## 3. Type Conversion Errors

### Numeric Conversion Fails

**Symptoms:**
- `to_int()` returns wrong value
- Overflow errors

**Checklist:**
1. Check if value type matches conversion method
2. Verify numeric ranges
3. Check for None values

```python
value = c.get_value("count")
if value is None:
    print("Value not found")
    return

# Check value type before conversion
if value.value_type == ValueType.INT:
    num = value.to_int()
elif value.value_type == ValueType.LLONG:
    num = value.to_llong()
elif value.value_type == ValueType.STRING:
    # String to number conversion
    num = int(value.to_string())
else:
    print(f"Unexpected type: {value.value_type}")
```

### LongValue Range Error

**Symptoms:**
- `LongValue` rejects values > INT32_MAX
- "Value out of range" error

**Cause:** LongValue is 32-bit for C++ compatibility

**Solution:**
```python
import sys

value = 2147483648  # Exceeds INT32_MAX

# Check range before creating LongValue
if -2147483648 <= value <= 2147483647:
    c.add(LongValue("val", value))
else:
    # Use LLongValue for larger values
    c.add(LLongValue("val", value))
```

### String Conversion Fails for Binary Data

**Symptoms:**
- `to_string()` raises exception for BytesValue
- Binary data corrupted

**Solution:**
```python
value = c.get_value("data")

if value.value_type == ValueType.BYTES:
    # Use to_bytes() for binary data
    data = value.to_bytes()

    # If string representation needed, use base64
    import base64
    str_repr = base64.b64encode(data).decode('ascii')
    print(f"Base64: {str_repr}")
else:
    # Safe to use to_string()
    print(value.to_string())
```

---

## 4. Cross-Language Compatibility

### Data Not Compatible with C++

**Symptoms:**
- C++ server cannot deserialize Python data
- Type mismatches between languages

**Checklist:**
1. Use `serialize_to_bytes()` for binary format
2. Ensure value type mappings match
3. Check byte order (little-endian)

**Type Mapping:**

| Python Type | C++ Type | Notes |
|-------------|----------|-------|
| ShortValue | short_value | 16-bit signed |
| IntValue | int_value | 32-bit signed |
| LongValue | long_value | 32-bit signed |
| LLongValue | llong_value | 64-bit signed |
| FloatValue | float_value | 32-bit float |
| DoubleValue | double_value | 64-bit float |
| StringValue | string_value | UTF-8 encoded |
| BytesValue | bytes_value | Raw binary |

```python
# Use binary format for C++ interop
binary_data = c.serialize_to_bytes()
# Send binary_data to C++ server
```

### JSON Format Differs Between Languages

**Symptoms:**
- JSON from Python doesn't parse correctly in C++
- Field names don't match

**Solution:**
Use JSON v2.0 format for cross-language compatibility:

```python
from container_module.adapters import JsonV2Adapter

# Convert to v2.0 format
json_v2 = JsonV2Adapter.to_json(container)

# Parse from v2.0 format
restored = JsonV2Adapter.from_json(json_v2)
```

See [JSON_V2_ADAPTER](../JSON_V2_ADAPTER.md) for details.

---

## 5. Performance Issues

### Slow Serialization Performance

**Symptoms:**
- Serialization takes longer than expected
- High CPU usage

**Checklist:**
1. Use binary format instead of JSON/XML
2. Avoid serializing unnecessarily large containers
3. Batch small containers

```python
# Slow: JSON serialization
json_str = c.to_json()  # ~50K ops/sec

# Fast: Binary serialization
binary = c.serialize_to_bytes()  # ~100K ops/sec

# Optimization: Batch small containers
batch = ValueContainer(message_type="batch")
for item in items:
    batch.add(ContainerValue(f"item_{item.id}"))
binary = batch.serialize_to_bytes()  # Single serialization
```

### High Memory Usage

**Symptoms:**
- Memory grows when processing many containers
- Out of memory errors

**Solution:**
```python
# Clear containers after use
c.clear_value()

# Delete large containers explicitly
del large_container

# Use generator for large datasets
def process_containers(items):
    for item in items:
        c = ValueContainer()
        c.add(StringValue("data", item))
        yield c.serialize_to_bytes()
        c.clear_value()  # Clear for GC

# Process without holding all in memory
for binary in process_containers(large_dataset):
    send_to_server(binary)
```

---

## 6. Thread Safety Issues

### Race Conditions

**Symptoms:**
- Inconsistent data when using threads
- Random crashes

**Solution:**
```python
import threading

# Enable thread safety
container = ValueContainer(message_type="thread_safe")
container.enable_thread_safety(True)

# Or use external lock
lock = threading.RLock()

def safe_add(name, value):
    with lock:
        container.add(StringValue(name, value))

def safe_get(name):
    with lock:
        return container.get_value(name)
```

### Deadlock

**Symptoms:**
- Application hangs
- Threads waiting indefinitely

**Solution:**
```python
# Avoid nested locks
# Bad:
def bad_operation():
    with lock1:
        with lock2:  # Potential deadlock
            pass

# Good: Use single lock or lock ordering
container = ValueContainer()
container.enable_thread_safety(True)  # Internal lock handles this
```

---

## 7. Common Error Messages

### "Value not found"

**Cause:** Trying to get a value that doesn't exist

**Solution:**
```python
value = c.get_value("key")
if value is None:
    # Handle missing value
    print("Key not found, using default")
    value = StringValue("key", "default")
    c.add(value)
```

### "Invalid value type"

**Cause:** Creating value with invalid data

**Solution:**
```python
# Ensure correct type for value
try:
    value = IntValue("count", "not_a_number")  # Will fail
except (TypeError, ValueError) as e:
    print(f"Invalid value: {e}")
    value = IntValue("count", 0)  # Use default
```

### "Serialization failed"

**Cause:** Container contains unserializable data

**Solution:**
```python
# Check all values before serialization
for name in container.get_all_value_names():
    value = container.get_value(name)
    try:
        # Verify each value can be serialized
        _ = value.serialize()
    except Exception as e:
        print(f"Value '{name}' cannot be serialized: {e}")
        container.remove(name)

# Now safe to serialize
serialized = container.serialize()
```

### "Invalid binary format"

**Cause:** Corrupted or incomplete binary data

**Solution:**
```python
# Verify data integrity before deserialization
if len(data) < 4:
    print("Data too short for binary format")
    return None

# Try alternative formats
c = ValueContainer()
try:
    c.deserialize_from_bytes(data)
except Exception:
    try:
        c.from_json(data.decode('utf-8'))
    except Exception:
        print("Could not parse data in any format")
        return None
```

---

## Getting Help

If your issue isn't covered here:

1. **Search existing issues**: [GitHub Issues](https://github.com/kcenon/python_container_system/issues)
2. **Ask in discussions**: [GitHub Discussions](https://github.com/kcenon/python_container_system/discussions)
3. **Report new issue** with:
   - Python version (`python --version`)
   - Container System version
   - Minimal reproducible example
   - Full stack trace

---

**Last Updated:** 2025-11-26
