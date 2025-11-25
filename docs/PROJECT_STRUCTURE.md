# Python Container System Project Structure

**Last Updated**: 2025-11-26

## Overview

This document provides comprehensive information about the Python Container System project structure, including directory organization, file descriptions, module dependencies, and installation artifacts.

## Directory Tree

```
python_container_system/
├── 📁 container_module/           # Main package
│   ├── __init__.py                # Package initialization
│   ├── py.typed                   # Type stub marker
│   ├── 📁 core/                   # Core functionality
│   │   ├── __init__.py            # Core module exports
│   │   ├── value_types.py         # Value type enumerations
│   │   ├── value.py               # Abstract Value base class
│   │   └── container.py           # ValueContainer class
│   ├── 📁 values/                 # Value implementations
│   │   ├── __init__.py            # Value exports
│   │   ├── bool_value.py          # Boolean values
│   │   ├── numeric_value.py       # Numeric values (10 types)
│   │   ├── string_value.py        # String values
│   │   ├── bytes_value.py         # Byte array values
│   │   ├── container_value.py     # Nested containers
│   │   └── array_value.py         # Homogeneous arrays
│   ├── 📁 utilities/              # Utility functions
│   │   └── __init__.py            # Utility exports
│   ├── 📁 adapters/               # Cross-language adapters
│   │   ├── __init__.py            # Adapter exports
│   │   └── json_v2_adapter.py     # JSON v2.0 adapter
│   └── 📁 serializers/            # Serialization modules
│       ├── __init__.py            # Serializer exports
│       └── messagepack_serializer.py  # MessagePack serializer
├── 📁 tests/                      # Test suite
│   ├── test_value_types.py        # Type system tests
│   ├── test_container.py          # Container tests
│   ├── test_values.py             # Value tests
│   ├── test_thread_safety.py      # Threading tests
│   ├── test_edge_cases.py         # Edge case tests
│   ├── test_long_range_checking.py  # Range validation tests
│   └── run_edge_case_tests.py     # Simple test runner
├── 📁 examples/                   # Example programs
│   ├── basic_usage.py             # Basic usage example
│   ├── advanced_usage.py          # Advanced features
│   ├── array_value_example.py     # Array value usage
│   └── messagepack_example.py     # MessagePack serialization
├── 📁 benchmarks/                 # Performance benchmarks
│   ├── performance_benchmark.py   # Benchmark script
│   └── PERFORMANCE_REPORT.md      # Benchmark results
├── 📁 docs/                       # Documentation
│   ├── README.md                  # Documentation index
│   ├── FEATURES.md                # Feature documentation
│   ├── API_REFERENCE.md           # API reference
│   ├── PROJECT_STRUCTURE.md       # This file
│   ├── ARCHITECTURE.md            # Architecture (link to root)
│   ├── CHANGELOG.md               # Changelog (link to root)
│   ├── ARRAY_VALUE_GUIDE.md       # ArrayValue guide
│   ├── JSON_V2_ADAPTER.md         # JSON v2.0 guide
│   ├── 📁 guides/                 # User guides
│   │   ├── FAQ.md                 # Frequently asked questions
│   │   └── TROUBLESHOOTING.md     # Troubleshooting guide
│   ├── 📁 contributing/           # Contribution docs
│   │   └── TESTING.md             # Testing guide
│   └── 📁 performance/            # Performance docs
│       └── BENCHMARKS.md          # Performance benchmarks
├── 📄 setup.py                    # Setup script
├── 📄 pyproject.toml              # Project configuration
├── 📄 MANIFEST.in                 # Package manifest
├── 📄 README.md                   # Main README
├── 📄 README_KO.md                # Korean README
├── 📄 ARCHITECTURE.md             # Architecture documentation
├── 📄 CHANGELOG.md                # Version history
├── 📄 CONTRIBUTING.md             # Contribution guidelines
├── 📄 PROJECT_SUMMARY.md          # Implementation summary
├── 📄 ENHANCEMENTS_SUMMARY.md     # Enhancement summary
├── 📄 LICENSE                     # BSD 3-Clause License
└── 📄 .gitignore                  # Git ignore rules
```

## Core Module Files

### Package Root (`container_module/`)

#### `__init__.py`
**Purpose**: Package initialization and public API exports

**Exports**:
- `ValueContainer` - Main container class
- `Value` - Abstract base class
- `ValueTypes` - Type enumerations
- All value classes (BoolValue, IntValue, StringValue, etc.)

**Example**:
```python
from container_module import ValueContainer
from container_module.values import IntValue, StringValue
```

#### `py.typed`
**Purpose**: PEP 561 marker for type stub support

**Content**: Empty file indicating this package includes type hints

### Core Layer (`container_module/core/`)

#### `value_types.py`
**Purpose**: Value type enumerations and type utilities

**Key Features**:
- `ValueTypes` IntEnum with 16 value types
- Type conversion utilities
- Type checking functions (is_numeric_type, is_integer_type)
- String-to-type and type-to-string mapping

**Example**:
```python
from container_module.core import ValueTypes

assert ValueTypes.INT_VALUE == 4
assert ValueTypes.STRING_VALUE == 14
```

#### `value.py`
**Purpose**: Abstract base class for all value types

**Key Features**:
- ABC (Abstract Base Class) definition
- Type conversion methods (to_int, to_string, to_bytes, etc.)
- Properties for read-only attributes
- Duck typing support with `__getitem__`

**Public Interface**:
```python
from abc import ABC, abstractmethod

class Value(ABC):
    @property
    def name(self) -> str: ...

    @property
    def type(self) -> ValueTypes: ...

    @abstractmethod
    def serialize(self) -> str: ...

    def to_int(self) -> int: ...
    def to_string(self) -> str: ...
```

#### `container.py`
**Purpose**: Main container class for managing values

**Key Features**:
- Header management (source, target, message_type)
- Value storage with list-based lookup
- Serialization/deserialization support
- Optional thread safety with RLock
- File I/O operations

**Public Interface**:
```python
class ValueContainer:
    # Properties
    @property
    def source_id(self) -> str: ...
    @property
    def target_id(self) -> str: ...
    @property
    def message_type(self) -> str: ...

    # Value management
    def add(self, target_value: Value) -> Value: ...
    def get_value(self, target_name: str, index: int = 0) -> Optional[Value]: ...
    def remove(self, target: Union[str, Value]) -> None: ...

    # Serialization
    def serialize(self) -> str: ...
    def deserialize(self, data_string: str) -> bool: ...
    def to_json(self) -> str: ...
    def to_xml(self) -> str: ...

    # File I/O
    def save_to_file(self, file_path: str) -> None: ...
    def load_from_file(self, file_path: str) -> None: ...
```

### Value Implementations (`container_module/values/`)

#### `bool_value.py`
**Purpose**: Boolean value implementation

**Features**:
- True/False storage
- Conversion to int (1/0)
- Binary serialization (1 byte)

#### `numeric_value.py`
**Purpose**: All numeric value types

**Implemented Types**:
- `ShortValue` (i16), `UShortValue` (u16)
- `IntValue` (i32), `UIntValue` (u32)
- `LongValue` (i32 for C++ compat), `ULongValue` (u32 for C++ compat)
- `LLongValue` (i64), `ULLongValue` (u64)
- `FloatValue` (f32), `DoubleValue` (f64)

**Key Features**:
- struct module for binary packing
- Factory methods (from_string, from_data)
- Range validation for long types
- Type conversions with overflow checking

**Example**:
```python
import struct

class IntValue(NumericValue):
    def __init__(self, name: str, value: int):
        data = struct.pack("i", value)  # Little-endian int32
        super().__init__(name, ValueTypes.INT_VALUE, data)
```

#### `string_value.py`
**Purpose**: UTF-8 string value implementation

**Features**:
- Native UTF-8 encoding/decoding
- Escape handling for serialization
- Immutable string storage

#### `bytes_value.py`
**Purpose**: Binary data value implementation

**Features**:
- Hex encoding/decoding
- Base64 encoding/decoding
- Raw byte storage
- Factory methods (from_hex, from_base64)

#### `container_value.py`
**Purpose**: Nested container support

**Features**:
- Recursive serialization
- Child value management
- Parent-child relationship tracking
- Query by name with filtering

#### `array_value.py`
**Purpose**: Homogeneous array support

**Features**:
- Type validation for elements
- Efficient array storage
- Integration with JSON v2.0 format
- Index-based access

### Adapters (`container_module/adapters/`)

#### `json_v2_adapter.py`
**Purpose**: Cross-language JSON adapter

**Features**:
- JSON v2.0 format support
- Array serialization
- Type-safe conversion
- Bidirectional conversion (to/from JSON)

**Public Interface**:
```python
class JSONv2Adapter:
    @staticmethod
    def to_json(container: ValueContainer) -> str: ...

    @staticmethod
    def from_json(json_str: str) -> ValueContainer: ...

    @staticmethod
    def to_dict(container: ValueContainer) -> dict: ...

    @staticmethod
    def from_dict(data: dict) -> ValueContainer: ...
```

### Serializers (`container_module/serializers/`)

#### `messagepack_serializer.py`
**Purpose**: Pure Python MessagePack serialization

**Features**:
- Zero dependencies
- Full MessagePack spec support
- Compact binary format
- Fast serialization (2.5M ops/sec)

**Public Interface**:
```python
class MessagePackSerializer:
    @staticmethod
    def container_to_msgpack(container: ValueContainer) -> bytes: ...

    @staticmethod
    def msgpack_to_container(data: bytes) -> ValueContainer: ...
```

## Test Organization

### Unit Tests (`tests/`)

**Coverage**: Core functionality, individual components

**Key Tests**:
- `test_value_types.py`: Type system and enumerations
- `test_container.py`: Container operations and header management
- `test_values.py`: All value type implementations
- `test_thread_safety.py`: Concurrent access patterns
- `test_edge_cases.py`: Boundary conditions and edge cases
- `test_long_range_checking.py`: Range validation for long types

**Test Framework**: pytest
**Total Test Cases**: 150+

### Example Programs (`examples/`)

**Purpose**: Demonstrate usage patterns

**Programs**:
- `basic_usage.py`: Core functionality (141 lines)
- `advanced_usage.py`: Advanced features (285 lines)
- `array_value_example.py`: Array value usage
- `messagepack_example.py`: MessagePack serialization

### Performance Benchmarks (`benchmarks/`)

**Purpose**: Performance measurement and optimization

**Files**:
- `performance_benchmark.py`: Benchmark script
- `PERFORMANCE_REPORT.md`: Results and analysis

## Module Dependencies

### Internal Dependencies

```
Python Standard Library (no external dependencies)
    │
    └──> container_module.core (value_types, value, container)
            │
            ├──> container_module.values (all value implementations)
            │      │
            │      └──> container_module.adapters (json_v2_adapter)
            │
            └──> container_module.serializers (messagepack_serializer)
```

### Standard Library Dependencies

| Module | Purpose | Used By |
|--------|---------|---------|
| **abc** | Abstract base classes | Value base class |
| **struct** | Binary packing | Numeric values |
| **json** | JSON serialization | Container, JSONv2Adapter |
| **xml.etree.ElementTree** | XML serialization | Container |
| **threading** | Thread safety | Container (RLock) |
| **base64** | Base64 encoding | BytesValue |
| **binascii** | Hex encoding | BytesValue |
| **pathlib** | File operations | Container |
| **typing** | Type hints | All modules |

### No External Dependencies

The Python Container System uses **only the Python standard library**:
- ✅ Zero external dependencies for core functionality
- ✅ pytest only for testing (optional)
- ✅ No C extensions required
- ✅ Pure Python implementation

## Installation Artifacts

### Development Installation

```bash
pip install -e .
```

**Result**:
```
python_container_system.egg-info/
├── PKG-INFO
├── SOURCES.txt
├── dependency_links.txt
├── requires.txt
└── top_level.txt
```

### Distribution Build

```bash
python setup.py sdist bdist_wheel
```

**Result**:
```
dist/
├── python_container_system-1.1.0.tar.gz          # Source distribution
└── python_container_system-1.1.0-py3-none-any.whl  # Wheel distribution
```

### Installed Package

```bash
pip install python_container_system
```

**Location**: `site-packages/container_module/`

## File Naming Conventions

### Python Files
- **Modules**: `snake_case.py` (e.g., `value_types.py`)
- **Classes**: `PascalCase` (e.g., `ValueContainer`)
- **Functions**: `snake_case` (e.g., `get_value`)
- **Constants**: `UPPER_SNAKE_CASE` (e.g., `VERSION`)

### Documentation Files
- **Markdown**: `UPPERCASE.md` (e.g., `README.md`)
- **Korean Translation**: `UPPERCASE_KO.md` (e.g., `README_KO.md`)
- **Guides**: `lowercase.md` in `docs/guides/`

### Test Files
- **Unit Tests**: `test_<module>.py` (e.g., `test_container.py`)
- **Test Runner**: `run_<test_type>_tests.py`

## Code Organization Best Practices

### Import Organization

```python
# Standard library imports
import struct
import json
from typing import List, Optional, Union

# Package imports
from container_module.core import Value, ValueTypes
from container_module.values import IntValue, StringValue

# Local imports (if any)
from .utilities import helper_function
```

### Module Structure

```python
"""Module docstring describing purpose and usage.

Example:
    from container_module import ValueContainer
    container = ValueContainer(message_type="example")
"""

# Imports
from typing import List, Optional

# Constants
VERSION = "1.1.0"

# Classes
class MyClass:
    """Class docstring with examples."""
    pass

# Functions
def my_function():
    """Function docstring."""
    pass

# Module-level code (if any)
if __name__ == "__main__":
    # Test code
    pass
```

### Type Hints

```python
from typing import List, Optional, Union

def process_values(
    values: List[Value],
    filter_type: Optional[ValueTypes] = None
) -> Union[List[Value], None]:
    """
    Process values with optional filtering.

    Args:
        values: List of values to process
        filter_type: Optional type filter

    Returns:
        Filtered list or None if empty

    Example:
        >>> values = [IntValue("a", 1), StringValue("b", "text")]
        >>> result = process_values(values, ValueTypes.INT_VALUE)
    """
    if filter_type:
        return [v for v in values if v.type == filter_type]
    return values if values else None
```

### File Size Guidelines
- **Module Files**: <800 lines
- **Test Files**: <600 lines per module
- **Example Files**: <300 lines
- **Documentation**: No strict limit, but break into sections

## Package Configuration

### `setup.py`

```python
from setuptools import setup, find_packages

setup(
    name="python-container-system",
    version="1.1.0",
    packages=find_packages(exclude=["tests", "examples", "benchmarks"]),
    python_requires=">=3.8",
    install_requires=[],  # No dependencies
    extras_require={
        "dev": ["pytest>=7.0", "pytest-cov", "black", "mypy"],
        "test": ["pytest>=7.0", "pytest-cov"],
    },
)
```

### `pyproject.toml`

```toml
[build-system]
requires = ["setuptools>=45", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "python-container-system"
version = "1.1.0"
description = "Type-safe container system for Python"
readme = "README.md"
requires-python = ">=3.8"
license = {text = "BSD-3-Clause"}

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = "test_*.py"

[tool.black]
line-length = 88
target-version = ['py38']
```

## Platform Support

| Platform | Status | Notes |
|----------|--------|-------|
| **Linux** | ✅ Full | All distributions with Python 3.8+ |
| **macOS** | ✅ Full | x86_64 and ARM64 (Apple Silicon) |
| **Windows** | ✅ Full | Windows 10+ with Python 3.8+ |
| **Python Versions** | 3.8, 3.9, 3.10, 3.11, 3.12, 3.13+ | Tested on all versions |

## See Also

- [FEATURES.md](FEATURES.md) - Complete feature documentation
- [API_REFERENCE.md](API_REFERENCE.md) - API documentation
- [ARCHITECTURE.md](ARCHITECTURE.md) - Architecture guide
- [CHANGELOG.md](CHANGELOG.md) - Version history
- [guides/FAQ.md](guides/FAQ.md) - Frequently asked questions

---

**Last Updated**: 2025-11-26
**Version**: 1.1.0
