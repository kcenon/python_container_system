#!/usr/bin/env python3
"""
Basic usage example for python_container_system

Demonstrates creating containers, adding values, and serialization.

Equivalent to C++ examples/basic_usage.cpp
"""

from container_module import ValueContainer
from container_module.values import (
    StringValue,
    IntValue,
    BoolValue,
    DoubleValue,
    ContainerValue,
)


def main():
    """Demonstrate basic container operations."""
    print("=== Python Container System - Basic Usage ===\n")

    # 1. Create a container with header information
    print("1. Creating container with header...")
    container = ValueContainer(
        source_id="client_01",
        source_sub_id="session_123",
        target_id="server",
        target_sub_id="main_handler",
        message_type="user_data",
    )
    print(f"Container created: {container}\n")

    # 2. Add various types of values
    print("2. Adding values to container...")
    container.add(IntValue("user_id", 12345))
    container.add(StringValue("username", "john_doe"))
    container.add(DoubleValue("balance", 1500.75))
    container.add(BoolValue("active", True))
    print(f"Added {len(container.units)} values\n")

    # 3. Retrieve values
    print("3. Retrieving values...")
    user_id = container.get_value("user_id")
    if user_id:
        print(f"User ID: {user_id.to_int()}")

    username = container.get_value("username")
    if username:
        print(f"Username: {username.to_string()}")

    balance = container.get_value("balance")
    if balance:
        print(f"Balance: ${balance.to_double():.2f}")

    active = container.get_value("active")
    if active:
        print(f"Active: {active.to_boolean()}")
    print()

    # 4. Add nested container
    print("4. Adding nested container...")
    address = ContainerValue("address")
    address.add(StringValue("street", "123 Main St"))
    address.add(StringValue("city", "Seattle"))
    address.add(StringValue("zip", "98101"))
    container.add(address)
    print(f"Nested container added with {address.child_count()} fields\n")

    # 5. Serialize container
    print("5. Serializing container...")
    serialized = container.serialize()
    print(f"Serialized length: {len(serialized)} bytes")
    print(f"Preview: {serialized[:100]}...\n")

    # 6. Convert to JSON
    print("6. Converting to JSON...")
    json_str = container.to_json()
    print("JSON output:")
    print(json_str[:200] + "...\n")

    # 7. Swap source and target
    print("7. Swapping source and target...")
    print(f"Before swap: {container.source_id} -> {container.target_id}")
    container.swap_header()
    print(f"After swap: {container.source_id} -> {container.target_id}\n")

    # 8. Create response container (copy without values)
    print("8. Creating response container...")
    response = container.copy(containing_values=False)
    response.set_message_type("user_data_response")
    response.add(StringValue("status", "success"))
    response.add(IntValue("code", 200))
    print(f"Response: {response}")
    print(f"Response values: {len(response.units)}\n")

    # 9. Deserialize from string
    print("9. Testing deserialization...")
    new_container = ValueContainer(data_string=serialized)
    print(f"Deserialized: {new_container}")
    print(f"Message type: {new_container.message_type}")
    print(f"Source: {new_container.source_id}/{new_container.source_sub_id}\n")

    print("=== Example completed successfully ===")


if __name__ == "__main__":
    main()
