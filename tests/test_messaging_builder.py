"""
Tests for MessagingBuilder class
"""

import pytest
from container_module.messaging import MessagingBuilder
from container_module.values import StringValue, IntValue, BoolValue


class TestMessagingBuilder:
    """Test MessagingBuilder class functionality."""

    def test_default_builder(self):
        """Test default builder creates empty container."""
        builder = MessagingBuilder()
        container = builder.build()

        assert container.source_id == ""
        assert container.source_sub_id == ""
        assert container.target_id == ""
        assert container.target_sub_id == ""
        assert container.message_type == "data_container"
        assert len(container.units) == 0

    def test_set_source(self):
        """Test setting source identifiers."""
        container = MessagingBuilder().set_source("client1", "session1").build()

        assert container.source_id == "client1"
        assert container.source_sub_id == "session1"

    def test_set_source_without_sub_id(self):
        """Test setting source with only main ID."""
        container = MessagingBuilder().set_source("client1").build()

        assert container.source_id == "client1"
        assert container.source_sub_id == ""

    def test_set_target(self):
        """Test setting target identifiers."""
        container = MessagingBuilder().set_target("server1", "handler1").build()

        assert container.target_id == "server1"
        assert container.target_sub_id == "handler1"

    def test_set_target_without_sub_id(self):
        """Test setting target with only main ID."""
        container = MessagingBuilder().set_target("server1").build()

        assert container.target_id == "server1"
        assert container.target_sub_id == ""

    def test_set_type(self):
        """Test setting message type."""
        container = MessagingBuilder().set_type("request").build()

        assert container.message_type == "request"

    def test_method_chaining(self):
        """Test full method chaining workflow."""
        container = (
            MessagingBuilder()
            .set_source("client1", "session1")
            .set_target("server1", "handler1")
            .set_type("request")
            .build()
        )

        assert container.source_id == "client1"
        assert container.source_sub_id == "session1"
        assert container.target_id == "server1"
        assert container.target_sub_id == "handler1"
        assert container.message_type == "request"

    def test_add_value(self):
        """Test adding single value."""
        container = (
            MessagingBuilder()
            .set_type("test")
            .add_value(StringValue("name", "John"))
            .build()
        )

        assert len(container.units) == 1
        assert container.get_value("name") is not None

    def test_add_multiple_values(self):
        """Test adding multiple values via chaining."""
        container = (
            MessagingBuilder()
            .set_type("test")
            .add_value(StringValue("name", "John"))
            .add_value(IntValue("age", 30))
            .add_value(BoolValue("active", True))
            .build()
        )

        assert len(container.units) == 3
        assert container.get_value("name") is not None
        assert container.get_value("age") is not None
        assert container.get_value("active") is not None

    def test_add_values_list(self):
        """Test adding multiple values at once."""
        values = [
            StringValue("name", "John"),
            IntValue("age", 30),
        ]

        container = MessagingBuilder().set_type("test").add_values(values).build()

        assert len(container.units) == 2

    def test_builder_returns_self(self):
        """Test that all setter methods return the builder instance."""
        builder = MessagingBuilder()

        result1 = builder.set_source("src", "sub")
        result2 = builder.set_target("tgt", "sub")
        result3 = builder.set_type("test")
        result4 = builder.add_value(StringValue("key", "value"))
        result5 = builder.add_values([])

        assert result1 is builder
        assert result2 is builder
        assert result3 is builder
        assert result4 is builder
        assert result5 is builder

    def test_reset(self):
        """Test builder reset functionality."""
        builder = (
            MessagingBuilder()
            .set_source("client1", "session1")
            .set_target("server1", "handler1")
            .set_type("request")
            .add_value(StringValue("name", "John"))
        )

        # Reset and build new container
        container = builder.reset().set_type("response").build()

        assert container.source_id == ""
        assert container.source_sub_id == ""
        assert container.target_id == ""
        assert container.target_sub_id == ""
        assert container.message_type == "response"
        assert len(container.units) == 0

    def test_builder_reuse(self):
        """Test that builder can be reused after reset."""
        builder = MessagingBuilder()

        # Build first container
        container1 = builder.set_source("client1").set_type("request").build()

        # Reset and build second container
        container2 = builder.reset().set_source("client2").set_type("response").build()

        assert container1.source_id == "client1"
        assert container1.message_type == "request"
        assert container2.source_id == "client2"
        assert container2.message_type == "response"

    def test_built_container_is_functional(self):
        """Test that built container works correctly."""
        container = (
            MessagingBuilder()
            .set_source("src", "sub_src")
            .set_target("tgt", "sub_tgt")
            .set_type("test_message")
            .add_value(StringValue("data", "test_data"))
            .build()
        )

        # Test serialization
        serialized = container.serialize()
        assert "@header={{" in serialized
        assert "@data={{" in serialized

        # Test deserialization
        from container_module import ValueContainer

        new_container = ValueContainer(data_string=serialized, parse_only_header=False)
        assert new_container.source_id == "src"
        assert new_container.target_id == "tgt"
        assert new_container.message_type == "test_message"
