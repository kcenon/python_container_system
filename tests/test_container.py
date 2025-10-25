"""
Tests for ValueContainer class
"""

import pytest
from container_module import ValueContainer
from container_module.values import StringValue, IntValue, BoolValue


class TestValueContainer:
    """Test ValueContainer class functionality."""

    def test_default_constructor(self):
        """Test default container creation."""
        container = ValueContainer()
        assert container.source_id == ""
        assert container.target_id == ""
        assert container.message_type == "data_container"
        assert container.version == "1.0.0.0"
        assert len(container.units) == 0

    def test_constructor_with_parameters(self):
        """Test container creation with parameters."""
        container = ValueContainer(
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

    def test_set_source_target(self):
        """Test setting source and target."""
        container = ValueContainer()
        container.set_source("src1", "sub1")
        container.set_target("tgt1", "sub2")

        assert container.source_id == "src1"
        assert container.source_sub_id == "sub1"
        assert container.target_id == "tgt1"
        assert container.target_sub_id == "sub2"

    def test_swap_header(self):
        """Test swapping source and target."""
        container = ValueContainer(
            source_id="src", source_sub_id="src_sub",
            target_id="tgt", target_sub_id="tgt_sub",
        )
        container.swap_header()

        assert container.source_id == "tgt"
        assert container.source_sub_id == "tgt_sub"
        assert container.target_id == "src"
        assert container.target_sub_id == "src_sub"

    def test_add_value(self):
        """Test adding values to container."""
        container = ValueContainer()

        val1 = StringValue("name", "John")
        val2 = IntValue("age", 30)
        val3 = BoolValue("active", True)

        container.add(val1)
        container.add(val2)
        container.add(val3)

        assert len(container.units) == 3
        assert container.get_value("name") == val1
        assert container.get_value("age") == val2
        assert container.get_value("active") == val3

    def test_value_array(self):
        """Test getting all values with same name."""
        container = ValueContainer()

        val1 = StringValue("tag", "tag1")
        val2 = StringValue("tag", "tag2")
        val3 = StringValue("name", "test")

        container.add(val1)
        container.add(val2)
        container.add(val3)

        tags = container.value_array("tag")
        assert len(tags) == 2
        assert val1 in tags
        assert val2 in tags

    def test_remove_value_by_name(self):
        """Test removing values by name."""
        container = ValueContainer()

        val1 = StringValue("name", "John")
        val2 = IntValue("age", 30)

        container.add(val1)
        container.add(val2)
        assert len(container.units) == 2

        container.remove("name")
        assert len(container.units) == 1
        assert container.get_value("name") is None
        assert container.get_value("age") == val2

    def test_clear_value(self):
        """Test clearing all values."""
        container = ValueContainer()
        container.add(StringValue("name", "John"))
        container.add(IntValue("age", 30))

        assert len(container.units) == 2

        container.clear_value()
        assert len(container.units) == 0

    def test_serialize_deserialize(self):
        """Test serialization and deserialization."""
        container = ValueContainer(
            source_id="src",
            target_id="tgt",
            message_type="test",
        )
        container.add(StringValue("name", "Test"))

        # Serialize
        serialized = container.serialize()
        assert isinstance(serialized, str)
        assert "source_id=src" in serialized
        assert "target_id=tgt" in serialized
        assert "message_type=test" in serialized

        # Deserialize
        new_container = ValueContainer(data_string=serialized)
        assert new_container.source_id == "src"
        assert new_container.target_id == "tgt"
        assert new_container.message_type == "test"

    def test_to_json(self):
        """Test JSON conversion."""
        container = ValueContainer(message_type="test")
        container.add(StringValue("name", "John"))
        container.add(IntValue("age", 30))

        json_str = container.to_json()
        assert isinstance(json_str, str)
        assert "message_type" in json_str
        assert "test" in json_str

    def test_to_xml(self):
        """Test XML conversion."""
        container = ValueContainer(message_type="test")
        container.add(StringValue("name", "John"))

        xml_str = container.to_xml()
        assert isinstance(xml_str, str)
        assert "container" in xml_str
        assert "message_type" in xml_str

    def test_copy(self):
        """Test container copying."""
        container = ValueContainer(
            source_id="src",
            message_type="test",
        )
        val1 = StringValue("name", "John")
        container.add(val1)

        # Copy with values
        copy1 = container.copy(containing_values=True)
        assert copy1.source_id == "src"
        assert copy1.message_type == "test"
        assert len(copy1.units) == 1

        # Copy without values
        copy2 = container.copy(containing_values=False)
        assert copy2.source_id == "src"
        assert copy2.message_type == "test"
        assert len(copy2.units) == 0

    def test_initialize(self):
        """Test container reinitialization."""
        container = ValueContainer(
            source_id="src",
            target_id="tgt",
            message_type="test",
        )
        container.add(StringValue("name", "John"))

        container.initialize()

        assert container.source_id == ""
        assert container.target_id == ""
        assert container.message_type == "data_container"
        assert len(container.units) == 0

    def test_getitem_operator(self):
        """Test [] operator for getting values."""
        container = ValueContainer()
        val1 = StringValue("name", "John")
        val2 = StringValue("name", "Jane")

        container.add(val1)
        container.add(val2)

        values = container["name"]
        assert len(values) == 2
        assert val1 in values
        assert val2 in values
