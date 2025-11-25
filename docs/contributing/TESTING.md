# Python Container System - Testing Guide

> **Last Updated:** 2025-11-26
> **Maintainer:** Container System Development Team

## Overview

This document provides a comprehensive guide to the Python Container System's testing infrastructure, including unit tests, integration tests, performance benchmarks, and testing best practices.

---

## Test Architecture

The Python Container System employs a multi-layered testing strategy:

```
┌─────────────────────────────────────────────┐
│           Testing Infrastructure            │
├─────────────────────────────────────────────┤
│  Unit Tests (tests/)                        │
│  ├─ Value type tests                        │
│  ├─ Container operations                    │
│  ├─ Serialization formats                   │
│  ├─ Thread safety                           │
│  └─ Edge cases                              │
├─────────────────────────────────────────────┤
│  Integration Tests                          │
│  ├─ Cross-language compatibility            │
│  ├─ End-to-end scenarios                    │
│  └─ Real-world usage patterns               │
├─────────────────────────────────────────────┤
│  Benchmark Tests (benchmarks/)              │
│  ├─ Container operations                    │
│  ├─ Serialization performance               │
│  └─ Memory usage                            │
└─────────────────────────────────────────────┘
```

---

## Test Organization

### Test Directory Structure

```
tests/
├── test_value_types.py      # Value type system tests
├── test_container.py        # Container operations tests
├── test_array_value.py      # ArrayValue tests
├── test_edge_cases.py       # Edge case and boundary tests
├── test_cross_language_array.py  # Cross-language interop tests
├── test_long_range_checking.py   # Numeric range tests
├── conftest.py              # Pytest fixtures
└── __init__.py

benchmarks/
├── benchmark_container.py   # Container benchmarks
├── benchmark_serialization.py  # Serialization benchmarks
└── PERFORMANCE_REPORT.md    # Performance results
```

### Test Categories

#### 1. Value Type Tests (`test_value_types.py`)

Tests for all 15 supported value types:
- Null, Boolean, Numeric (all integer variants)
- Float, Double
- String and Bytes
- Container and Array values

```python
def test_int_value_creation():
    """Test IntValue creation and retrieval."""
    value = IntValue("count", 42)

    assert value.name == "count"
    assert value.to_int() == 42
    assert value.value_type == ValueType.INT


def test_int_value_boundary():
    """Test IntValue at boundaries."""
    # Max value
    max_val = IntValue("max", 2147483647)
    assert max_val.to_int() == 2147483647

    # Min value
    min_val = IntValue("min", -2147483648)
    assert min_val.to_int() == -2147483648
```

#### 2. Container Operations Tests (`test_container.py`)

```python
def test_container_add_get():
    """Test adding and retrieving values."""
    container = ValueContainer(message_type="test")
    container.add(StringValue("name", "Alice"))
    container.add(IntValue("age", 30))

    name = container.get_value("name")
    assert name is not None
    assert name.to_string() == "Alice"

    age = container.get_value("age")
    assert age is not None
    assert age.to_int() == 30


def test_container_serialization_roundtrip():
    """Test serialization and deserialization."""
    original = ValueContainer(
        source_id="client",
        target_id="server",
        message_type="request"
    )
    original.add(StringValue("action", "query"))
    original.add(IntValue("limit", 100))

    # Serialize and deserialize
    serialized = original.serialize()
    restored = ValueContainer(data_string=serialized)

    assert restored.source_id == "client"
    assert restored.target_id == "server"
    assert restored.message_type == "request"
    assert restored.get_value("action").to_string() == "query"
    assert restored.get_value("limit").to_int() == 100
```

#### 3. Edge Case Tests (`test_edge_cases.py`)

```python
def test_empty_string_value():
    """Test empty string handling."""
    value = StringValue("empty", "")
    assert value.to_string() == ""


def test_unicode_string():
    """Test Unicode string handling."""
    value = StringValue("unicode", "한글 テスト 🚀")
    assert value.to_string() == "한글 テスト 🚀"


def test_large_bytes_value():
    """Test large binary data."""
    large_data = bytes(range(256)) * 1000  # 256KB
    value = BytesValue("large", large_data)
    assert value.to_bytes() == large_data
```

#### 4. Thread Safety Tests

```python
def test_thread_safe_operations():
    """Test thread-safe container operations."""
    container = ValueContainer(message_type="threaded")
    container.enable_thread_safety(True)

    errors = []

    def worker(worker_id):
        try:
            for i in range(100):
                container.add(IntValue(f"worker_{worker_id}_{i}", i))
        except Exception as e:
            errors.append(e)

    threads = [threading.Thread(target=worker, args=(i,)) for i in range(10)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    assert len(errors) == 0
```

---

## Running Tests

### Basic Commands

```bash
# Install test dependencies
pip install -e ".[dev]"

# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_container.py

# Run specific test function
pytest tests/test_container.py::test_container_add_get

# Run tests matching pattern
pytest -k "serialization"
```

### With Coverage

```bash
# Run with coverage
pytest --cov=container_module --cov-report=html

# View coverage report
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux

# Terminal coverage report
pytest --cov=container_module --cov-report=term-missing
```

### Parallel Execution

```bash
# Install pytest-xdist
pip install pytest-xdist

# Run tests in parallel
pytest -n auto  # Auto-detect CPU cores
pytest -n 4     # Use 4 workers
```

---

## Test Coverage

### Current Coverage Targets

| Component | Target | Status |
|-----------|--------|--------|
| Core (Value, Container) | 85%+ | ✅ |
| Value Types | 90%+ | ✅ |
| Serialization | 80%+ | ✅ |
| Thread Safety | 75%+ | ✅ |
| **Overall** | **80%+** | ✅ |

### Generating Coverage Report

```bash
# Generate coverage with HTML report
pytest --cov=container_module --cov-report=html --cov-report=xml

# Upload to codecov (in CI)
codecov --file coverage.xml
```

---

## Writing Tests

### Test Naming Conventions

```python
# Format: test_<component>_<action>_<scenario>
def test_int_value_creation(): ...
def test_container_serialize_with_nested(): ...
def test_thread_safety_concurrent_writes(): ...
```

### Test Structure (AAA Pattern)

```python
def test_container_copy_with_values():
    """Test container copy including values."""
    # Arrange - Set up test data
    original = ValueContainer(message_type="test")
    original.add(StringValue("name", "Alice"))
    original.add(IntValue("age", 30))

    # Act - Perform the operation
    copied = original.copy(containing_values=True)

    # Assert - Verify results
    assert copied.message_type == "test"
    assert copied.get_value("name").to_string() == "Alice"
    assert copied.get_value("age").to_int() == 30

    # Verify it's a true copy (not reference)
    copied.add(StringValue("extra", "value"))
    assert original.get_value("extra") is None
```

### Parametrized Tests

```python
import pytest

@pytest.mark.parametrize("value,expected", [
    (0, 0),
    (1, 1),
    (-1, -1),
    (2147483647, 2147483647),
    (-2147483648, -2147483648),
])
def test_int_value_boundaries(value, expected):
    """Test IntValue with various boundary values."""
    int_val = IntValue("test", value)
    assert int_val.to_int() == expected


@pytest.mark.parametrize("value_class,value,type_enum", [
    (BoolValue, True, ValueType.BOOL),
    (IntValue, 42, ValueType.INT),
    (StringValue, "test", ValueType.STRING),
])
def test_value_types(value_class, value, type_enum):
    """Test various value type creations."""
    val = value_class("name", value)
    assert val.value_type == type_enum
```

### Fixtures

```python
# conftest.py
import pytest
from container_module import ValueContainer
from container_module.values import StringValue, IntValue

@pytest.fixture
def empty_container():
    """Provide an empty container."""
    return ValueContainer()


@pytest.fixture
def sample_container():
    """Provide a container with sample values."""
    c = ValueContainer(
        source_id="test_source",
        target_id="test_target",
        message_type="test_message"
    )
    c.add(StringValue("name", "Test"))
    c.add(IntValue("count", 42))
    c.add(BoolValue("active", True))
    return c


@pytest.fixture
def temp_file(tmp_path):
    """Provide a temporary file path."""
    return tmp_path / "test_data.dat"


# Usage in tests
def test_with_sample_container(sample_container):
    assert sample_container.get_value("name").to_string() == "Test"
```

---

## Benchmark Tests

### Writing Benchmarks

```python
# benchmarks/benchmark_container.py
import time
from container_module import ValueContainer
from container_module.values import IntValue, StringValue


def benchmark_container_creation(iterations=10000):
    """Benchmark container creation."""
    start = time.perf_counter()
    for _ in range(iterations):
        _ = ValueContainer()
    elapsed = time.perf_counter() - start

    ops_per_sec = iterations / elapsed
    print(f"Container creation: {ops_per_sec:.0f} ops/sec")
    return ops_per_sec


def benchmark_serialization(iterations=10000):
    """Benchmark binary serialization."""
    container = ValueContainer(message_type="bench")
    for i in range(10):
        container.add(IntValue(f"val_{i}", i))

    start = time.perf_counter()
    for _ in range(iterations):
        _ = container.serialize_to_bytes()
    elapsed = time.perf_counter() - start

    ops_per_sec = iterations / elapsed
    print(f"Binary serialization: {ops_per_sec:.0f} ops/sec")
    return ops_per_sec


if __name__ == "__main__":
    benchmark_container_creation()
    benchmark_serialization()
```

### Running Benchmarks

```bash
# Run benchmarks
python benchmarks/benchmark_container.py

# With pytest-benchmark (if installed)
pip install pytest-benchmark
pytest benchmarks/ --benchmark-enable
```

### Performance Targets

| Operation | Target | Notes |
|-----------|--------|-------|
| Container creation | >100K/s | Empty container |
| Value addition | >300K/s | Single value |
| Binary serialize | >50K/s | 10 values |
| Binary deserialize | >40K/s | 10 values |
| JSON serialize | >30K/s | 10 values |

---

## Continuous Integration

### GitHub Actions Workflow

```yaml
# .github/workflows/tests.yml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, macos-latest, windows-latest]
        python-version: ['3.8', '3.9', '3.10', '3.11', '3.12']

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -e ".[dev]"

      - name: Run tests
        run: pytest --cov=container_module --cov-report=xml

      - name: Upload coverage
        uses: codecov/codecov-action@v4
        with:
          file: coverage.xml
```

---

## Debugging Failed Tests

### Common Issues

1. **Import Errors**
   ```bash
   # Ensure package is installed
   pip install -e .
   ```

2. **Flaky Tests**
   ```bash
   # Run test multiple times
   pytest tests/test_flaky.py --count=10
   ```

3. **Threading Issues**
   ```bash
   # Run without parallelism
   pytest -n 0 tests/test_threading.py
   ```

### Debugging Commands

```bash
# Verbose output with print statements
pytest -v -s tests/test_failing.py

# Drop into debugger on failure
pytest --pdb tests/test_failing.py

# Show locals in traceback
pytest --tb=long tests/test_failing.py

# Run only last failed tests
pytest --lf
```

### Using pdb

```python
def test_with_debugger():
    container = ValueContainer()
    container.add(StringValue("name", "test"))

    import pdb; pdb.set_trace()  # Debugger breakpoint

    value = container.get_value("name")
    assert value is not None
```

---

## Test Maintenance

### Regular Tasks

- **Weekly**: Review CI test results
- **Monthly**: Update performance baselines
- **Quarterly**: Review and update coverage targets
- **Per Release**: Verify all tests pass on all platforms

### Quality Metrics

- **Execution Time**: All unit tests < 30 seconds
- **Reliability**: >99% pass rate in CI
- **Coverage**: Maintain >80% line coverage
- **Flakiness**: <1% flaky tests

---

## References

### Related Documentation

- [CONTRIBUTING](../../CONTRIBUTING.md) - Contribution guidelines
- [PERFORMANCE_REPORT](../../benchmarks/PERFORMANCE_REPORT.md) - Performance data
- [FAQ](../guides/FAQ.md) - Frequently asked questions

### External Resources

- [pytest Documentation](https://docs.pytest.org/)
- [pytest-cov](https://pytest-cov.readthedocs.io/)
- [Python Testing Best Practices](https://docs.python.org/3/library/unittest.html)

---

**Document Version:** 1.0
**Last Updated:** 2025-11-26
**Contact:** kcenon@naver.com
