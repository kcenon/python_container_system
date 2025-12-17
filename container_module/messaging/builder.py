"""
MessagingBuilder class for container system

This module provides a builder pattern for creating ValueContainer instances
with fluent API for setting message headers.

Equivalent to C++ messaging builder pattern.
"""

from __future__ import annotations
from typing import List, Optional

from container_module.core.value import Value
from container_module.core.container import ValueContainer


class MessagingBuilder:
    """
    Builder class for creating ValueContainer instances with fluent API.

    Provides method chaining for setting source, target, message type,
    and values before building a fully configured ValueContainer.

    Example:
        container = (
            MessagingBuilder()
            .set_source("client1", "session1")
            .set_target("server1", "handler1")
            .set_type("request")
            .add_value(StringValue("name", "John"))
            .build()
        )
    """

    def __init__(self) -> None:
        """Initialize a new MessagingBuilder with default values."""
        self._source_id: str = ""
        self._source_sub_id: str = ""
        self._target_id: str = ""
        self._target_sub_id: str = ""
        self._message_type: str = ""
        self._values: List[Value] = []

    def set_source(self, source_id: str, source_sub_id: str = "") -> MessagingBuilder:
        """
        Set the source identifier for the message.

        Args:
            source_id: Source identifier
            source_sub_id: Source sub-identifier (optional)

        Returns:
            Self for method chaining
        """
        self._source_id = source_id
        self._source_sub_id = source_sub_id
        return self

    def set_target(self, target_id: str, target_sub_id: str = "") -> MessagingBuilder:
        """
        Set the target identifier for the message.

        Args:
            target_id: Target identifier
            target_sub_id: Target sub-identifier (optional)

        Returns:
            Self for method chaining
        """
        self._target_id = target_id
        self._target_sub_id = target_sub_id
        return self

    def set_type(self, message_type: str) -> MessagingBuilder:
        """
        Set the message type.

        Args:
            message_type: Type of message

        Returns:
            Self for method chaining
        """
        self._message_type = message_type
        return self

    def add_value(self, value: Value) -> MessagingBuilder:
        """
        Add a value to the message.

        Args:
            value: Value to add

        Returns:
            Self for method chaining
        """
        self._values.append(value)
        return self

    def add_values(self, values: List[Value]) -> MessagingBuilder:
        """
        Add multiple values to the message.

        Args:
            values: List of values to add

        Returns:
            Self for method chaining
        """
        self._values.extend(values)
        return self

    def build(self) -> ValueContainer:
        """
        Build and return the configured ValueContainer.

        Returns:
            A new ValueContainer with the configured settings
        """
        container = ValueContainer(
            source_id=self._source_id,
            source_sub_id=self._source_sub_id,
            target_id=self._target_id,
            target_sub_id=self._target_sub_id,
            message_type=self._message_type,
        )

        for value in self._values:
            container.add(value)

        return container

    def reset(self) -> MessagingBuilder:
        """
        Reset the builder to default state for reuse.

        Returns:
            Self for method chaining
        """
        self._source_id = ""
        self._source_sub_id = ""
        self._target_id = ""
        self._target_sub_id = ""
        self._message_type = ""
        self._values.clear()
        return self
