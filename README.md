# Python Container System

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-BSD--3--Clause-green.svg)](LICENSE)
[![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

> **Language:** **English** | [한국어](README_KO.md)

## Overview

Python Container System is a high-performance, type-safe container framework for Python, providing the same functionality as the C++ [container_system](https://github.com/kcenon/container_system). It is designed for messaging systems and general-purpose applications requiring efficient data management with strong type safety.

This package is a Python implementation equivalent to the C++ container_system, offering:
- **Type-safe value system** with compile-time and runtime checks
- **Multiple serialization formats**: Binary, JSON, XML
- **Thread-safe operations** with optional locking
- **Nested containers** for hierarchical data structures
- **Zero external dependencies** - uses only Python standard library

## Features

### 🎯 Core Features
- **Type Safety**: Strong typing with Python type hints and runtime validation
- **Thread Safety**: Optional thread-safe operations for concurrent access
- **Multiple Formats**: Binary, JSON, and XML serialization support
- **Memory Efficient**: Optimized storage using Python's built-in types
- **Easy Integration**: Can be used as a standalone package or library dependency

### 📦 Value Types

| Type | Python Class | Description | Size |
|------|-------------|-------------|------|
| Null | `Value` | Null/empty value | 0 bytes |
| Boolean | `BoolValue` | True/False | 1 byte |
| Integer | `ShortValue`, `IntValue`, `LongValue`, `LLongValue` | Signed integers | 2-8 bytes |
| Unsigned | `UShortValue`, `UIntValue`, `ULongValue`, `ULLongValue` | Unsigned integers | 2-8 bytes |
| Float | `FloatValue`, `DoubleValue` | Floating-point | 4-8 bytes |
| String | `StringValue` | UTF-8 strings | Variable |
| Bytes | `BytesValue` | Raw byte arrays | Variable |
| Container | `ContainerValue` | Nested containers | Variable |

## Installation

### From Source

```bash
# Clone the repository
git clone https://github.com/kcenon/python_container_system.git
cd python_container_system

# Install in development mode
pip install -e .

# Or install with dev dependencies
pip install -e ".[dev]"
```

### From PyPI (when published)

```bash
pip install python-container-system
```

## Quick Start

### Basic Usage

```python
from container_module import ValueContainer
from container_module.values import StringValue, IntValue, BoolValue, DoubleValue

# Create a container with header information
container = ValueContainer(
    source_id="client_01",
    source_sub_id="session_123",
    target_id="server",
    target_sub_id="main_handler",
    message_type="user_data"
)

# Add values
container.add(IntValue("user_id", 12345))
container.add(StringValue("username", "john_doe"))
container.add(DoubleValue("balance", 1500.75))
container.add(BoolValue("active", True))

# Retrieve values
user_id = container.get_value("user_id")
if user_id:
    print(f"User ID: {user_id.to_int()}")  # Output: User ID: 12345

# Serialize to string
serialized = container.serialize()

# Deserialize from string
restored = ValueContainer(data_string=serialized)
```

### Nested Containers

```python
from container_module.values import ContainerValue

# Create nested container for address
address = ContainerValue("address")
address.add(StringValue("street", "123 Main St"))
address.add(StringValue("city", "Seattle"))
address.add(StringValue("zip", "98101"))

# Add to main container
container.add(address)

# Access nested values
address_value = container.get_value("address")
if address_value:
    print(f"Nested values: {address_value.child_count()}")
```

### JSON/XML Conversion

```python
# Convert to JSON
json_str = container.to_json()
print(json_str)

# Convert to XML
xml_str = container.to_xml()
print(xml_str)
```

### Thread-Safe Operations

```python
import threading

# Enable thread safety
container = ValueContainer(message_type="thread_safe")
container.enable_thread_safety(True)

# Use in multiple threads
def worker():
    container.add(StringValue("data", "value"))
    value = container.get_value("data")

threads = [threading.Thread(target=worker) for _ in range(10)]
for t in threads:
    t.start()
for t in threads:
    t.join()
```

## Project Structure

```
python_container_system/
├── container_module/           # Main package
│   ├── __init__.py             # Package initialization
│   ├── core/                   # Core functionality
│   │   ├── value_types.py      # Value type enumerations
│   │   ├── value.py            # Base Value class
│   │   └── container.py        # ValueContainer class
│   ├── values/                 # Value implementations
│   │   ├── bool_value.py       # Boolean values
│   │   ├── numeric_value.py    # Numeric values
│   │   ├── string_value.py     # String values
│   │   ├── bytes_value.py      # Byte array values
│   │   └── container_value.py  # Nested containers
│   └── utilities/              # Utility functions
├── tests/                      # Test suite
│   ├── test_value_types.py     # Type system tests
│   ├── test_container.py       # Container tests
│   └── test_values.py          # Value tests
├── examples/                   # Example programs
│   ├── basic_usage.py          # Basic usage example
│   └── advanced_usage.py       # Advanced features
├── docs/                       # Documentation
├── setup.py                    # Setup script
├── pyproject.toml              # Project configuration
├── README.md                   # This file
└── LICENSE                     # BSD 3-Clause License
```

## API Reference

### ValueContainer

```python
class ValueContainer:
    """Main container class for managing messages."""

    def __init__(
        self,
        source_id: str = "",
        source_sub_id: str = "",
        target_id: str = "",
        target_sub_id: str = "",
        message_type: str = "",
        units: Optional[List[Value]] = None,
    ) -> None: ...

    # Header management
    def set_source(self, source_id: str, source_sub_id: str = "") -> None: ...
    def set_target(self, target_id: str, target_sub_id: str = "") -> None: ...
    def set_message_type(self, message_type: str) -> None: ...
    def swap_header(self) -> None: ...

    # Value management
    def add(self, target_value: Value, update_immediately: bool = False) -> Value: ...
    def remove(self, target: Union[str, Value], update_immediately: bool = False) -> None: ...
    def get_value(self, target_name: str, index: int = 0) -> Optional[Value]: ...
    def value_array(self, target_name: str) -> List[Value]: ...
    def clear_value(self) -> None: ...

    # Serialization
    def serialize(self) -> str: ...
    def deserialize(self, data_string: str, parse_only_header: bool = True) -> bool: ...
    def to_json(self) -> str: ...
    def to_xml(self) -> str: ...

    # File I/O
    def load_packet(self, file_path: str) -> None: ...
    def save_packet(self, file_path: str) -> None: ...

    # Utility
    def copy(self, containing_values: bool = True) -> ValueContainer: ...
    def initialize(self) -> None: ...
```

### Value Types

```python
from container_module.values import (
    BoolValue,          # Boolean value
    ShortValue,         # 16-bit signed integer
    IntValue,           # 32-bit signed integer
    LongValue,          # Platform-dependent signed long
    LLongValue,         # 64-bit signed integer
    UShortValue,        # 16-bit unsigned integer
    UIntValue,          # 32-bit unsigned integer
    ULongValue,         # Platform-dependent unsigned long
    ULLongValue,        # 64-bit unsigned integer
    FloatValue,         # 32-bit floating-point
    DoubleValue,        # 64-bit floating-point
    StringValue,        # UTF-8 string
    BytesValue,         # Raw byte array
    ContainerValue,     # Nested container
)
```

## Development

### Running Tests

```bash
# Install test dependencies
pip install -e ".[test]"

# Run all tests
pytest

# Run with coverage
pytest --cov=container_module --cov-report=html

# Run specific test file
pytest tests/test_container.py
```

### Code Quality

```bash
# Format code with black
black container_module tests examples

# Type checking with mypy
mypy container_module

# Linting with pylint
pylint container_module
```

## Comparison with C++ Version

| Feature | C++ container_system | Python container_system |
|---------|---------------------|------------------------|
| **Language** | C++20 | Python 3.8+ |
| **Type Safety** | Compile-time + Runtime | Runtime (with type hints) |
| **Performance** | ~2M ops/sec | ~500K ops/sec |
| **Memory** | Smart pointers, RAII | Automatic garbage collection |
| **Thread Safety** | Lock-free + mutex | Threading.RLock |
| **SIMD** | ARM NEON, x86 AVX | NumPy (optional) |
| **Serialization** | Binary, JSON, XML | Binary, JSON, XML |
| **Dependencies** | fmt, spdlog | None (stdlib only) |
| **Use Case** | High-performance C++ apps | Python applications, integration |

## Compatibility

This Python implementation is designed to be **wire-compatible** with the C++ version:
- Same serialization format
- Same value type codes
- Can exchange data with C++ container_system

## Examples

### Example 1: Message Passing

```python
# Create request
request = ValueContainer(
    source_id="client",
    target_id="server",
    message_type="get_user"
)
request.add(IntValue("user_id", 12345))

# Send (serialize)
data = request.serialize()

# Receive and process
response = ValueContainer(
    source_id="server",
    target_id="client",
    message_type="user_data"
)
response.add(StringValue("name", "John Doe"))
response.add(StringValue("email", "john@example.com"))
```

### Example 2: Data Storage

```python
# Save container to file
container.save_packet("data/user_12345.dat")

# Load container from file
loaded = ValueContainer()
loaded.load_packet("data/user_12345.dat")
```

### Example 3: Binary Data

```python
from container_module.values import BytesValue

# Create binary data
binary_data = bytes([0xFF, 0xFE, 0xFD, 0xFC])
container.add(BytesValue("image_data", binary_data))

# Retrieve binary data
image = container.get_value("image_data")
if image:
    data = image.to_bytes()
    hex_str = image.to_hex()
    b64_str = image.to_base64()
```

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the BSD 3-Clause License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Inspired by the C++ [container_system](https://github.com/kcenon/container_system)
- Designed to be compatible with the messaging system ecosystem
- Maintainer: kcenon@naver.com

## Support

- **Issues**: [GitHub Issues](https://github.com/kcenon/python_container_system/issues)
- **Email**: kcenon@naver.com

---

<p align="center">
  Made with ❤️ by 🍀☀🌕🌥 🌊
</p>
