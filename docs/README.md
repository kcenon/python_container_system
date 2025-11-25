# Python Container System Documentation

> **Language:** **English** | [한국어](README_KO.md)

**Version:** 1.1.0
**Last Updated:** 2025-11-26
**Status:** Production Ready

Welcome to the Python Container System documentation! A type-safe, high-performance container and serialization system for Python 3.8+ with multiple format support and zero external dependencies.

---

## 🚀 Quick Navigation

| I want to... | Document |
|--------------|----------|
| ⚡ Understand the system | [Architecture](../ARCHITECTURE.md) |
| ❓ Find answers to common questions | [FAQ](guides/FAQ.md) |
| 🔧 Learn the API | [API Reference](API_REFERENCE.md) |
| 📊 Review performance | [Benchmarks](performance/BENCHMARKS.md) |

---

## Documentation Structure

### 📘 Core Documentation

| Document | Description | Korean | Lines |
|----------|-------------|--------|-------|
| [FEATURES.md](FEATURES.md) | Complete feature documentation | - | 800+ |
| [API_REFERENCE.md](API_REFERENCE.md) | API reference with Python examples | - | 700+ |
| [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) | Project organization | - | 600+ |
| [ARCHITECTURE.md](../ARCHITECTURE.md) | System architecture and design | - | 1600+ |
| [CHANGELOG.md](../CHANGELOG.md) | Version history and changes | - | 400+ |

### 📗 User Guides

| Document | Description | Lines |
|----------|-------------|-------|
| [FAQ.md](guides/FAQ.md) | Frequently asked questions | 300+ |
| [TROUBLESHOOTING.md](guides/TROUBLESHOOTING.md) | Common issues and solutions | 200+ |
| [ARRAY_VALUE_GUIDE.md](ARRAY_VALUE_GUIDE.md) | ArrayValue implementation guide | 150+ |
| [JSON_V2_ADAPTER.md](JSON_V2_ADAPTER.md) | Cross-language JSON adapter | 200+ |

### 📙 Advanced Topics

| Document | Description | Lines |
|----------|-------------|-------|
| [PROJECT_SUMMARY.md](../PROJECT_SUMMARY.md) | Implementation summary | 250+ |
| [ENHANCEMENTS_SUMMARY.md](../ENHANCEMENTS_SUMMARY.md) | Enhancement documentation | 200+ |

### 📊 Performance

| Document | Description | Korean | Lines |
|----------|-------------|--------|-------|
| [BENCHMARKS.md](performance/BENCHMARKS.md) | Performance benchmarks and analysis | - | 500+ |
| [PERFORMANCE_REPORT.md](../benchmarks/PERFORMANCE_REPORT.md) | Raw benchmark data | - | 200+ |

### 🤝 Contributing

| Document | Description | Lines |
|----------|-------------|-------|
| [TESTING.md](contributing/TESTING.md) | Testing strategy and guidelines | 300+ |
| [CONTRIBUTING.md](../CONTRIBUTING.md) | Contribution guidelines | 200+ |

---

## Project Information

### Current Status
- **Version**: 1.1.0 (Production Ready)
- **Python Version**: 3.8+
- **License**: BSD 3-Clause

### Key Features
- ✅ **Type-safe values** - 16 value types with runtime validation
- ✅ **Multiple formats** - Binary, JSON v2.0, XML, MessagePack
- ✅ **High performance** - 6.7M binary serialize/sec, 173K containers/sec
- ✅ **Zero dependencies** - Pure Python standard library
- ✅ **Thread-safe** - Optional RLock for concurrent access
- ✅ **Cross-platform** - Linux, macOS, Windows

---

## Getting Started

### Installation

```bash
# From source
git clone https://github.com/kcenon/python_container_system.git
cd python_container_system
pip install -e .

# From PyPI (when published)
pip install python-container-system
```

### Quick Example

```python
from container_module import ValueContainer
from container_module.values import StringValue, IntValue, BoolValue

# Create container
container = ValueContainer(
    source_id="client_01",
    target_id="server",
    message_type="user_data"
)

# Add values
container.add(StringValue("name", "Alice"))
container.add(IntValue("age", 30))
container.add(BoolValue("active", True))

# Serialize
data = container.serialize()  # Binary format (6.7M ops/sec)
json_str = container.to_json()  # JSON format (50K ops/sec)

# Deserialize
restored = ValueContainer(data_string=data)
```

### Value Types

| Category | Types | Size |
|----------|-------|------|
| **Null** | `Value` | 0 bytes |
| **Boolean** | `BoolValue` | 1 byte |
| **16-bit Integers** | `ShortValue`, `UShortValue` | 2 bytes |
| **32-bit Integers** | `IntValue`, `UIntValue`, `LongValue`*, `ULongValue`* | 4 bytes |
| **64-bit Integers** | `LLongValue`, `ULLongValue` | 8 bytes |
| **Floating Point** | `FloatValue`, `DoubleValue` | 4-8 bytes |
| **Complex** | `StringValue`, `BytesValue`, `ContainerValue`, `ArrayValue` | Variable |

*\* LongValue/ULongValue are 32-bit for C++ compatibility*

### Serialization Formats

| Format | Use Case | Throughput | Size | Cross-Language |
|--------|----------|-----------|------|----------------|
| **Binary** | Production, network | 6.7M ops/sec | 167 bytes | Yes (C++, .NET, Go) |
| **JSON v2.0** | Interoperability | 50K ops/sec | 490 bytes | Yes |
| **MessagePack** | Compact binary | 2.5M ops/sec | 248 bytes | Optional |
| **XML** | Legacy systems | 16K ops/sec | 326 bytes | Yes |

---

## Documentation Index

### By Topic

#### 🎯 For New Users
1. [README.md](../README.md) - Project overview and quick start
2. [FAQ.md](guides/FAQ.md) - Common questions answered
3. [FEATURES.md](FEATURES.md) - Complete feature documentation
4. [API_REFERENCE.md](API_REFERENCE.md) - API documentation

#### 🛠 For Developers
1. [ARCHITECTURE.md](../ARCHITECTURE.md) - System design and principles
2. [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) - File organization
3. [TESTING.md](contributing/TESTING.md) - Testing guidelines
4. [CONTRIBUTING.md](../CONTRIBUTING.md) - Contribution process

#### ⚡ For Performance
1. [BENCHMARKS.md](performance/BENCHMARKS.md) - Detailed performance analysis
2. [PERFORMANCE_REPORT.md](../benchmarks/PERFORMANCE_REPORT.md) - Raw benchmark data
3. [ENHANCEMENTS_SUMMARY.md](../ENHANCEMENTS_SUMMARY.md) - Recent improvements

#### 🔗 For Integration
1. [JSON_V2_ADAPTER.md](JSON_V2_ADAPTER.md) - Cross-language JSON format
2. [ARRAY_VALUE_GUIDE.md](ARRAY_VALUE_GUIDE.md) - Array value usage
3. [TROUBLESHOOTING.md](guides/TROUBLESHOOTING.md) - Common issues

### By Use Case

#### Web Development
- [FEATURES.md#web-api-response](FEATURES.md#web-api-response) - API response examples
- [API_REFERENCE.md#serialization](API_REFERENCE.md#serialization) - JSON serialization
- [BENCHMARKS.md#web-apis](performance/BENCHMARKS.md#performance-by-use-case) - Performance for web

#### Data Processing
- [FEATURES.md#database-storage](FEATURES.md#database-storage) - Database integration
- [BENCHMARKS.md#data-processing](performance/BENCHMARKS.md#performance-by-use-case) - Processing performance
- [PROJECT_STRUCTURE.md#test-organization](PROJECT_STRUCTURE.md#test-organization) - Testing examples

#### IoT Applications
- [FEATURES.md#iot-sensor-data](FEATURES.md#iot-sensor-data) - Sensor data handling
- [ARRAY_VALUE_GUIDE.md](ARRAY_VALUE_GUIDE.md) - Efficient array storage
- [BENCHMARKS.md#iot-data](performance/BENCHMARKS.md#performance-by-use-case) - IoT performance

#### Message Queues
- [FEATURES.md#messaging-integration](FEATURES.md#enhanced-features) - Message patterns
- [API_REFERENCE.md#valuecontainer](API_REFERENCE.md#valuecontainer) - Container API
- [BENCHMARKS.md#message-queues](performance/BENCHMARKS.md#performance-by-use-case) - Messaging performance

---

## Performance Highlights

*Python 3.14, macOS, Release Build*

| Operation | Throughput | Notes |
|-----------|-----------|-------|
| **Value creation** | 4-6M ops/sec | Depends on type |
| **Container creation** | 174K ops/sec | With 8 values |
| **Binary serialize** | 6.7M ops/sec | Very fast |
| **Binary deserialize** | 700K ops/sec | Parser overhead |
| **JSON serialize** | 50K ops/sec | Use for APIs |
| **MessagePack** | 2.5M ops/sec | Compact binary |

**Performance Rating**: ⭐⭐⭐⭐⭐ (5/5)
- Fast enough for 99% of applications
- 10x slower than C++ (expected for Python)
- Binary format production-ready
- Linear scaling with container size

⚡ **[Full Benchmarks →](performance/BENCHMARKS.md)**

---

## Comparison with C++

| Aspect | C++ | Python | Notes |
|--------|-----|--------|-------|
| **Performance** | 2M ops/sec | 174K-6.7M ops/sec | 10x slower, still excellent |
| **Memory** | ~2 KB | ~4.2 KB | 2x larger, Python overhead |
| **Type Safety** | Compile-time | Runtime + hints | Python approach |
| **Dependencies** | fmt, spdlog | None | Pure Python advantage |
| **Development** | Slower | Faster | Rapid prototyping |
| **Wire Compatible** | Yes | Yes | Same format |

🏗️ **[Architecture Guide →](../ARCHITECTURE.md)**

---

## Quick Links by Role

### For Users
- 📖 [README.md](../README.md) - Start here
- ❓ [FAQ.md](guides/FAQ.md) - Common questions
- 🔧 [API_REFERENCE.md](API_REFERENCE.md) - API docs
- 🆘 [TROUBLESHOOTING.md](guides/TROUBLESHOOTING.md) - Problem solving

### For Contributors
- 🤝 [CONTRIBUTING.md](../CONTRIBUTING.md) - How to contribute
- 🧪 [TESTING.md](contributing/TESTING.md) - Testing guide
- 📁 [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) - Code organization
- 🏛️ [ARCHITECTURE.md](../ARCHITECTURE.md) - System design

### For Integrators
- 🔗 [JSON_V2_ADAPTER.md](JSON_V2_ADAPTER.md) - Cross-language JSON
- 📊 [ARRAY_VALUE_GUIDE.md](ARRAY_VALUE_GUIDE.md) - Array values
- 🌐 [FEATURES.md#integration](FEATURES.md#integration-capabilities) - Integration examples

---

## Project Ecosystem

The Python Container System is part of a larger ecosystem:

- **[container_system](https://github.com/kcenon/container_system)** (C++) - Original implementation
- **[dotnet_container_system](https://github.com/kcenon/dotnet_container_system)** (.NET) - .NET implementation
- **[go_container_system](https://github.com/kcenon/go_container_system)** (Go) - Go implementation
- **python_container_system** (Python) - This implementation

All implementations maintain **wire-format compatibility** for cross-language data exchange.

---

## Feature Comparison

| Feature | Status | Document |
|---------|--------|----------|
| **15+ Value Types** | ✅ Complete | [FEATURES.md#value-types](FEATURES.md#value-types) |
| **Binary Serialization** | ✅ Complete | [API_REFERENCE.md#serialization](API_REFERENCE.md#serialization) |
| **JSON Serialization** | ✅ Complete | [API_REFERENCE.md#serialization](API_REFERENCE.md#serialization) |
| **JSON v2.0** | ✅ Complete | [JSON_V2_ADAPTER.md](JSON_V2_ADAPTER.md) |
| **XML Serialization** | ✅ Complete | [API_REFERENCE.md#serialization](API_REFERENCE.md#serialization) |
| **MessagePack** | ✅ Complete | [FEATURES.md#messagepack](FEATURES.md#messagepack-serialization) |
| **Thread Safety** | ✅ Complete | [FEATURES.md#thread-safety](FEATURES.md#thread-safe-operations) |
| **Nested Containers** | ✅ Complete | [FEATURES.md#nested-containers](FEATURES.md#nested-containers) |
| **Array Values** | ✅ Complete | [ARRAY_VALUE_GUIDE.md](ARRAY_VALUE_GUIDE.md) |
| **Type Hints** | ✅ Complete | [ARCHITECTURE.md#type-hints](../ARCHITECTURE.md#core-principles) |
| **Zero Dependencies** | ✅ Yes | [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md#no-external-dependencies) |

---

## Roadmap

### Current Version (1.1.0)
- ✅ All value types implemented
- ✅ Multiple serialization formats
- ✅ Thread-safe operations
- ✅ Comprehensive testing
- ✅ MessagePack support
- ✅ Performance optimizations

### Future Plans
- ⏳ NumPy integration for arrays
- ⏳ Async/await support
- ⏳ Cython extensions for hot paths
- ⏳ Protocol Buffers support
- ⏳ gRPC integration

---

## 📞 Getting Help

### Documentation
- **FAQ**: [guides/FAQ.md](guides/FAQ.md) - 25+ common questions
- **Troubleshooting**: [guides/TROUBLESHOOTING.md](guides/TROUBLESHOOTING.md) - Problem solving
- **Examples**: [../examples/](../examples/) - Working code samples

### Community
- **Issues**: [GitHub Issues](https://github.com/kcenon/python_container_system/issues)
- **Discussions**: [GitHub Discussions](https://github.com/kcenon/python_container_system/discussions)
- **Email**: kcenon@naver.com

### Related Projects
- **C++ Version**: [container_system](https://github.com/kcenon/container_system)
- **Documentation**: Cross-reference with C++ docs for advanced topics

---

## License

This project is licensed under the BSD 3-Clause License - see the [LICENSE](../LICENSE) file for details.

---

## Acknowledgments

- Inspired by the C++ [container_system](https://github.com/kcenon/container_system)
- Designed for compatibility with the messaging system ecosystem
- Maintained by: kcenon@naver.com

---

<p align="center">
  <strong>Python Container System Documentation</strong><br>
  Version 1.1.0 | Last Updated: 2025-11-26
</p>

<p align="center">
  Made with ❤️ by 🍀☀🌕🌥 🌊
</p>
