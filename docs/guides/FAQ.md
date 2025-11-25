# Python Container System - Frequently Asked Questions

> **Version:** 1.0
> **Last Updated:** 2025-11-26
> **Audience:** Users, Developers

This FAQ addresses common questions about the Python Container System, covering containers, values, serialization, and integration.

---

## Table of Contents

1. [General Questions](#general-questions)
2. [Container Basics](#container-basics)
3. [Value Types](#value-types)
4. [Serialization](#serialization)
5. [Performance](#performance)
6. [Integration](#integration)
7. [Advanced Topics](#advanced-topics)

---

## General Questions

### 1. What is the Python Container System?

A type-safe, high-performance container and serialization system for Python:
- **Type-safe containers** using Python type hints
- **Multiple serialization formats** (Binary, JSON, XML, MessagePack)
- **Cross-language compatibility** with C++, .NET, and Go implementations
- **15 value types** with full type checking
- **Zero external dependencies** (standard library only)

```python
from container_module import ValueContainer
from container_module.values import StringValue, IntValue, DoubleValue

container = ValueContainer(message_type="user_data")
container.add(StringValue("name", "John"))
container.add(IntValue("age", 30))
container.add(DoubleValue("score", 95.5))

# Serialize to JSON
json_str = container.to_json()
```

---

### 2. What Python version is required?

**Required:** Python 3.8+

**Recommended:** Python 3.10+ for best type hint support

---

### 3. How does it differ from dataclasses or JSON libraries?

| Feature | Container System | dataclasses | json module |
|---------|------------------|-------------|-------------|
| Type Safety | Strong (15 types) | Basic | None |
| Cross-language | Yes (C++, .NET, Go) | No | JSON only |
| Binary Format | Yes | No | No |
| Nested Structures | Yes | Yes | Yes |
| Type Metadata | Preserved | Lost in JSON | Lost |
| Thread Safety | Optional locks | Manual | N/A |

---

## Container Basics

### 4. How do I create a container?

```python
from container_module import ValueContainer
from container_module.values import StringValue, IntValue

# Empty container
container1 = ValueContainer()

# Container with message type
container2 = ValueContainer(message_type="user_profile")

# Full container with header
container3 = ValueContainer(
    source_id="client_app",
    source_sub_id="instance_1",
    target_id="server_api",
    target_sub_id="v2",
    message_type="user_registration"
)
```

---

### 5. How do I add values to a container?

```python
from container_module.values import (
    StringValue, IntValue, DoubleValue, BoolValue,
    BytesValue, ContainerValue
)

c = ValueContainer()

# Primitive types
c.add(StringValue("name", "Alice"))
c.add(IntValue("age", 25))
c.add(DoubleValue("height", 165.5))
c.add(BoolValue("active", True))

# Binary data
c.add(BytesValue("data", bytes([0x01, 0x02, 0x03])))

# Nested container
address = ContainerValue("address")
address.add(StringValue("city", "Seoul"))
address.add(StringValue("zip", "12345"))
c.add(address)
```

---

### 6. How do I retrieve values?

```python
# Get value by name (first occurrence)
name = c.get_value("name")
if name:
    print(f"Name: {name.to_string()}")

# Get value at specific index (for multiple values with same name)
first_tag = c.get_value("tag", 0)
second_tag = c.get_value("tag", 1)

# Get all values with same name
all_tags = c.value_array("tag")
for tag in all_tags:
    print(tag.to_string())

# Check if value exists
if c.get_value("email"):
    print("Email found")

# Access raw value
user_id = c.get_value("user_id")
if user_id:
    print(f"User ID (int): {user_id.to_int()}")
    print(f"User ID (str): {user_id.to_string()}")
```

---

## Value Types

### 7. What value types are supported?

**Numeric Types:**
- `ShortValue`, `UShortValue` (16-bit integers)
- `IntValue`, `UIntValue` (32-bit integers)
- `LongValue`, `ULongValue` (32-bit for C++ compatibility)
- `LLongValue`, `ULLongValue` (64-bit integers)
- `FloatValue`, `DoubleValue` (floating point)

**Other Types:**
- `BoolValue` (boolean)
- `StringValue` (UTF-8 string)
- `BytesValue` (binary data)
- `ContainerValue` (nested container)
- `ArrayValue` (array of values)

```python
from container_module.values import *

# All supported types
c.add(BoolValue("enabled", True))
c.add(ShortValue("short_val", 123))
c.add(IntValue("int_val", 12345))
c.add(LLongValue("long_val", 123456789012))
c.add(FloatValue("float_val", 3.14))
c.add(DoubleValue("double_val", 3.14159265359))
c.add(StringValue("text", "Hello"))
c.add(BytesValue("binary", bytes([0xAB, 0xCD])))
```

---

### 8. How do I work with arrays?

```python
from container_module.values import ArrayValue, IntValue, StringValue

# Create array of integers
int_array = ArrayValue("scores")
int_array.add(IntValue("", 85))
int_array.add(IntValue("", 90))
int_array.add(IntValue("", 95))
c.add(int_array)

# Create array of strings
string_array = ArrayValue("tags")
for tag in ["python", "container", "serialization"]:
    string_array.add(StringValue("", tag))
c.add(string_array)

# Iterate array
scores = c.get_value("scores")
if scores:
    for i in range(scores.child_count()):
        child = scores.get_child("", i)
        if child:
            print(f"Score {i}: {child.to_int()}")
```

See [ARRAY_VALUE_GUIDE](../ARRAY_VALUE_GUIDE.md) for detailed usage.

---

### 9. How do I work with nested containers?

```python
from container_module.values import ContainerValue, StringValue, IntValue

# Create nested structure
root = ValueContainer(message_type="root")

# Create user with address
address = ContainerValue("address")
address.add(StringValue("city", "Seoul"))
address.add(StringValue("country", "Korea"))
address.add(StringValue("zip", "12345"))

user = ContainerValue("user")
user.add(StringValue("name", "Alice"))
user.add(IntValue("age", 30))
user.add(address)

root.add(user)

# Access nested values
user_value = root.get_value("user")
if user_value:
    name = user_value.get_child("name", 0)
    if name:
        print(f"User name: {name.to_string()}")

    addr = user_value.get_child("address", 0)
    if addr:
        city = addr.get_child("city", 0)
        if city:
            print(f"City: {city.to_string()}")
```

---

## Serialization

### 10. What serialization formats are supported?

**String Format** (human-readable):
```python
serialized = c.serialize()
restored = ValueContainer(data_string=serialized)
```

**Binary Format** (fastest):
```python
# Serialize to bytes
binary_data = c.serialize_to_bytes()

# Deserialize from bytes
restored = ValueContainer()
restored.deserialize_from_bytes(binary_data)
```

**JSON Format** (interoperable):
```python
json_str = c.to_json()
restored = ValueContainer()
restored.from_json(json_str)
```

**XML Format** (legacy support):
```python
xml_str = c.to_xml()
restored = ValueContainer()
restored.from_xml(xml_str)
```

---

### 11. Which format should I use?

| Format | Speed | Size | Use Case |
|--------|-------|------|----------|
| **Binary** | Fastest | Smallest | Network, cross-language |
| **String** | Fast | Medium | Debugging, logging |
| **JSON** | Medium | Medium | REST APIs, configuration |
| **XML** | Slowest | Largest | Legacy systems, SOAP |

---

### 12. How do I serialize to/from JSON?

```python
# Serialize
c = ValueContainer(message_type="user_data")
c.add(StringValue("name", "Alice"))
c.add(IntValue("age", 30))

json_str = c.to_json()
# Result: {"message_type":"user_data","values":[...]}

# Deserialize
restored = ValueContainer()
restored.from_json(json_str)

name = restored.get_value("name")
print(name.to_string())  # "Alice"
```

For cross-language JSON compatibility, see [JSON_V2_ADAPTER](../JSON_V2_ADAPTER.md).

---

## Performance

### 13. What is the performance?

**Benchmarks** (Apple M1, Python 3.11):

| Operation | Throughput | Notes |
|-----------|------------|-------|
| Container creation | ~200K/s | Empty container |
| Value addition | ~500K/s | Single value |
| Binary serialize | ~100K/s | Medium container |
| JSON serialize | ~50K/s | Medium container |
| Value access | ~1M/s | By name lookup |

See [PERFORMANCE_REPORT](../../benchmarks/PERFORMANCE_REPORT.md) for detailed benchmarks.

---

### 14. How do I optimize performance?

```python
# 1. Use binary format for speed
binary_data = c.serialize_to_bytes()  # Fastest

# 2. Disable thread safety when not needed
c = ValueContainer(message_type="fast")
# c.enable_thread_safety(False)  # Default is disabled

# 3. Batch operations
# Add all values, then serialize once
for i in range(100):
    c.add(IntValue(f"item_{i}", i))
serialized = c.serialize_to_bytes()  # Single serialization

# 4. Reuse containers
c.clear_value()  # Clear values but keep container
```

---

## Integration

### 15. How do I integrate with C++ container_system?

Use the binary serialization format for cross-language compatibility:

```python
# Python: Serialize
c = ValueContainer(message_type="request")
c.add(StringValue("action", "query"))
binary_data = c.serialize_to_bytes()

# Send binary_data to C++ server...

# C++ side:
# auto container = value_container::deserialize_from_bytes(bytes);
# auto action = container->get_value<std::string>("action");
```

---

### 16. Can I use MessagePack?

MessagePack is supported through the optional msgpack dependency:

```bash
pip install msgpack
```

```python
# If msgpack is installed
import msgpack

# Convert container to dict, then pack
data = container.to_dict()
packed = msgpack.packb(data)

# Unpack and restore
unpacked = msgpack.unpackb(packed)
restored = ValueContainer.from_dict(unpacked)
```

---

### 17. How do I integrate with REST APIs?

```python
from flask import Flask, request, jsonify
from container_module import ValueContainer
from container_module.values import StringValue

app = Flask(__name__)

@app.route('/api/process', methods=['POST'])
def process():
    # Parse incoming container
    c = ValueContainer()
    c.from_json(request.data.decode())

    # Process request
    action = c.get_value("action")

    # Send response
    response = ValueContainer(message_type="response")
    response.add(StringValue("status", "success"))

    return response.to_json(), 200, {'Content-Type': 'application/json'}
```

---

## Advanced Topics

### 18. Is it thread-safe?

By default, containers are **not thread-safe**. Enable thread safety when needed:

```python
import threading

# Enable thread safety
container = ValueContainer(message_type="thread_safe")
container.enable_thread_safety(True)

def worker(worker_id):
    container.add(StringValue(f"worker_{worker_id}", f"data_{worker_id}"))

# Use in multiple threads
threads = [threading.Thread(target=worker, args=(i,)) for i in range(10)]
for t in threads:
    t.start()
for t in threads:
    t.join()
```

---

### 19. How do I swap headers for response messages?

```python
# Incoming request
request = ValueContainer(
    source_id="client",
    source_sub_id="client_sub",
    target_id="server",
    target_sub_id="server_sub",
    message_type="query"
)

# Create response by swapping headers
response = request.copy(containing_values=False)
response.swap_header()

# Now: source="server/server_sub", target="client/client_sub"
response.set_message_type("query_response")
response.add(StringValue("result", "success"))
```

---

### 20. How do I debug containers?

```python
import json

# Print container structure
print(f"Message type: {c.message_type}")
print(f"Source: {c.source_id}/{c.source_sub_id}")
print(f"Target: {c.target_id}/{c.target_sub_id}")

# Print serialized form (human-readable)
print(c.serialize())

# Print JSON (formatted)
json_str = c.to_json()
print(json.dumps(json.loads(json_str), indent=2))

# Print all values
print(f"Value count: {len(c.value_array(''))}")
for key in set(v.name for v in c.value_array('')):
    values = c.value_array(key)
    for v in values:
        print(f"  {v.name} ({v.value_type}): {v.to_string()}")
```

---

### 21. What are the memory considerations?

**Memory Usage (approximate):**
- **Empty container**: ~500 bytes
- **Per value**: 100-200 bytes (depends on type)
- **String value**: 100 bytes + string length
- **Container value**: 500 bytes + nested values

**Optimization:**
```python
# Clear containers for reuse
c.clear_value()

# Use smaller numeric types when possible
c.add(ShortValue("count", 100))  # 2 bytes vs 8 bytes

# Delete large containers when done
del large_container
```

---

### 22. Where can I find more examples?

**Documentation:**
- [Quick Start](../../README.md#quick-start) - 5-minute guide
- [Architecture](../../ARCHITECTURE.md) - System design
- [ARRAY_VALUE_GUIDE](../ARRAY_VALUE_GUIDE.md) - Array patterns
- [JSON_V2_ADAPTER](../JSON_V2_ADAPTER.md) - Cross-language JSON

**Examples:**
- `examples/basic_usage.py` - Basic operations
- `examples/advanced_usage.py` - Advanced patterns
- `examples/json_v2_compatibility.py` - Cross-language JSON
- `examples/messagepack_example.py` - MessagePack serialization

**Support:**
- [GitHub Issues](https://github.com/kcenon/python_container_system/issues)
- [GitHub Discussions](https://github.com/kcenon/python_container_system/discussions)

---

**Last Updated:** 2025-11-26
**Next Review:** 2026-02-26
