#!/usr/bin/env python3
"""
Dependency Injection example for python_container_system

Demonstrates using DI patterns for container creation and serialization,
including factory patterns and framework integration examples.

Equivalent to C++ DI patterns in Kcenon module.
"""

from container_module import (
    ValueContainer,
    MessagingBuilder,
    IContainerFactory,
    IContainerSerializer,
    DefaultContainerFactory,
    DefaultContainerSerializer,
)
from container_module.values import StringValue, IntValue, DoubleValue, BoolValue


def basic_factory_usage():
    """Demonstrate basic factory usage."""
    print("=== 1. Basic Factory Usage ===\n")

    # Create factory instance
    factory = DefaultContainerFactory()

    # Create container using factory
    container = factory.create(
        source_id="client1",
        target_id="server1",
        message_type="request",
    )

    # Add values
    container.add(StringValue("action", "get_user"))
    container.add(IntValue("user_id", 12345))

    print(f"Created container: {container}")
    print(f"Source: {container.source_id}")
    print(f"Target: {container.target_id}")
    print(f"Type: {container.message_type}")
    print(f"Values: {len(container.units)}\n")


def factory_with_values():
    """Demonstrate creating containers with pre-populated values."""
    print("=== 2. Factory with Pre-populated Values ===\n")

    factory = DefaultContainerFactory()

    # Create container with values in one call
    values = [
        StringValue("name", "John Doe"),
        IntValue("age", 30),
        DoubleValue("balance", 1500.75),
        BoolValue("active", True),
    ]

    container = factory.create_with_values(
        values=values,
        source_id="client",
        target_id="server",
        message_type="user_data",
    )

    print(f"Created container with {len(container.units)} values:")
    for value in container.units:
        print(f"  - {value.name}: {value.to_string()}")
    print()


def factory_with_builder():
    """Demonstrate using builder via factory."""
    print("=== 3. Factory with Builder Pattern ===\n")

    factory = DefaultContainerFactory()

    # Create builder via factory
    container = (
        factory.create_builder()
        .set_source("client1", "session1")
        .set_target("server1", "handler1")
        .set_type("request")
        .add_value(StringValue("command", "process"))
        .add_value(IntValue("priority", 1))
        .build()
    )

    print(f"Built container via factory:")
    print(f"Source: {container.source_id}/{container.source_sub_id}")
    print(f"Target: {container.target_id}/{container.target_sub_id}")
    print(f"Type: {container.message_type}")
    print(f"Values: {len(container.units)}\n")


def serialization_example():
    """Demonstrate serializer usage."""
    print("=== 4. Serialization with DI ===\n")

    factory = DefaultContainerFactory()
    serializer = DefaultContainerSerializer()

    # Create container
    container = factory.create_with_values(
        values=[
            StringValue("message", "Hello, World!"),
            IntValue("count", 42),
        ],
        source_id="sender",
        message_type="greeting",
    )

    # Serialize
    data = serializer.serialize(container)
    print(f"Serialized data length: {len(data)} chars")

    # Deserialize
    restored = serializer.deserialize(data, parse_only_header=False)
    print(f"Restored container:")
    print(f"  Source: {restored.source_id}")
    print(f"  Type: {restored.message_type}")
    message = restored.get_value("message")
    if message:
        print(f"  Message: {message.to_string()}")
    print()


def deserialization_from_factory():
    """Demonstrate deserializing via factory."""
    print("=== 5. Deserialization via Factory ===\n")

    factory = DefaultContainerFactory()

    # Create and serialize a container
    original = factory.create_with_values(
        values=[StringValue("data", "test_value")],
        source_id="original_source",
        message_type="test",
    )
    serialized = original.serialize()

    # Deserialize via factory
    restored = factory.create_from_serialized(
        data=serialized,
        parse_only_header=False,
    )

    print(f"Original source: {original.source_id}")
    print(f"Restored source: {restored.source_id}")
    print(f"Data matches: {original.get_value('data').to_string() == restored.get_value('data').to_string()}\n")


class MockContainerFactory:
    """
    Mock factory for testing.

    Tracks all created containers for test assertions.
    """

    def __init__(self):
        self.created_containers = []
        self.create_call_count = 0

    def create(
        self,
        source_id: str = "",
        source_sub_id: str = "",
        target_id: str = "",
        target_sub_id: str = "",
        message_type: str = "",
    ) -> ValueContainer:
        """Create a container and track it."""
        self.create_call_count += 1
        container = ValueContainer(
            source_id=source_id,
            source_sub_id=source_sub_id,
            target_id=target_id,
            target_sub_id=target_sub_id,
            message_type=message_type,
        )
        self.created_containers.append(container)
        return container

    def create_builder(self) -> MessagingBuilder:
        """Create a new MessagingBuilder."""
        return MessagingBuilder()


class MessageService:
    """Example service that uses DI for container creation."""

    def __init__(self, factory: IContainerFactory):
        self._factory = factory

    def create_request(self, action: str, user_id: int) -> ValueContainer:
        """Create a request container."""
        container = self._factory.create(
            source_id="message_service",
            message_type="request",
        )
        container.add(StringValue("action", action))
        container.add(IntValue("user_id", user_id))
        return container

    def create_response(self, success: bool, message: str) -> ValueContainer:
        """Create a response container."""
        return (
            self._factory.create_builder()
            .set_source("message_service")
            .set_type("response")
            .add_value(BoolValue("success", success))
            .add_value(StringValue("message", message))
            .build()
        )


def mock_factory_example():
    """Demonstrate using mock factory for testing."""
    print("=== 6. Mock Factory for Testing ===\n")

    # Create mock factory
    mock_factory = MockContainerFactory()

    # Create service with mock factory
    service = MessageService(factory=mock_factory)

    # Use service
    request = service.create_request("get_user", 12345)
    response = service.create_response(True, "User found")

    # Verify mock tracked calls
    print(f"Factory create() called: {mock_factory.create_call_count} times")
    print(f"Containers tracked: {len(mock_factory.created_containers)}")
    print(f"Request action: {request.get_value('action').to_string()}")
    print(f"Response success: {response.get_value('success').to_bool()}\n")


def protocol_compliance_example():
    """Demonstrate protocol compliance checking."""
    print("=== 7. Protocol Compliance ===\n")

    # Check if DefaultContainerFactory implements IContainerFactory
    factory = DefaultContainerFactory()
    print(f"DefaultContainerFactory is IContainerFactory: {isinstance(factory, IContainerFactory)}")

    # Check if DefaultContainerSerializer implements IContainerSerializer
    serializer = DefaultContainerSerializer()
    print(f"DefaultContainerSerializer is IContainerSerializer: {isinstance(serializer, IContainerSerializer)}")

    # Check mock factory (also implements protocol via duck typing)
    mock_factory = MockContainerFactory()
    print(f"MockContainerFactory is IContainerFactory: {isinstance(mock_factory, IContainerFactory)}")
    print()


def main():
    """Run all DI examples."""
    print("=" * 60)
    print("Python Container System - Dependency Injection Example")
    print("=" * 60)
    print()

    basic_factory_usage()
    factory_with_values()
    factory_with_builder()
    serialization_example()
    deserialization_from_factory()
    mock_factory_example()
    protocol_compliance_example()

    print("=" * 60)
    print("All DI examples completed successfully!")
    print("=" * 60)


if __name__ == "__main__":
    main()
