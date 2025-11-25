# Python Container System Features

**Last Updated**: 2025-11-26

## Overview

This document provides comprehensive details about all features and capabilities of the Python Container System, including value types, serialization formats, advanced features, and integration capabilities.

## Core Capabilities

### Type Safety
- **Strongly-typed value system** with runtime checks
- **Type hints throughout** for static analysis support
- **ABC-based design** with consistent interfaces
- **Type validation** at construction and deserialization
- **Runtime type checking** with isinstance()

### Thread Safety
- **Optional thread-safe operations** via `enable_thread_safety()`
- **RLock-based synchronization** for concurrent write scenarios
- **Concurrent read access** - multiple threads can safely read simultaneously
- **Zero overhead when disabled** - dummy lock pattern
- **GIL-aware design** - optimized for Python's threading model

### Memory Efficiency
- **Automatic garbage collection** - no manual memory management
- **Reference counting** for predictable cleanup
- **List-based storage** with efficient append operations
- **Move semantics** via Python's reference sharing
- **Memory profiling** tools integrated

### Serialization Formats
- **Binary format** - high-performance with C++ compatibility
- **JSON format** - human-readable with type information
- **JSON v2.0** - enhanced cross-language compatibility
- **XML format** - legacy system support
- **MessagePack** - compact binary format (zero dependencies)
- **Automatic format detection** for deserialization

## Value Types

The Python Container System supports 16 distinct value types covering all common data scenarios:

### Primitive Types

| Type | Python Class | Size | Description |
|------|-------------|------|-------------|
| `null_value` | `Value` | 0 bytes | Null/empty value, represents absence of data |
| `bool_value` | `BoolValue` | 1 byte | Boolean true/false |

### Integer Types

| Type | Python Class | Size | Range |
|------|-------------|------|-------|
| `short_value` | `ShortValue` | 2 bytes | -32,768 to 32,767 |
| `ushort_value` | `UShortValue` | 2 bytes | 0 to 65,535 |
| `int_value` | `IntValue` | 4 bytes | -2³¹ to 2³¹-1 |
| `uint_value` | `UIntValue` | 4 bytes | 0 to 2³²-1 |
| `long_value` | `LongValue` | 4 bytes* | -2³¹ to 2³¹-1 |
| `ulong_value` | `ULongValue` | 4 bytes* | 0 to 2³²-1 |
| `llong_value` | `LLongValue` | 8 bytes | -2⁶³ to 2⁶³-1 |
| `ullong_value` | `ULLongValue` | 8 bytes | 0 to 2⁶⁴-1 |

*LongValue/ULongValue are 32-bit for cross-platform C++ compatibility

### Floating-Point Types

| Type | Python Class | Size | Precision |
|------|-------------|------|-----------|
| `float_value` | `FloatValue` | 4 bytes | ~7 decimal digits |
| `double_value` | `DoubleValue` | 8 bytes | ~15 decimal digits |

### Complex Types

| Type | Python Class | Size | Description |
|------|-------------|------|-------------|
| `bytes_value` | `BytesValue` | Variable | Raw byte array, binary data |
| `container_value` | `ContainerValue` | Variable | Nested container for hierarchical data |
| `string_value` | `StringValue` | Variable | UTF-8 encoded string |
| `array_value` | `ArrayValue` | Variable | Homogeneous arrays of values |

### Value Type Usage Examples

```python
from container_module import ValueContainer
from container_module.values import (
    BoolValue, IntValue, LongValue, LLongValue,
    FloatValue, DoubleValue, StringValue, BytesValue,
    ContainerValue, ArrayValue
)

# Primitive types
bool_val = BoolValue("is_active", True)
null_val = Value()  # Null value

# Integer types
int_val = IntValue("count", 42)
long_val = LongValue("timestamp", 1234567890)  # 32-bit for C++ compatibility
llong_val = LLongValue("large_number", 5000000000)  # Use for values > 2³¹

# Floating-point types
float_val = FloatValue("pi_approx", 3.14159)
double_val = DoubleValue("price", 99.99)

# Complex types
bytes_val = BytesValue("data", b"\x00\x01\x02\x03")
string_val = StringValue("name", "John Doe")

# Array values
array_val = ArrayValue("scores")
array_val.add(IntValue("", 95))
array_val.add(IntValue("", 87))
array_val.add(IntValue("", 92))

# Nested container
address = ContainerValue("address")
address.add(StringValue("street", "123 Main St"))
address.add(StringValue("city", "Seattle"))
address.add(StringValue("zip", "98101"))
```

## Enhanced Features

### JSON v2.0 Adapter
- **Cross-language compatibility** with C++, .NET, Go implementations
- **Type-safe serialization** with explicit type information
- **Array support** for homogeneous collections
- **Enhanced error handling** with detailed error messages
- **Bidirectional conversion** between JSON and containers

```python
from container_module.adapters import JSONv2Adapter

# Serialize to JSON v2.0 format
container = ValueContainer(message_type="user_data")
container.add(StringValue("name", "Alice"))
container.add(IntValue("age", 30))

json_str = JSONv2Adapter.to_json(container)

# Deserialize from JSON v2.0 format
restored = JSONv2Adapter.from_json(json_str)
```

### MessagePack Serialization
- **Zero dependencies** - pure Python implementation
- **Compact binary format** - 50% smaller than JSON
- **Fast performance** - 2.5M ops/sec
- **Cross-platform** compatible
- **Full spec support** - integers, floats, strings, binary, arrays, maps

```python
from container_module.serializers import MessagePackSerializer

# Serialize to MessagePack
msgpack_data = MessagePackSerializer.container_to_msgpack(container)

# Deserialize from MessagePack
restored = MessagePackSerializer.msgpack_to_container(msgpack_data)
```

### Array Values
- **Homogeneous collections** of same-type values
- **Efficient storage** for numeric arrays
- **Type validation** ensures consistency
- **Nested arrays** supported
- **Integration with NumPy** (optional)

```python
# Create an array of integers
scores = ArrayValue("test_scores")
for score in [95, 87, 92, 88, 94]:
    scores.add(IntValue("", score))

container.add(scores)

# Access array elements
array = container.get_value("test_scores")
for i in range(array.child_count()):
    score = array.get_child(i)
    print(f"Score {i+1}: {score.to_int()}")
```

### Properties for Clean API
- **Pythonic attribute access** with @property decorators
- **Read-only attributes** for immutable data
- **No getter methods** - direct attribute syntax
- **Type-safe access** with type hints

```python
# Clean property access (Pythonic)
container = ValueContainer(source_id="client", target_id="server")
print(container.source_id)  # Direct access
print(container.message_type)

# vs C++ style (not used)
# print(container.get_source_id())  # Verbose
```

### Context Managers
- **Resource safety** with automatic cleanup
- **Exception-safe** file operations
- **RAII-like patterns** for Python

```python
from pathlib import Path

# Context manager for file operations
def save_to_file(container, path):
    with Path(path).open('wb') as f:
        f.write(container.serialize_array())
    # File automatically closed, even on exception
```

## Technology Stack

### Pure Python Foundation
- **Python 3.8+ compatibility** - modern Python features
- **Type hints throughout** - PEP 484 compliance
- **ABC-based design** - abstract base classes for interfaces
- **No external dependencies** - uses only standard library
- **Zero compilation** - instant execution

### Standard Library Usage
- **struct module** - binary packing for C++ compatibility
- **json module** - JSON serialization
- **xml.etree.ElementTree** - XML serialization
- **threading.RLock** - thread safety
- **abc module** - abstract base classes

### Design Patterns
- **Factory Pattern** - Value creation methods
- **Abstract Factory** - Type-specific value factories
- **Template Method Pattern** - Serialization framework
- **Strategy Pattern** - Multiple serialization formats
- **EAFP Pattern** - Easier to Ask Forgiveness than Permission
- **Duck Typing** - Flexible interfaces

## Advanced Capabilities

### Nested Containers
```python
# Create hierarchical data structures
root = ValueContainer(message_type="order")

customer = ContainerValue("customer")
customer.add(StringValue("name", "Alice"))
customer.add(StringValue("email", "alice@example.com"))

address = ContainerValue("address")
address.add(StringValue("street", "123 Main St"))
address.add(StringValue("city", "Seattle"))
customer.add(address)

root.add(customer)
```

### Thread-Safe Operations
```python
import threading

# Enable thread safety
container = ValueContainer()
container.enable_thread_safety(True)

def worker(thread_id):
    # Thread-safe add
    container.add(IntValue(f"thread_{thread_id}", thread_id))
    # Thread-safe read
    value = container.get_value(f"thread_{thread_id}")

threads = [threading.Thread(target=worker, args=(i,)) for i in range(4)]
for t in threads:
    t.start()
for t in threads:
    t.join()
```

### Multiple Serialization Formats
```python
# Binary format (fastest, most compact)
binary_data = container.serialize()

# JSON format (human-readable)
json_str = container.to_json()

# JSON v2.0 (cross-language compatible)
from container_module.adapters import JSONv2Adapter
json_v2 = JSONv2Adapter.to_json(container)

# XML format (legacy systems)
xml_str = container.to_xml()

# MessagePack (compact binary)
from container_module.serializers import MessagePackSerializer
msgpack_data = MessagePackSerializer.container_to_msgpack(container)
```

## Real-World Use Cases

### Financial Trading System
```python
from container_module import ValueContainer
from container_module.values import StringValue, DoubleValue, IntValue, LLongValue
import time

# Market data tick
market_data = ValueContainer(
    source_id="trading_engine",
    source_sub_id="session_001",
    target_id="risk_monitor",
    target_sub_id="main",
    message_type="market_tick"
)

market_data.add(StringValue("symbol", "AAPL"))
market_data.add(DoubleValue("price", 175.50))
market_data.add(IntValue("volume", 1000000))
market_data.add(DoubleValue("bid", 175.48))
market_data.add(DoubleValue("ask", 175.52))
market_data.add(LLongValue("timestamp", int(time.time() * 1000000)))

# High-frequency serialization
data = market_data.serialize()  # ~400K ops/sec
```

### IoT Sensor Data
```python
# Environmental sensor reading
sensor_reading = ValueContainer(
    source_id="sensor_array",
    source_sub_id="building_A_floor_3",
    message_type="environmental_reading"
)

# Temperature readings array
temps = ArrayValue("temperature_readings")
for temp in [22.5, 23.1, 22.8, 23.3]:
    temps.add(DoubleValue("", temp))
sensor_reading.add(temps)

# Humidity readings array
humidity = ArrayValue("humidity_readings")
for h in [45, 47, 46, 48]:
    humidity.add(IntValue("", h))
sensor_reading.add(humidity)

# Save to file
sensor_reading.save_to_file("sensor_data.bin")
```

### Web API Response
```python
# API response container
api_response = ValueContainer(message_type="api_response")
api_response.add(IntValue("status", 200))
api_response.add(BoolValue("success", True))

# Nested data
data = ContainerValue("data")
data.add(IntValue("user_id", 12345))
data.add(StringValue("username", "john_doe"))
data.add(StringValue("email", "john@example.com"))
api_response.add(data)

# JSON serialization for HTTP response
json_response = api_response.to_json()
```

### Database Storage
```python
# Create database record
record = ValueContainer(message_type="user_record")
record.add(LLongValue("id", 12345))
record.add(StringValue("username", "alice"))
record.add(DoubleValue("balance", 1500.75))
record.add(BoolValue("active", True))

# Compact binary format for BLOB storage
blob_data = record.serialize_array()  # bytes
# Store blob_data in database BLOB field
```

## Performance Characteristics

### Value Operations Performance

| Operation | Throughput (ops/s) | Notes |
|-----------|-------------------|-------|
| **BoolValue creation** | 5.0M | Fastest basic type |
| **IntValue creation** | 3.9M | Includes struct packing |
| **StringValue creation** | 5.0M | UTF-8 encoding |
| **BytesValue creation** | 5.7M | Minimal processing |

### Container Operations Performance

| Operation | Throughput (ops/s) | Latency (µs) |
|-----------|-------------------|--------------|
| **Container creation (8 values)** | 174K | 5.7 |
| **get_value() lookup** | 1.7M | 0.6 |
| **add() operation** | 3M+ | 0.3 |

### Serialization Performance

| Format | Throughput (ops/s) | Size Overhead | Best Use Case |
|--------|-------------------|---------------|---------------|
| **Binary** | 6.7M | 100% (baseline) | High-performance, network transmission |
| **MessagePack** | 2.5M | 149% | Cross-platform binary, compact |
| **JSON** | 50K | 293% | Human-readable, debugging, APIs |
| **XML** | 16K | 195% | Legacy integration |

### Memory Characteristics

| Component | Memory Usage | Notes |
|-----------|--------------|-------|
| Empty Container | ~600 bytes | Python object overhead |
| String Value | ~450 bytes + length | Includes Python object overhead |
| Numeric Value | ~420 bytes | Fixed-size allocation |
| Nested Container | Recursive | Sum of all child containers |

### Performance Comparison

| Platform | Implementation | Throughput | Notes |
|----------|---------------|------------|-------|
| Python | This implementation | 400K ops/sec | Pure Python |
| C++ | container_system | 2M ops/sec | Native code, SIMD |
| Ratio | C++/Python | 5x | Expected for interpreted language |

## Error Handling

### Exception-Based Approach

The Python Container System uses Python's exception system:

```python
# EAFP: Easier to Ask for Forgiveness than Permission
try:
    value = container.get_value("user_id")
    user_id = value.to_int()
except AttributeError:
    # Value not found (None)
    user_id = 0
except ValueError as e:
    # Type conversion failed
    print(f"Error: {e}")
    user_id = 0
```

### Error Categories

| Category | Exception Type | Examples |
|----------|---------------|----------|
| Type Errors | `TypeError` | Wrong type passed to function |
| Value Errors | `ValueError` | Invalid value or conversion |
| Attribute Errors | `AttributeError` | Method doesn't exist (duck typing) |
| Overflow Errors | `OverflowError` | Numeric range exceeded |

### Safe Type Conversion

```python
class Value:
    def _safe_convert(self, type_name: str, default_value):
        """
        Safe conversion with null checking.

        Raises:
            ValueError: If trying to convert from null_value
        """
        if self._type == ValueTypes.NULL_VALUE:
            raise ValueError(f"Cannot convert null_value to {type_name}")
        return default_value
```

## Cross-Language Compatibility

### Wire Format Compatibility

The Python implementation maintains **wire-format compatibility** with other implementations:

```python
# Python serializes
container = ValueContainer(source_id="python", target_id="cpp")
container.add(IntValue("user_id", 12345))
data = container.serialize()

# C++ can deserialize the same format
# .NET can deserialize the same format
# Go can deserialize the same format
```

### Type Code Compatibility

| Type | Code | C++ | Python | .NET | Go | Rust |
|------|------|-----|--------|------|----|----|
| int32 | 4 | `int32_t` | `IntValue` | `int` | `int32` | `i32` |
| string | 14 | `std::string` | `StringValue` | `string` | `string` | `String` |
| container | 15 | `container` | `ContainerValue` | `Container` | `Container` | `Container` |

## Integration Capabilities

### With Other Python Libraries

```python
# NumPy integration (optional)
import numpy as np

# Convert array to NumPy
scores = [95, 87, 92, 88, 94]
array_val = ArrayValue("scores")
for s in scores:
    array_val.add(IntValue("", s))

# Extract to NumPy array (manual)
np_array = np.array([child.to_int() for child in array_val.children()])

# Pandas integration
import pandas as pd

# Convert container to DataFrame
data = {
    "name": container.get_value("name").to_string(),
    "age": container.get_value("age").to_int(),
    "balance": container.get_value("balance").to_double()
}
df = pd.DataFrame([data])
```

### With Web Frameworks

```python
# Flask integration
from flask import Flask, request, jsonify
from container_module import ValueContainer
from container_module.adapters import JSONv2Adapter

app = Flask(__name__)

@app.route('/api/user', methods=['POST'])
def create_user():
    # Parse JSON v2.0 from request
    container = JSONv2Adapter.from_json(request.get_json())

    # Process container
    name = container.get_value("name").to_string()
    age = container.get_value("age").to_int()

    # Return JSON v2.0 response
    response = ValueContainer(message_type="user_created")
    response.add(StringValue("status", "success"))
    response.add(IntValue("user_id", 12345))

    return jsonify(JSONv2Adapter.to_dict(response))
```

### With Message Queues

```python
# RabbitMQ integration
import pika

# Send container via RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

container = ValueContainer(message_type="task")
container.add(StringValue("action", "process"))

# Serialize to binary
data = container.serialize_array()
channel.basic_publish(exchange='', routing_key='task_queue', body=data)

# Receive and deserialize
def callback(ch, method, properties, body):
    container = ValueContainer(data_string=body.decode('utf-8'))
    action = container.get_value("action").to_string()
    print(f"Processing: {action}")

channel.basic_consume(queue='task_queue', on_message_callback=callback)
```

## See Also

- [API_REFERENCE.md](API_REFERENCE.md) - Complete API documentation
- [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) - File organization and dependencies
- [ARCHITECTURE.md](ARCHITECTURE.md) - Architecture and design patterns
- [CHANGELOG.md](CHANGELOG.md) - Version history
- [performance/BENCHMARKS.md](performance/BENCHMARKS.md) - Performance benchmarks

---

**Last Updated**: 2025-11-26
**Version**: 1.1.0
