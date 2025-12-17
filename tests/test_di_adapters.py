"""
Tests for Dependency Injection adapters
"""

import pytest
from container_module.di import (
    IContainerFactory,
    IContainerSerializer,
    DefaultContainerFactory,
    DefaultContainerSerializer,
    serialize_container,
    deserialize_container,
)
from container_module.values import StringValue, IntValue
from container_module import ValueContainer, MessagingBuilder


class TestIContainerFactoryProtocol:
    """Test IContainerFactory Protocol definition."""

    def test_default_factory_implements_protocol(self):
        """Test that DefaultContainerFactory implements IContainerFactory."""
        factory = DefaultContainerFactory()
        assert isinstance(factory, IContainerFactory)

    def test_custom_factory_implements_protocol(self):
        """Test that custom factory can implement IContainerFactory."""

        class CustomFactory:
            def create(
                self,
                source_id: str = "",
                source_sub_id: str = "",
                target_id: str = "",
                target_sub_id: str = "",
                message_type: str = "",
            ) -> ValueContainer:
                container = ValueContainer(
                    source_id=source_id,
                    message_type=message_type or "custom_type",
                )
                return container

            def create_with_values(
                self, values, source_id="", target_id="", message_type=""
            ):
                return ValueContainer()

            def create_from_serialized(self, data, parse_only_header=True):
                return ValueContainer(data_string=data)

            def create_builder(self):
                return MessagingBuilder()

        custom = CustomFactory()
        assert isinstance(custom, IContainerFactory)


class TestIContainerSerializerProtocol:
    """Test IContainerSerializer Protocol definition."""

    def test_default_serializer_implements_protocol(self):
        """Test that DefaultContainerSerializer implements IContainerSerializer."""
        serializer = DefaultContainerSerializer()
        assert isinstance(serializer, IContainerSerializer)


class TestDefaultContainerFactory:
    """Test DefaultContainerFactory class functionality."""

    def test_create_empty_container(self):
        """Test creating an empty container."""
        factory = DefaultContainerFactory()
        container = factory.create()

        assert container.source_id == ""
        assert container.target_id == ""
        assert container.message_type == "data_container"

    def test_create_with_identifiers(self):
        """Test creating a container with identifiers."""
        factory = DefaultContainerFactory()
        container = factory.create(
            source_id="client1",
            source_sub_id="session1",
            target_id="server1",
            target_sub_id="handler1",
            message_type="request",
        )

        assert container.source_id == "client1"
        assert container.source_sub_id == "session1"
        assert container.target_id == "server1"
        assert container.target_sub_id == "handler1"
        assert container.message_type == "request"

    def test_create_with_values(self):
        """Test creating a container with pre-populated values."""
        factory = DefaultContainerFactory()
        values = [
            StringValue("name", "John"),
            IntValue("age", 30),
        ]
        container = factory.create_with_values(
            values=values,
            source_id="client1",
            message_type="user_data",
        )

        assert container.source_id == "client1"
        assert container.message_type == "user_data"
        assert len(container.units) == 2
        assert container.get_value("name") is not None
        assert container.get_value("age") is not None

    def test_create_from_serialized(self):
        """Test creating a container from serialized data."""
        factory = DefaultContainerFactory()

        # Create and serialize a container
        original = factory.create(
            source_id="src1",
            target_id="tgt1",
            message_type="test_msg",
        )
        original.add(StringValue("key", "value"))
        serialized = original.serialize()

        # Deserialize
        restored = factory.create_from_serialized(serialized, parse_only_header=False)

        assert restored.source_id == "src1"
        assert restored.target_id == "tgt1"
        assert restored.message_type == "test_msg"

    def test_create_builder(self):
        """Test creating a MessagingBuilder."""
        factory = DefaultContainerFactory()
        builder = factory.create_builder()

        assert isinstance(builder, MessagingBuilder)

        container = builder.set_source("client1").set_type("test").build()
        assert container.source_id == "client1"


class TestDefaultContainerSerializer:
    """Test DefaultContainerSerializer class functionality."""

    def test_serialize_container(self):
        """Test serializing a container to string."""
        serializer = DefaultContainerSerializer()
        container = ValueContainer(source_id="client1", message_type="test")
        container.add(StringValue("name", "John"))

        data = serializer.serialize(container)

        assert "@header={{" in data
        assert "@data={{" in data
        assert "client1" in data

    def test_serialize_bytes(self):
        """Test serializing a container to bytes."""
        serializer = DefaultContainerSerializer()
        container = ValueContainer(source_id="client1")

        data = serializer.serialize_bytes(container)

        assert isinstance(data, bytes)
        assert b"client1" in data

    def test_deserialize_string(self):
        """Test deserializing a container from string."""
        serializer = DefaultContainerSerializer()
        container = ValueContainer(source_id="src1", target_id="tgt1")
        container.add(StringValue("key", "value"))
        serialized = container.serialize()

        restored = serializer.deserialize(serialized, parse_only_header=False)

        assert restored.source_id == "src1"
        assert restored.target_id == "tgt1"

    def test_deserialize_bytes(self):
        """Test deserializing a container from bytes."""
        serializer = DefaultContainerSerializer()
        container = ValueContainer(source_id="src1")
        serialized = container.serialize_array()

        restored = serializer.deserialize_bytes(serialized, parse_only_header=False)

        assert restored.source_id == "src1"

    def test_roundtrip_serialization(self):
        """Test complete serialization roundtrip."""
        serializer = DefaultContainerSerializer()
        original = ValueContainer(
            source_id="client1",
            target_id="server1",
            message_type="request",
        )
        original.add(StringValue("name", "John"))
        original.add(IntValue("age", 30))

        # String roundtrip
        serialized = serializer.serialize(original)
        restored = serializer.deserialize(serialized, parse_only_header=False)

        assert restored.source_id == original.source_id
        assert restored.target_id == original.target_id
        assert restored.message_type == original.message_type

        # Bytes roundtrip
        serialized_bytes = serializer.serialize_bytes(original)
        restored_bytes = serializer.deserialize_bytes(
            serialized_bytes, parse_only_header=False
        )

        assert restored_bytes.source_id == original.source_id


class TestConvenienceFunctions:
    """Test convenience functions for serialization."""

    def test_serialize_container_function(self):
        """Test serialize_container convenience function."""
        container = ValueContainer(source_id="client1")

        data = serialize_container(container)

        assert "@header={{" in data
        assert "client1" in data

    def test_deserialize_container_function(self):
        """Test deserialize_container convenience function."""
        container = ValueContainer(source_id="src1", target_id="tgt1")
        serialized = container.serialize()

        restored = deserialize_container(serialized, parse_only_header=False)

        assert restored.source_id == "src1"
        assert restored.target_id == "tgt1"


class TestMockDIScenario:
    """Test DI integration with mock DI scenario."""

    def test_dependency_injection_pattern(self):
        """Test factory injection pattern similar to FastAPI."""

        class MessageService:
            """Mock service that uses injected factory."""

            def __init__(self, factory: IContainerFactory):
                self._factory = factory

            def create_request(
                self, source: str, target: str, payload: str
            ) -> ValueContainer:
                return (
                    self._factory.create_builder()
                    .set_source(source)
                    .set_target(target)
                    .set_type("request")
                    .add_value(StringValue("payload", payload))
                    .build()
                )

        # Inject factory into service
        factory = DefaultContainerFactory()
        service = MessageService(factory)

        # Use service
        container = service.create_request("client1", "server1", "Hello")

        assert container.source_id == "client1"
        assert container.target_id == "server1"
        assert container.message_type == "request"
        assert container.get_value("payload") is not None

    def test_serializer_injection_pattern(self):
        """Test serializer injection pattern."""

        class MessageEncoder:
            """Mock encoder that uses injected serializer."""

            def __init__(self, serializer: IContainerSerializer):
                self._serializer = serializer

            def encode(self, container: ValueContainer) -> str:
                return self._serializer.serialize(container)

            def decode(self, data: str) -> ValueContainer:
                return self._serializer.deserialize(data, parse_only_header=False)

        # Inject serializer
        serializer = DefaultContainerSerializer()
        encoder = MessageEncoder(serializer)

        # Create and encode
        container = ValueContainer(source_id="test")
        container.add(StringValue("data", "test_value"))

        encoded = encoder.encode(container)
        decoded = encoder.decode(encoded)

        assert decoded.source_id == "test"

    def test_mock_factory_for_testing(self):
        """Test using mock factory for unit testing."""

        class MockContainerFactory:
            """Mock factory for testing that tracks calls."""

            def __init__(self):
                self.create_calls = []
                self.builder_calls = 0

            def create(
                self,
                source_id: str = "",
                source_sub_id: str = "",
                target_id: str = "",
                target_sub_id: str = "",
                message_type: str = "",
            ) -> ValueContainer:
                self.create_calls.append(
                    {
                        "source_id": source_id,
                        "target_id": target_id,
                        "message_type": message_type,
                    }
                )
                return ValueContainer(
                    source_id=source_id,
                    target_id=target_id,
                    message_type=message_type,
                )

            def create_with_values(
                self, values, source_id="", target_id="", message_type=""
            ):
                return ValueContainer()

            def create_from_serialized(self, data, parse_only_header=True):
                return ValueContainer(data_string=data)

            def create_builder(self):
                self.builder_calls += 1
                return MessagingBuilder()

        # Use mock factory
        mock = MockContainerFactory()
        assert isinstance(mock, IContainerFactory)

        mock.create(source_id="test", message_type="msg")
        mock.create_builder()

        assert len(mock.create_calls) == 1
        assert mock.create_calls[0]["source_id"] == "test"
        assert mock.builder_calls == 1

    def test_factory_as_provider(self):
        """Test factory used as dependency provider."""

        def get_container_factory() -> IContainerFactory:
            """Dependency provider function."""
            return DefaultContainerFactory()

        # Simulate dependency resolution
        factory = get_container_factory()
        container = factory.create(source_id="resolved")

        assert container.source_id == "resolved"


class TestModuleExports:
    """Test that DI module exports are accessible."""

    def test_imports_from_di_module(self):
        """Test importing from container_module.di."""
        from container_module.di import (
            IContainerFactory,
            IContainerSerializer,
            DefaultContainerFactory,
            DefaultContainerSerializer,
            serialize_container,
            deserialize_container,
        )

        # Verify all imports are accessible
        assert IContainerFactory is not None
        assert IContainerSerializer is not None
        assert DefaultContainerFactory is not None
        assert DefaultContainerSerializer is not None
        assert serialize_container is not None
        assert deserialize_container is not None

    def test_imports_from_main_module(self):
        """Test importing from container_module (main)."""
        from container_module import (
            IContainerFactory,
            IContainerSerializer,
            DefaultContainerFactory,
            DefaultContainerSerializer,
            serialize_container,
            deserialize_container,
        )

        # Verify all imports are accessible from main module
        factory = DefaultContainerFactory()
        assert isinstance(factory, IContainerFactory)
