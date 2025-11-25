#!/usr/bin/env python3
"""
MessagePack serialization example

Demonstrates using MessagePack for fast, compact binary serialization.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from container_module import ValueContainer
from container_module.values import IntValue, StringValue, FloatValue, BoolValue
from container_module.serializers import MessagePackSerializer


def main():
    print("=" * 70)
    print("MessagePack Serialization Example")
    print("=" * 70)
    print()

    # 1. Basic MessagePack encoding/decoding
    print("1. Basic MessagePack Encoding/Decoding:")
    print("-" * 70)

    data = {
        "name": "Alice",
        "age": 30,
        "active": True,
        "score": 95.5,
        "tags": ["python", "coding", "messagepack"],
        "metadata": {"level": 5, "experience": 1000},
    }

    print(f"Original data: {data}")
    print()

    # Pack to MessagePack
    msgpack_bytes = MessagePackSerializer.pack(data)
    print(f"MessagePack bytes: {len(msgpack_bytes)} bytes")
    print(
        f"Hex: {msgpack_bytes[:50].hex()}..."
        if len(msgpack_bytes) > 50
        else msgpack_bytes.hex()
    )
    print()

    # Unpack from MessagePack
    unpacked = MessagePackSerializer.unpack(msgpack_bytes)
    print(f"Unpacked data: {unpacked}")
    print(f"Match: {data == unpacked}")
    print()

    # 2. Container serialization
    print("2. ValueContainer with MessagePack:")
    print("-" * 70)

    container = ValueContainer(
        source_id="client", target_id="server", message_type="request"
    )

    container.add(StringValue("username", "alice"))
    container.add(IntValue("user_id", 12345))
    container.add(FloatValue("balance", 1234.56))
    container.add(BoolValue("verified", True))

    print(f"Container: {container.message_type}")
    print(f"Values: {len(container.units)}")
    print()

    # Serialize to MessagePack
    msgpack_data = MessagePackSerializer.container_to_msgpack(container)
    print(f"MessagePack size: {len(msgpack_data)} bytes")
    print()

    # Deserialize from MessagePack (header only)
    restored = MessagePackSerializer.msgpack_to_container(msgpack_data)
    print(f"Restored container (header):")
    print(f"  Source: {restored.source_id}")
    print(f"  Target: {restored.target_id}")
    print(f"  Type: {restored.message_type}")
    print()
    print("Note: Full value reconstruction from MessagePack")
    print("      is not yet implemented. Use binary format for")
    print("      complete round-trip serialization.")
    print()

    # 3. Compare serialization formats
    print("3. Format Comparison:")
    print("-" * 70)

    # Binary format
    binary_data = container.serialize()
    print(f"Binary format:      {len(binary_data):>6} bytes")

    # JSON format
    json_data = container.to_json()
    json_bytes = json_data.encode("utf-8") if isinstance(json_data, str) else json_data
    print(
        f"JSON format:        {len(json_bytes):>6} bytes  ({len(json_bytes)/len(binary_data):.1f}x)"
    )

    # MessagePack format
    print(
        f"MessagePack format: {len(msgpack_data):>6} bytes  ({len(msgpack_data)/len(binary_data):.1f}x)"
    )

    # XML format
    xml_data = container.to_xml()
    xml_bytes = xml_data.encode("utf-8") if isinstance(xml_data, str) else xml_data
    print(
        f"XML format:         {len(xml_bytes):>6} bytes  ({len(xml_bytes)/len(binary_data):.1f}x)"
    )
    print()

    print("Summary:")
    print("  MessagePack is more compact than JSON and XML")
    print("  MessagePack is faster to encode/decode than JSON")
    print("  MessagePack is cross-platform and widely supported")
    print("  MessagePack is binary (not human-readable)")
    print()

    # 4. Performance tip
    print("4. When to use MessagePack:")
    print("-" * 70)
    print("  ✓ Network communication (smaller payload)")
    print("  ✓ Storage (compact binary format)")
    print("  ✓ Inter-process communication")
    print("  ✓ API communication (REST/gRPC alternative)")
    print("  ✓ Cross-language data exchange")
    print()
    print("  ✗ Human-readable logs (use JSON)")
    print("  ✗ Configuration files (use JSON/YAML)")
    print("  ✗ Debugging (use JSON for readability)")
    print()

    print("=" * 70)
    print("Example Complete!")
    print("=" * 70)


if __name__ == "__main__":
    main()
