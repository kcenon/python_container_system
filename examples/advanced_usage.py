#!/usr/bin/env python3
"""
Advanced usage example for python_container_system

Demonstrates complex operations, nested containers, and thread safety.

Equivalent to C++ examples/advanced_usage.cpp
"""

import threading
import time
from typing import List
from container_module import ValueContainer
from container_module.values import (
    StringValue,
    IntValue,
    DoubleValue,
    ContainerValue,
    BytesValue,
)


def example_nested_containers():
    """Demonstrate nested container structures."""
    print("\n=== Nested Containers Example ===")

    # Create main container
    order = ValueContainer(message_type="order_create")
    order.add(StringValue("order_id", "ORD-2025-001234"))
    order.add(IntValue("customer_id", 98765))
    order.add(DoubleValue("total_amount", 299.99))

    # Create nested items container
    items = ContainerValue("items")

    # Add multiple items
    for i in range(3):
        item = ContainerValue(f"item_{i}")
        item.add(StringValue("sku", f"SKU-{1000+i}"))
        item.add(IntValue("quantity", i + 1))
        item.add(DoubleValue("unit_price", 99.99))
        items.add(item)

    order.add(items)

    # Display structure
    print(f"Order contains {len(order.units)} top-level values")
    items_value = order.get_value("items")
    if items_value:
        print(f"Items container has {items_value.child_count()} items")

    # Serialize
    serialized = order.serialize()
    print(f"Serialized size: {len(serialized)} bytes\n")


def example_bytes_value():
    """Demonstrate BytesValue for binary data."""
    print("\n=== Bytes Value Example ===")

    # Create container with binary data
    data_container = ValueContainer(message_type="binary_data")

    # Add raw bytes
    raw_data = bytes([0x01, 0x02, 0x03, 0x04, 0xFF, 0xFE])
    data_container.add(BytesValue("raw_bytes", raw_data))

    # Add hex data
    hex_value = BytesValue.from_hex("hex_data", "deadbeef")
    data_container.add(hex_value)

    # Retrieve and display
    raw = data_container.get_value("raw_bytes")
    if raw:
        print(f"Raw bytes (hex): {raw.to_hex()}")
        print(f"Raw bytes (base64): {raw.to_base64()}")

    hex_val = data_container.get_value("hex_data")
    if hex_val:
        print(f"Hex data: {hex_val.to_hex()}")
    print()


def example_thread_safety():
    """Demonstrate thread-safe operations."""
    print("\n=== Thread Safety Example ===")

    # Create thread-safe container
    container = ValueContainer(message_type="thread_test")
    container.enable_thread_safety(True)

    # Shared counter
    counters = {"read": 0, "write": 0}
    lock = threading.Lock()

    def writer_thread(thread_id: int):
        """Write values to container."""
        for i in range(10):
            container.add(IntValue(f"value_{thread_id}_{i}", i))
            with lock:
                counters["write"] += 1
            time.sleep(0.001)

    def reader_thread(thread_id: int):
        """Read values from container."""
        for i in range(10):
            values = container.value_array(f"value_0_{i}")
            with lock:
                counters["read"] += 1
            time.sleep(0.001)

    # Start threads
    threads: List[threading.Thread] = []

    # Create writer threads
    for i in range(3):
        t = threading.Thread(target=writer_thread, args=(i,))
        threads.append(t)
        t.start()

    # Create reader threads
    for i in range(2):
        t = threading.Thread(target=reader_thread, args=(i,))
        threads.append(t)
        t.start()

    # Wait for completion
    for t in threads:
        t.join()

    print(f"Thread operations completed:")
    print(f"  Writes: {counters['write']}")
    print(f"  Reads: {counters['read']}")
    print(f"  Total values in container: {len(container.units)}\n")


def example_file_io():
    """Demonstrate file I/O operations."""
    print("\n=== File I/O Example ===")

    # Create container
    container = ValueContainer(
        source_id="app",
        target_id="storage",
        message_type="save_request",
    )
    container.add(StringValue("filename", "data.dat"))
    container.add(IntValue("timestamp", 1234567890))

    # Save to file
    filename = "/tmp/container_test.dat"
    container.save_packet(filename)
    print(f"Container saved to {filename}")

    # Load from file
    loaded = ValueContainer()
    loaded.load_packet(filename)
    print(f"Container loaded: {loaded}")
    print(f"Message type: {loaded.message_type}")
    print(f"Source: {loaded.source_id}\n")


def example_value_operations():
    """Demonstrate various value operations."""
    print("\n=== Value Operations Example ===")

    container = ValueContainer(message_type="value_ops")

    # Add multiple values with same name
    container.add(StringValue("tag", "python"))
    container.add(StringValue("tag", "container"))
    container.add(StringValue("tag", "system"))

    # Get all values with same name
    tags = container.value_array("tag")
    print(f"Found {len(tags)} tags:")
    for tag in tags:
        print(f"  - {tag.to_string()}")

    # Remove specific value
    container.remove("tag")
    remaining = container.value_array("tag")
    print(f"After remove, {len(remaining)} tags remain\n")


def main():
    """Run all advanced examples."""
    print("=== Python Container System - Advanced Usage ===")

    example_nested_containers()
    example_bytes_value()
    example_thread_safety()
    example_file_io()
    example_value_operations()

    print("=== All examples completed successfully ===")


if __name__ == "__main__":
    main()
