# Python Container System Documentation

> **Version:** 1.1.0
> **Last Updated:** 2025-11-26

Welcome to the Python Container System documentation. This guide helps you navigate all available resources for using and contributing to the project.

---

## Quick Navigation

| Document | Description | Audience |
|----------|-------------|----------|
| [README](../README.md) | Project overview and quick start | Everyone |
| [ARCHITECTURE](../ARCHITECTURE.md) | System design and principles | Developers |
| [CHANGELOG](../CHANGELOG.md) | Version history | Everyone |
| [PROJECT_SUMMARY](../PROJECT_SUMMARY.md) | High-level overview | Everyone |

### Guides

| Document | Description | Audience |
|----------|-------------|----------|
| [FAQ](guides/FAQ.md) | Frequently asked questions | Users |
| [TROUBLESHOOTING](guides/TROUBLESHOOTING.md) | Common issues and solutions | Users |
| [JSON_V2_ADAPTER](JSON_V2_ADAPTER.md) | Cross-language JSON adapter guide | Developers |
| [ARRAY_VALUE_GUIDE](ARRAY_VALUE_GUIDE.md) | ArrayValue implementation guide | Developers |

### Contributing

| Document | Description | Audience |
|----------|-------------|----------|
| [CONTRIBUTING](../CONTRIBUTING.md) | How to contribute | Contributors |
| [TESTING](contributing/TESTING.md) | Testing guide | Contributors |

### Performance

| Document | Description | Audience |
|----------|-------------|----------|
| [PERFORMANCE_REPORT](../benchmarks/PERFORMANCE_REPORT.md) | Performance benchmarks | Developers |
| [ENHANCEMENTS_SUMMARY](../ENHANCEMENTS_SUMMARY.md) | Recent improvements | Developers |

---

## Getting Started

### For Users

1. Start with the [README](../README.md) for installation and quick start
2. Read the [FAQ](guides/FAQ.md) for common questions
3. Check [TROUBLESHOOTING](guides/TROUBLESHOOTING.md) if you encounter issues

### For Contributors

1. Read [CONTRIBUTING](../CONTRIBUTING.md) for contribution guidelines
2. Review [ARCHITECTURE](../ARCHITECTURE.md) for system design
3. Follow [TESTING](contributing/TESTING.md) for test requirements

### For Cross-Language Integration

1. Review [JSON_V2_ADAPTER](JSON_V2_ADAPTER.md) for JSON format compatibility
2. Check [ARRAY_VALUE_GUIDE](ARRAY_VALUE_GUIDE.md) for array handling

---

## Project Ecosystem

The Python Container System is part of a larger ecosystem:

- **[container_system](https://github.com/kcenon/container_system)**: Original C++ implementation
- **[dotnet_container_system](https://github.com/kcenon/dotnet_container_system)**: .NET implementation
- **[go_container_system](https://github.com/kcenon/go_container_system)**: Go implementation

---

## Key Features

### Value Types (15 types)

| Category | Types |
|----------|-------|
| **Null** | `Value` (null) |
| **Boolean** | `BoolValue` |
| **16-bit Integers** | `ShortValue`, `UShortValue` |
| **32-bit Integers** | `IntValue`, `UIntValue`, `LongValue`*, `ULongValue`* |
| **64-bit Integers** | `LLongValue`, `ULLongValue` |
| **Floating Point** | `FloatValue`, `DoubleValue` |
| **Complex** | `StringValue`, `BytesValue`, `ContainerValue`, `ArrayValue` |

*\* LongValue/ULongValue are 32-bit for C++ compatibility*

### Serialization Formats

| Format | Use Case | Cross-Language |
|--------|----------|----------------|
| Binary | High performance | Yes |
| JSON v2.0 | Interoperability | Yes |
| XML | Legacy systems | Yes |
| MessagePack | Compact binary | Optional |

---

## Support

- **GitHub Issues**: [Report bugs or request features](https://github.com/kcenon/python_container_system/issues)
- **GitHub Discussions**: [Ask questions and share ideas](https://github.com/kcenon/python_container_system/discussions)
- **Email**: kcenon@naver.com

---

**Last Updated:** 2025-11-26
