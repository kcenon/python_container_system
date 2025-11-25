"""
BSD 3-Clause License

Copyright (c) 2025, kcenon
All rights reserved.

JSON v2.0 Cross-Language Compatibility Example

This example demonstrates how to use JsonV2Adapter for data interchange
between C++, Python, and .NET container system implementations.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from container_module import ValueContainer
from container_module.core.value import Value
from container_module.values import (
    IntValue,
    LongValue,
    DoubleValue,
    StringValue,
    BytesValue,
    BoolValue,
    ContainerValue,
)
from container_module.adapters import JsonV2Adapter


def example_1_basic_conversion():
    """Example 1: Basic Python container to v2.0 JSON conversion."""
    print("=" * 80)
    print("Example 1: Basic Python Container to JSON v2.0")
    print("=" * 80)

    # Create a container with user data
    container = ValueContainer(
        source_id="python_client",
        source_sub_id="session_001",
        target_id="cpp_server",
        target_sub_id="handler_main",
        message_type="user_profile",
    )

    container.add(IntValue("user_id", 12345))
    container.add(StringValue("username", "john_doe"))
    container.add(StringValue("email", "john@example.com"))
    container.add(DoubleValue("balance", 1500.75))
    container.add(BoolValue("is_active", True))

    # Convert to v2.0 JSON
    v2_json = JsonV2Adapter.to_v2_json(container, pretty=True)
    print("\nJSON v2.0 Output:")
    print(v2_json)

    # Parse back from v2.0 JSON
    restored = JsonV2Adapter.from_v2_json(v2_json)
    print("\nRestored container:")
    print(f"  Message type: {restored.message_type}")
    print(f"  Source: {restored.source_id}.{restored.source_sub_id}")
    print(f"  Target: {restored.target_id}.{restored.target_sub_id}")
    print(f"  Values count: {restored.units.__len__()}")

    # Verify values
    user_id = restored.get_value("user_id")
    username = restored.get_value("username")
    print(f"\n  user_id: {user_id.to_int() if user_id else 'N/A'}")
    print(f"  username: {username.to_string() if username else 'N/A'}")


def example_2_nested_containers():
    """Example 2: Nested containers with v2.0 format."""
    print("\n" + "=" * 80)
    print("Example 2: Nested Containers in JSON v2.0")
    print("=" * 80)

    # Create main container
    main = ValueContainer(
        source_id="python_app",
        target_id="dotnet_service",
        message_type="customer_data",
    )

    main.add(IntValue("customer_id", 9876))
    main.add(StringValue("name", "Alice Johnson"))

    # Create nested address container
    address = ContainerValue("address")
    address.add(StringValue("street", "123 Main St"))
    address.add(StringValue("city", "Seattle"))
    address.add(StringValue("state", "WA"))
    address.add(StringValue("zip", "98101"))
    main.add(address)

    # Create nested contact container
    contact = ContainerValue("contact")
    contact.add(StringValue("phone", "+1-206-555-0123"))
    contact.add(StringValue("email", "alice@example.com"))
    main.add(contact)

    # Convert to v2.0 JSON
    v2_json = JsonV2Adapter.to_v2_json(main, pretty=True)
    print("\nJSON v2.0 with nested containers:")
    print(v2_json)

    # Parse and verify
    restored = JsonV2Adapter.from_v2_json(v2_json)
    address_val = restored.get_value("address")
    if address_val and isinstance(address_val, ContainerValue):
        print(f"\nAddress container has {address_val.child_count()} children:")
        city = address_val.get_value("city")
        print(f"  City: {city.to_string() if city else 'N/A'}")


def example_3_binary_data():
    """Example 3: Binary data with base64 encoding."""
    print("\n" + "=" * 80)
    print("Example 3: Binary Data with Base64 Encoding")
    print("=" * 80)

    # Create container with binary data
    container = ValueContainer(message_type="image_data")
    container.add(StringValue("filename", "avatar.png"))
    container.add(IntValue("size", 2048))

    # Add binary data (simulating image bytes)
    binary_data = bytes([0xFF, 0xD8, 0xFF, 0xE0, 0x00, 0x10, 0x4A, 0x46])
    container.add(BytesValue("image_bytes", binary_data))

    # Convert to v2.0 JSON
    v2_json = JsonV2Adapter.to_v2_json(container, pretty=True)
    print("\nJSON v2.0 with binary data:")
    print(v2_json)

    # Parse and verify binary data
    restored = JsonV2Adapter.from_v2_json(v2_json)
    image_val = restored.get_value("image_bytes")
    if image_val:
        restored_bytes = image_val.to_bytes()
        print(f"\nRestored binary data:")
        print(f"  Original: {binary_data.hex()}")
        print(f"  Restored: {restored_bytes.hex()}")
        print(f"  Match: {binary_data == restored_bytes}")


def example_4_cpp_format_conversion():
    """Example 4: Convert between C++ and Python formats."""
    print("\n" + "=" * 80)
    print("Example 4: C++ Format Conversion")
    print("=" * 80)

    # Simulate C++ JSON format (nested with header object)
    cpp_json = """{
  "header": {
    "target_id": "python_service",
    "target_sub_id": "handler",
    "source_id": "cpp_client",
    "source_sub_id": "main",
    "message_type": "request",
    "version": "1.0.0.0"
  },
  "values": {
    "request_id": {
      "type": 4,
      "data": "42"
    },
    "action": {
      "type": 13,
      "data": "get_user"
    },
    "timeout": {
      "type": 4,
      "data": "30"
    }
  }
}"""

    print("\nOriginal C++ JSON format:")
    print(cpp_json)

    # Parse C++ format
    container = JsonV2Adapter.from_cpp_json(cpp_json)
    print(f"\nParsed container:")
    print(f"  Message type: {container.message_type}")
    print(f"  Source: {container.source_id}")
    print(f"  Target: {container.target_id}")
    print(f"  Values: {container.units.__len__()}")

    # Convert to v2.0 format
    v2_json = JsonV2Adapter.to_v2_json(container, pretty=True)
    print("\nConverted to JSON v2.0:")
    print(v2_json)

    # Convert to Python format
    python_json = container.to_json()
    print("\nConverted to Python flat format:")
    print(python_json)


def example_5_format_detection():
    """Example 5: Automatic format detection and conversion."""
    print("\n" + "=" * 80)
    print("Example 5: Format Detection and Auto-Conversion")
    print("=" * 80)

    # Test different formats
    test_formats = {
        "v2.0": """{
            "container": {
                "version": "2.0",
                "metadata": {
                    "message_type": "test",
                    "protocol_version": "1.0.0.0",
                    "source": {"id": "src", "sub_id": ""},
                    "target": {"id": "tgt", "sub_id": ""}
                },
                "values": [
                    {"name": "key", "type": 13, "type_name": "string", "data": "value"}
                ]
            }
        }""",
        "cpp": """{
            "header": {
                "message_type": "test",
                "source_id": "src",
                "target_id": "tgt"
            },
            "values": {
                "key": {"type": 13, "data": "value"}
            }
        }""",
        "python": """{
            "message_type": "test",
            "source_id": "src",
            "target_id": "tgt",
            "values": [
                {"name": "key", "type": 13, "data": "value"}
            ]
        }""",
    }

    for format_name, json_str in test_formats.items():
        detected = JsonV2Adapter.detect_format(json_str)
        print(f"\n{format_name} format detected as: {detected}")

        # Convert to v2.0
        try:
            v2_json = JsonV2Adapter.convert_format(json_str, "v2.0")
            print(f"   Successfully converted to v2.0")
        except Exception as e:
            print(f"   Conversion failed: {e}")


def example_6_cross_language_workflow():
    """Example 6: Complete cross-language data exchange workflow."""
    print("\n" + "=" * 80)
    print("Example 6: Cross-Language Data Exchange Workflow")
    print("=" * 80)

    print("\nScenario: Python -> C++ -> .NET -> Python")
    print("-" * 80)

    # Step 1: Python creates request
    print("\n[Step 1] Python creates request:")
    python_request = ValueContainer(
        source_id="python_client",
        target_id="cpp_server",
        message_type="data_request",
    )
    python_request.add(IntValue("request_id", 1001))
    python_request.add(StringValue("query", "SELECT * FROM users"))
    print(f"  Created container with {python_request.units.__len__()} values")

    # Convert to v2.0 for transmission
    v2_json = JsonV2Adapter.to_v2_json(python_request)
    print(f"  Serialized to v2.0 JSON ({len(v2_json)} bytes)")

    # Step 2: C++ receives and processes
    print("\n[Step 2] C++ receives and processes (simulated):")
    cpp_received = JsonV2Adapter.from_v2_json(v2_json)
    print(f"  C++ parsed container: {cpp_received.message_type}")
    print(f"  Processing query: {cpp_received.get_value('query').to_string()}")

    # C++ creates response
    cpp_response = ValueContainer(
        source_id="cpp_server",
        target_id="dotnet_middleware",
        message_type="data_response",
    )
    cpp_response.add(IntValue("request_id", 1001))
    cpp_response.add(IntValue("row_count", 42))
    cpp_response.add(StringValue("status", "success"))

    # Convert to C++ JSON format
    cpp_json = JsonV2Adapter.to_cpp_json(cpp_response)
    print(f"  C++ created response in C++ JSON format")

    # Step 3: .NET receives via v2.0
    print("\n[Step 3] .NET receives and enriches (simulated):")
    v2_from_cpp = JsonV2Adapter.convert_format(cpp_json, "v2.0")
    dotnet_received = JsonV2Adapter.from_v2_json(v2_from_cpp)
    print(f"  .NET parsed container: {dotnet_received.message_type}")

    # .NET adds processing info
    dotnet_received.add(StringValue("processed_by", "dotnet_middleware"))
    dotnet_received.add(DoubleValue("processing_time_ms", 15.3))
    dotnet_received.set_target("python_client", "")

    # Step 4: Python receives final result
    print("\n[Step 4] Python receives final result:")
    final_v2_json = JsonV2Adapter.to_v2_json(dotnet_received)
    python_final = JsonV2Adapter.from_v2_json(final_v2_json)
    print(f"  Python received container with {python_final.units.__len__()} values")

    # Display final result
    print("\n  Final values:")
    for value in python_final.units:
        print(f"    {value.name}: {str(value)} (type: {value.type.name})")


def example_7_all_value_types():
    """Example 7: Test all 15 value types in v2.0 format."""
    print("\n" + "=" * 80)
    print("Example 7: All 15 Value Types in JSON v2.0")
    print("=" * 80)

    from container_module.values import (
        ShortValue,
        UShortValue,
        UIntValue,
        ULongValue,
        LLongValue,
        ULLongValue,
        FloatValue,
    )

    container = ValueContainer(message_type="all_types_test")

    # Add all 15 types
    # Note: NULL_VALUE is represented by StringValue with empty string
    container.add(StringValue("null_value", ""))  # NULL_VALUE representation
    container.add(BoolValue("bool_value", True))
    container.add(ShortValue("short_value", -32000))
    container.add(UShortValue("ushort_value", 65000))
    container.add(IntValue("int_value", -2147483648))
    container.add(UIntValue("uint_value", 4294967295))
    container.add(LongValue("long_value", -9223372036854775808))
    container.add(ULongValue("ulong_value", 18446744073709551615))
    container.add(LLongValue("llong_value", -9223372036854775808))
    container.add(ULLongValue("ullong_value", 18446744073709551615))
    container.add(FloatValue("float_value", 3.14159))
    container.add(DoubleValue("double_value", 2.718281828459045))
    container.add(BytesValue("bytes_value", b"\x00\x01\x02\x03\xff"))
    container.add(StringValue("string_value", "Hello, World!"))

    nested = ContainerValue("container_value")
    nested.add(IntValue("nested_int", 42))
    nested.add(StringValue("nested_string", "nested"))
    container.add(nested)

    # Convert to v2.0
    v2_json = JsonV2Adapter.to_v2_json(container, pretty=True)
    print("\nJSON v2.0 with all 15 value types:")
    print(v2_json)

    # Parse and verify
    restored = JsonV2Adapter.from_v2_json(v2_json)
    print(f"\nRestored container has {restored.units.__len__()} values (all 15 types)")

    # Verify critical values
    test_cases = [
        ("short_value", "to_int", -32000),
        ("uint_value", "to_int", 4294967295),
        ("float_value", "to_float", 3.14159),
        ("string_value", "to_string", "Hello, World!"),
    ]

    print("\nVerification:")
    for name, method, expected in test_cases:
        value = restored.get_value(name)
        if value:
            actual = getattr(value, method)()
            match = "" if actual == expected else ""
            print(f"  {match} {name}: {actual}")


def main():
    """Run all examples."""
    print("\n" + "=" * 80)
    print("JSON v2.0 Cross-Language Compatibility Examples")
    print("=" * 80)
    print("\nThese examples demonstrate JSON v2.0 adapter usage for data interchange")
    print("between C++, Python, and .NET container system implementations.")
    print("=" * 80)

    examples = [
        example_1_basic_conversion,
        example_2_nested_containers,
        example_3_binary_data,
        example_4_cpp_format_conversion,
        example_5_format_detection,
        example_6_cross_language_workflow,
        example_7_all_value_types,
    ]

    for i, example_func in enumerate(examples, 1):
        try:
            example_func()
        except Exception as e:
            print(f"\n Example {i} failed: {e}")
            import traceback

            traceback.print_exc()

    print("\n" + "=" * 80)
    print("All examples completed")
    print("=" * 80)


if __name__ == "__main__":
    main()
