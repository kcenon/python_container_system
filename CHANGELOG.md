# Changelog

All notable changes to the Python Container System project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

> **Language:** **English** | [한국어](CHANGELOG_KO.md)

---

## [Unreleased]

### Planned
- NumPy integration for efficient array operations
- Async/await support for non-blocking I/O
- Protocol Buffers integration
- gRPC support for distributed systems
- Advanced schema validation
- Compression support (gzip, zstd)
- C extension for performance-critical paths
- Type stub files (.pyi) for better IDE support

---

## [1.3.0] - 2025-12-17

### Added
- **Dependency Injection Support**: DI-compatible factory classes for modern Python architectures
  - New module: `container_module/di/adapters.py`
  - `IContainerFactory` Protocol for container creation abstraction
  - `IContainerSerializer` Protocol for serialization abstraction
  - `DefaultContainerFactory` implementation
  - `DefaultContainerSerializer` implementation
  - Convenience functions: `serialize_container()`, `deserialize_container()`
  - Facilitates integration with frameworks like FastAPI or Dependency Injector
  - Standardizes object creation patterns matching C++ Kcenon module patterns
  - Unit tests: `tests/test_di_adapters.py` (21 test cases)

### Usage Example
```python
from container_module import (
    DefaultContainerFactory,
    DefaultContainerSerializer,
    IContainerFactory,
)
from container_module.values import StringValue

# Use factory for dependency injection
factory = DefaultContainerFactory()
container = factory.create(
    source_id="client1",
    target_id="server1",
    message_type="request"
)

# Or use builder pattern via factory
container = (
    factory.create_builder()
    .set_source("client1")
    .set_target("server1")
    .add_value(StringValue("data", "value"))
    .build()
)

# FastAPI integration example
from fastapi import Depends

def get_factory() -> IContainerFactory:
    return DefaultContainerFactory()

@app.post("/messages")
async def create_message(factory: IContainerFactory = Depends(get_factory)):
    container = factory.create(source_id="api")
    return {"status": "created"}
```

---

## [1.2.0] - 2025-12-17

### Added
- **MessagingBuilder Pattern**: Fluent API for ValueContainer creation
  - New module: `container_module/messaging/builder.py`
  - `MessagingBuilder` class with method chaining support
  - Methods: `set_source()`, `set_target()`, `set_type()`, `add_value()`, `add_values()`, `build()`, `reset()`
  - Simplifies complex message header configuration
  - Equivalent to C++ messaging builder pattern
  - Unit tests: `tests/test_messaging_builder.py` (14 test cases)

### Usage Example
```python
from container_module import MessagingBuilder
from container_module.values import StringValue, IntValue

container = (
    MessagingBuilder()
    .set_source("client1", "session1")
    .set_target("server1", "handler1")
    .set_type("request")
    .add_value(StringValue("name", "John"))
    .add_value(IntValue("age", 30))
    .build()
)
```

---

## [1.1.0] - 2025-10-26

### Added
- **Performance Profiling & Optimization**: Comprehensive benchmark suite
  - Performance benchmark script (benchmarks/performance_benchmark.py)
  - Detailed performance report (benchmarks/PERFORMANCE_REPORT.md)
  - Metrics for all operations (creation, serialization, deserialization)
  - Comparison across all serialization formats
- **Edge Case Testing**: Extensive boundary condition coverage
  - Edge case test suite (tests/test_edge_cases.py)
  - Simple test runner without pytest dependency (tests/run_edge_case_tests.py)
  - Numeric boundary tests (min/max values for all types)
  - String edge cases (empty, very long, unicode, special characters)
  - Bytes edge cases (empty, large binary, null bytes)
  - Container edge cases (empty, many values, special headers)
  - Serialization edge cases (binary, JSON, XML with special data)
- **MessagePack Serialization**: Zero-dependency binary format
  - Pure Python MessagePack implementation (container_module/serializers/messagepack_serializer.py)
  - Full MessagePack spec support (integers, floats, strings, binary, arrays, maps)
  - Container serialization to MessagePack
  - Header deserialization from MessagePack
  - MessagePack example (examples/messagepack_example.py)
  - 50% smaller than JSON, significantly faster
  - Cross-platform binary format

### Performance
- **Value Creation**: 4-6M operations/sec
  - BoolValue: 4.2M ops/sec
  - IntValue: 5.8M ops/sec
  - StringValue: 6.1M ops/sec
- **Binary Serialization**: 6.7M operations/sec (baseline)
- **Binary Deserialization**: 700K operations/sec
- **Container Creation**: 174K operations/sec
- **Serialization Format Comparison**:
  - Binary: Fastest (6.7M ops/sec)
  - MessagePack: ~2.5M ops/sec (2.7x slower than binary, 54x faster than JSON)
  - JSON: 50K ops/sec (134x slower than binary)
  - XML: 16K ops/sec (406x slower than binary)
- **File Sizes**:
  - Binary: 167 bytes (baseline)
  - MessagePack: 248 bytes (49% larger, but cross-platform)
  - XML: 326 bytes (95% larger)
  - JSON: 490 bytes (193% larger)

### Documentation
- Performance analysis and optimization recommendations
- Edge case coverage documentation
- MessagePack usage examples and best practices

---

## [1.0.0] - 2025-10-26

### Added
- **15 Value Types**: Complete implementation matching C++ version
  - Primitive types: Bool, Short, UShort, Int, UInt, Long, ULong, LLong, ULLong
  - Numeric types: Float, Double
  - Complex types: String, Bytes, Container (nested)
  - Null type for empty values
- **ValueContainer**: Full-featured message container system
  - Header management (source_id, target_id, message_type)
  - Sub-ID support for hierarchical addressing
  - Value storage and retrieval with dictionary-based lookup
  - Container copy operations (with/without values)
  - Header swap for request-response patterns
- **Type-Safe Value System**: ABC-based design with runtime type checking
  - Abstract Value base class with consistent API
  - Type conversion methods (to_int32, to_int64, to_string, to_bytes)
  - Type hints throughout (PEP 484 compliance)
  - Safe type checking with is_container, is_null properties
- **Multiple Serialization Formats**: Three serialization options
  - **Binary format**: Compact wire format with Little Endian encoding
  - **JSON format**: Standard JSON with type information
  - **XML format**: Self-describing XML structure
  - Wire-compatible with C++ version
- **File I/O Operations**: Complete file persistence support
  - save_to_file / load_from_file (binary format)
  - to_json_file / from_json_file
  - to_xml_file / from_xml_file
  - Atomic file operations with error handling
- **Thread-Safe Mode**: Optional concurrent access support
  - enable_thread_safety() method for opt-in locking
  - threading.RLock-based implementation
  - Recursive lock for nested operations
  - Zero overhead when disabled
- **Nested Container Support**: Hierarchical data structures
  - ContainerValue for child value management
  - Recursive serialization and deserialization
  - Query by name with index support
  - Deep copy for nested structures
- **Type Hints**: Full PEP 484 compliance
  - Type hints throughout codebase
  - py.typed marker for mypy support
  - Better IDE autocomplete and error detection
- **Properties for Clean API**: Pythonic read-only attributes
  - @property decorators for immutable fields
  - Clean attribute access (container.source_id instead of get_source_id())
  - Consistent with Python conventions
- **Context Managers**: Resource safety patterns
  - Proper cleanup for file operations
  - Exception-safe resource handling
- **Comprehensive Testing**: Production-ready test suite
  - Unit tests for all value types
  - Container operation tests
  - Serialization/deserialization tests
  - Thread safety tests
  - GitHub Actions CI/CD pipeline
- **Complete Documentation**:
  - README.md: Comprehensive English documentation (462 lines)
  - PROJECT_SUMMARY.md: Implementation summary and metrics
  - ENHANCEMENTS_SUMMARY.md: Enhancement documentation
  - Examples: 2 complete usage examples (basic + advanced)

### Performance Characteristics
- **Compared to C++ Version**: ~5x slower (interpreted nature)
  - Container creation: ~500K/sec (C++: 2M/sec)
  - Value addition: ~3M/sec (C++: 15M/sec)
  - Serialization: ~400K/sec (C++: 2M/sec)
  - Deserialization: ~300K/sec (C++: 1.5M/sec)
- **Memory Overhead**: Higher than C++ due to Python object model
- **GIL Limitation**: Thread parallelism limited by Global Interpreter Lock
- **No SIMD**: Python doesn't support direct SIMD operations

### Safety Guarantees
- **Type Safety**: Runtime type checking + type hints
  - isinstance() checks at runtime
  - Type hints for static analysis
  - Explicit error messages for type mismatches
- **Memory Safety**: Automatic memory management
  - Garbage collector handles cleanup
  - No manual memory management
  - No memory leaks or dangling pointers
- **Thread Safety**: Optional concurrent access
  - Opt-in RLock protection
  - Recursive locking for nested calls
  - Safe for multi-threaded applications when enabled
- **Error Handling**: Explicit exception raising
  - ValueError for invalid inputs
  - TypeError for type mismatches
  - Clear error messages for debugging

### Quality Metrics
- **Code Metrics**: ~2,616 lines of code
  - Core modules: ~1,162 lines
  - Value implementations: ~740 lines
  - Tests: ~294 lines
  - Examples: ~426 lines
- **Test Coverage**: Comprehensive unit and integration tests
- **Code Quality**: Black formatting, pylint compliant
- **Documentation**: Complete with examples and API reference
- **Examples**: 2 comprehensive example programs
  - basic_usage.py: Core functionality and patterns (141 lines)
  - advanced_usage.py: Nested containers, binary data, thread safety, file I/O (285 lines)

### Compatibility
- **Wire-Format Compatible with C++**: Binary data can be exchanged
  - Same serialization format
  - Same type codes (identical numeric values)
  - Same header structure
  - Same value semantics
- **Cross-Language Support**:
  - Python clients ↔ C++ servers
  - C++ clients ↔ Python servers
  - Mixed-language messaging systems
  - Gradual migration between implementations

---

## [0.1.0] - 2025-10-15 (Initial Development)

### Added
- Initial project structure with setuptools
- Core module with ValueTypes enumeration
- Abstract Value base class
- Basic value implementations (Bool, Int, String, Bytes)
- ValueContainer with header support
- Binary serialization
- JSON conversion
- Basic test suite
- README documentation

### Development Milestones
1. **Project Setup** (Day 1):
   - Python package structure
   - setup.py and pyproject.toml
   - Core module design

2. **Core Implementation** (Days 2-3):
   - ValueTypes enumeration (15 types)
   - Abstract Value class with ABC
   - Type conversion methods
   - Numeric value types (10 types)

3. **Container Implementation** (Days 4-5):
   - ValueContainer class
   - Header management (source/target/message_type)
   - Value storage with dictionary-based lookup
   - add / remove / get operations

4. **Serialization** (Day 6):
   - Binary format serialization
   - JSON conversion
   - XML conversion
   - File I/O support

5. **Testing & Documentation** (Day 7):
   - Unit tests for all value types
   - Container operation tests
   - Serialization tests
   - README and documentation

---

## Comparison with C++ Version

### Feature Parity

| Feature | C++ v1.0.0 | Python v1.1.0 | Notes |
|---------|------------|---------------|-------|
| Value Types | 15 types | 15 types | ✅ 100% Complete |
| Container API | Full | Full | ✅ Complete |
| Binary Serialization | ✓ | ✓ | ✅ Complete |
| JSON Serialization | ✓ | ✓ | ✅ Complete |
| XML Serialization | ✓ | ✓ | ✅ Complete |
| MessagePack | Planned | ✓ | ✅ Enhanced |
| File I/O | Basic | Full (4 formats) | ✅ Enhanced |
| Thread Safety | mutex | RLock (opt-in) | ✅ Complete |
| Nested Containers | ✓ | ✓ | ✅ Complete |
| Memory Management | Smart pointers | GC | ✅ Different approach |
| SIMD Support | ✓ (AVX2, NEON) | N/A | N/A (Python) |
| Type Hints | N/A | ✓ (PEP 484) | ✅ Enhanced |
| Properties | N/A | ✓ | ✅ Enhanced |
| Context Managers | N/A | ✓ | ✅ Enhanced |

### Advantages Over C++

1. **Simplified Development**:
   - C++: Manual memory management, complex build systems
   - Python: Automatic GC, simple pip install

2. **Type Hints**:
   - C++: Compile-time type checking only
   - Python: Type hints + runtime checks for better safety

3. **Ease of Integration**:
   - C++: Compilation required, platform-specific binaries
   - Python: Zero compilation, cross-platform source code

4. **Modern Language Features**:
   - Properties for clean API (container.source_id)
   - Context managers for resource safety
   - List comprehensions and generators
   - Duck typing with type hints

5. **Development Speed**:
   - C++: Slower compile-edit-test cycle
   - Python: Instant execution, rapid prototyping

6. **MessagePack Support**:
   - C++: Planned for future release
   - Python: Fully implemented with zero dependencies

### Trade-offs

**C++ Advantages**:
- Performance: ~5x faster across all operations
- SIMD support: 25M numeric ops/sec vs N/A
- Lower memory overhead: Direct memory allocation
- Zero-cost abstractions with templates
- Deterministic destruction with RAII
- Better for resource-constrained systems

**Python Advantages**:
- Memory safety: Automatic GC prevents use-after-free
- Easier deployment: No compilation required
- Faster development: Simpler syntax, less boilerplate
- Better integration: Rich ecosystem of Python libraries
- Type hints: Static analysis + runtime checking
- Properties and context managers for cleaner code

### Performance Comparison

| Operation | C++ (estimated) | Python (measured) | Ratio |
|-----------|----------------|-------------------|-------|
| Value creation | ~10M ops/sec | 4-6M ops/sec | ~2x slower |
| Container creation | 2M ops/sec | 174K ops/sec | ~11x slower |
| Binary serialization | Very fast | 6.7M ops/sec | Similar |
| JSON serialization | Fast | 50K ops/sec | ~5x slower |
| MessagePack | N/A | 2.5M ops/sec | Python advantage |
| SIMD operations | 25M ops/sec | N/A | C++ advantage |

---

## Version Numbering

This project uses Semantic Versioning:
- **MAJOR** version: Incompatible API changes
- **MINOR** version: Backwards-compatible functionality additions
- **PATCH** version: Backwards-compatible bug fixes

### Pre-1.0.0 Releases

During the 0.x.x series:
- MINOR version bumps may include breaking changes
- PATCH version bumps include backwards-compatible bug fixes
- API stability is not guaranteed until 1.0.0 release

---

## Migration Notes

### From C++ container_system

The Python version provides equivalent functionality with Pythonic idioms:

```cpp
// C++ version
auto container = std::make_shared<value_container>();
container->set_source("client", "session");
auto value = std::make_shared<int_value>("count", 42);
container->add_value(value);
```

```python
# Python version
container = ValueContainer(source_id="client", source_sub_id="session")
value = IntValue("count", 42)
container.add(value)
```

**Key Differences**:
1. **Smart Pointers**: `std::shared_ptr` → automatic GC (no manual reference counting)
2. **Naming Convention**: snake_case (Python) vs camelCase (C++)
3. **Error Handling**: Exceptions → exceptions (but more Pythonic)
4. **Thread Safety**: Manual mutex → opt-in RLock
5. **Memory Management**: RAII → garbage collection
6. **Properties**: Methods → properties (container.source_id vs container->get_source_id())

### API Changes from 1.0.0 to 1.1.0

**Added**:
- MessagePack serialization (MessagePackSerializer class)
- Performance benchmark suite
- Edge case test suite
- Simple test runner (no pytest required)

**Changed**:
- None (backwards compatible additions only)

**Removed**:
- None (backwards compatible additions only)

### Upgrading from 1.0.0 to 1.1.0

```python
# Old: Binary, JSON, XML serialization (still works)
binary_data = container.serialize()
json_str = container.to_json()
xml_str = container.to_xml()

# New: MessagePack serialization
from container_module.serializers import MessagePackSerializer
msgpack_data = MessagePackSerializer.container_to_msgpack(container)
restored = MessagePackSerializer.msgpack_to_container(msgpack_data)

# New: Run performance benchmarks
# python3 benchmarks/performance_benchmark.py

# New: Run edge case tests
# python3 tests/run_edge_case_tests.py
```

### Type Hints Benefits

Python Container System uses type hints throughout:

```python
def add(self, value: Value) -> None:
    """Add a value to the container."""
    # Type checking at development time with mypy
    # Runtime validation with isinstance()
```

**Benefits**:
- IDE autocomplete and error detection
- Static analysis with mypy
- Better documentation
- Easier refactoring
- Catches errors before runtime

---

## Contributing

When contributing, please:
1. Follow Python code conventions (PEP 8)
2. Use Black for code formatting
3. Add type hints to all new code
4. Add tests for new functionality
5. Update documentation and examples
6. Update this CHANGELOG under [Unreleased]
7. Ensure all tests pass (pytest)
8. Run linters (mypy, pylint)

---

## License

This project is licensed under the BSD 3-Clause License, same as the original C++ container_system.

---

**Project Status**: ✅ Production Ready (100% Feature Complete + Enhanced)
**Latest Version**: 1.1.0
**Release Date**: 2025-10-26
**Python Version**: 3.8+
**GitHub**: https://github.com/kcenon/python_container_system
**C++ Version**: https://github.com/kcenon/container_system
