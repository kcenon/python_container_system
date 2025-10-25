#!/usr/bin/env python3
"""
Performance benchmarking for Container System

Measures performance of:
- Value creation
- Serialization (Binary, JSON, XML)
- Deserialization
- Container operations
"""

import time
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from container_module import ValueContainer
from container_module.values import (
    BoolValue, ShortValue, IntValue, LongValue,
    FloatValue, DoubleValue, StringValue, BytesValue
)


def benchmark(name: str, func, iterations: int = 10000):
    """Run benchmark and report results."""
    start = time.perf_counter()
    for _ in range(iterations):
        func()
    elapsed = time.perf_counter() - start
    ops_per_sec = iterations / elapsed

    print(f"{name:40s}: {ops_per_sec:>12,.0f} ops/sec  ({elapsed:.3f}s for {iterations:,} iterations)")
    return ops_per_sec


def create_test_container():
    """Create a container with various value types."""
    container = ValueContainer(
        source_id="bench_src",
        target_id="bench_tgt",
        message_type="benchmark"
    )
    container.add(BoolValue("bool", True))
    container.add(ShortValue("short", 12345))
    container.add(IntValue("int", 1234567))
    container.add(LongValue("long", 123456789))
    container.add(FloatValue("float", 3.14159))
    container.add(DoubleValue("double", 2.718281828))
    container.add(StringValue("string", "Hello, World!"))
    container.add(BytesValue("bytes", b"Binary data"))
    return container


def main():
    """Run all benchmarks."""
    print("=" * 80)
    print("Container System Performance Benchmark")
    print("=" * 80)
    print()

    # 1. Value creation benchmarks
    print("1. Value Creation:")
    print("-" * 80)
    benchmark("BoolValue creation", lambda: BoolValue("test", True))
    benchmark("IntValue creation", lambda: IntValue("test", 12345))
    benchmark("FloatValue creation", lambda: FloatValue("test", 3.14))
    benchmark("StringValue creation", lambda: StringValue("test", "Hello"))
    benchmark("BytesValue creation", lambda: BytesValue("test", b"data"))
    print()

    # 2. Container operations
    print("2. Container Operations:")
    print("-" * 80)

    test_container = create_test_container()
    benchmark("Container creation (8 values)", create_test_container)
    benchmark("Container.get_value()", lambda: test_container.get_value("string"))
    print()

    # 3. Serialization benchmarks
    print("3. Serialization:")
    print("-" * 80)

    container = create_test_container()
    benchmark("Binary serialize", lambda: container.serialize())
    benchmark("JSON serialize", lambda: container.to_json())
    benchmark("XML serialize", lambda: container.to_xml())
    print()

    # 4. Deserialization benchmarks
    print("4. Deserialization:")
    print("-" * 80)

    binary_data = container.serialize()
    json_data = container.to_json()
    xml_data = container.to_xml()

    benchmark("Binary deserialize", lambda: ValueContainer(data_string=binary_data))
    print()

    # 5. Round-trip benchmarks
    print("5. Round-trip (Serialize + Deserialize):")
    print("-" * 80)

    def binary_roundtrip():
        c = create_test_container()
        data = c.serialize()
        ValueContainer(data_string=data)

    benchmark("Binary round-trip", binary_roundtrip)
    print()

    # 6. Large container benchmark
    print("6. Large Container (100 values):")
    print("-" * 80)

    def create_large_container():
        container = ValueContainer(source_id="large", target_id="test")
        for i in range(100):
            container.add(IntValue(f"value_{i}", i))
        return container

    benchmark("Create 100 values", create_large_container, iterations=1000)

    large = create_large_container()
    benchmark("Serialize 100 values", lambda: large.serialize(), iterations=1000)

    large_data = large.serialize()
    benchmark("Deserialize 100 values", lambda: ValueContainer(data_string=large_data), iterations=1000)
    print()

    # 7. Memory efficiency test
    print("7. Memory Efficiency:")
    print("-" * 80)

    import sys

    # Measure size of serialized data
    binary_size = len(binary_data)
    json_size = len(json_data)
    xml_size = len(xml_data)

    print(f"{'Binary format size':40s}: {binary_size:>8,} bytes")
    print(f"{'JSON format size':40s}: {json_size:>8,} bytes  ({json_size/binary_size:.1f}x binary)")
    print(f"{'XML format size':40s}: {xml_size:>8,} bytes  ({xml_size/binary_size:.1f}x binary)")
    print()

    # 8. Summary
    print("=" * 80)
    print("Benchmark Complete!")
    print("=" * 80)
    print()
    print("Performance Tips:")
    print("  - Binary format is fastest and most compact")
    print("  - JSON is good for debugging and web APIs")
    print("  - XML provides best interoperability")
    print("  - Batch operations when possible")
    print("  - Reuse containers to reduce allocation overhead")


if __name__ == "__main__":
    main()
