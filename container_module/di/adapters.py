"""
Dependency Injection adapters for container system

This module provides DI-compatible factory classes and interfaces
to support modern Python application architectures.

Equivalent to C++ Kcenon module DI patterns.
"""

from __future__ import annotations
from typing import Protocol, Optional, List, runtime_checkable

from container_module.core.value import Value
from container_module.core.container import ValueContainer
from container_module.messaging.builder import MessagingBuilder


@runtime_checkable
class IContainerFactory(Protocol):
    """
    Protocol (interface) for creating ValueContainer instances.

    Provides an abstraction for container creation that can be
    injected into application components, enabling loose coupling
    and testability.

    Example with FastAPI:
        ```python
        from fastapi import Depends

        def get_container_factory() -> IContainerFactory:
            return DefaultContainerFactory()

        @app.post("/messages")
        async def create_message(
            factory: IContainerFactory = Depends(get_container_factory)
        ):
            container = factory.create()
            # ...
        ```
    """

    def create(
        self,
        source_id: str = "",
        source_sub_id: str = "",
        target_id: str = "",
        target_sub_id: str = "",
        message_type: str = "",
    ) -> ValueContainer:
        """
        Create a new ValueContainer instance.

        Args:
            source_id: Source identifier
            source_sub_id: Source sub-identifier
            target_id: Target identifier
            target_sub_id: Target sub-identifier
            message_type: Type of message

        Returns:
            A new ValueContainer instance
        """
        ...

    def create_with_values(
        self,
        values: List[Value],
        source_id: str = "",
        target_id: str = "",
        message_type: str = "",
    ) -> ValueContainer:
        """
        Create a ValueContainer with pre-populated values.

        Args:
            values: List of values to add to the container
            source_id: Source identifier
            target_id: Target identifier
            message_type: Type of message

        Returns:
            A new ValueContainer with the given values
        """
        ...

    def create_from_serialized(
        self,
        data: str,
        parse_only_header: bool = True,
    ) -> ValueContainer:
        """
        Create a ValueContainer from serialized data.

        Args:
            data: Serialized container string
            parse_only_header: If True, only parse header fields

        Returns:
            A ValueContainer deserialized from the data
        """
        ...

    def create_builder(self) -> MessagingBuilder:
        """
        Create a new MessagingBuilder for fluent container construction.

        Returns:
            A new MessagingBuilder instance
        """
        ...


@runtime_checkable
class IContainerSerializer(Protocol):
    """
    Protocol (interface) for serializing/deserializing containers.

    Provides an abstraction for container serialization that can be
    injected into services requiring message encoding/decoding.

    Example:
        ```python
        class MessageService:
            def __init__(self, serializer: IContainerSerializer):
                self._serializer = serializer

            def encode(self, container: ValueContainer) -> str:
                return self._serializer.serialize(container)
        ```
    """

    def serialize(self, container: ValueContainer) -> str:
        """
        Serialize a container to string format.

        Args:
            container: The container to serialize

        Returns:
            Serialized string representation
        """
        ...

    def serialize_bytes(self, container: ValueContainer) -> bytes:
        """
        Serialize a container to bytes.

        Args:
            container: The container to serialize

        Returns:
            Serialized byte representation
        """
        ...

    def deserialize(
        self,
        data: str,
        parse_only_header: bool = True,
    ) -> ValueContainer:
        """
        Deserialize a container from string data.

        Args:
            data: Serialized string data
            parse_only_header: If True, only parse header fields

        Returns:
            Deserialized ValueContainer
        """
        ...

    def deserialize_bytes(
        self,
        data: bytes,
        parse_only_header: bool = True,
    ) -> ValueContainer:
        """
        Deserialize a container from bytes.

        Args:
            data: Serialized byte data
            parse_only_header: If True, only parse header fields

        Returns:
            Deserialized ValueContainer
        """
        ...


class DefaultContainerFactory:
    """
    Default implementation of IContainerFactory.

    Provides standard container creation suitable for most use cases.
    Can be subclassed for custom container creation behavior.

    Example:
        ```python
        factory = DefaultContainerFactory()
        container = factory.create(
            source_id="client1",
            target_id="server1",
            message_type="request"
        )
        ```
    """

    def create(
        self,
        source_id: str = "",
        source_sub_id: str = "",
        target_id: str = "",
        target_sub_id: str = "",
        message_type: str = "",
    ) -> ValueContainer:
        """
        Create a new ValueContainer instance.

        Args:
            source_id: Source identifier
            source_sub_id: Source sub-identifier
            target_id: Target identifier
            target_sub_id: Target sub-identifier
            message_type: Type of message

        Returns:
            A new ValueContainer instance
        """
        return ValueContainer(
            source_id=source_id,
            source_sub_id=source_sub_id,
            target_id=target_id,
            target_sub_id=target_sub_id,
            message_type=message_type,
        )

    def create_with_values(
        self,
        values: List[Value],
        source_id: str = "",
        target_id: str = "",
        message_type: str = "",
    ) -> ValueContainer:
        """
        Create a ValueContainer with pre-populated values.

        Args:
            values: List of values to add to the container
            source_id: Source identifier
            target_id: Target identifier
            message_type: Type of message

        Returns:
            A new ValueContainer with the given values
        """
        container = ValueContainer(
            source_id=source_id,
            target_id=target_id,
            message_type=message_type,
        )
        for value in values:
            container.add(value)
        return container

    def create_from_serialized(
        self,
        data: str,
        parse_only_header: bool = True,
    ) -> ValueContainer:
        """
        Create a ValueContainer from serialized data.

        Args:
            data: Serialized container string
            parse_only_header: If True, only parse header fields

        Returns:
            A ValueContainer deserialized from the data
        """
        return ValueContainer(
            data_string=data,
            parse_only_header=parse_only_header,
        )

    def create_builder(self) -> MessagingBuilder:
        """
        Create a new MessagingBuilder for fluent container construction.

        Returns:
            A new MessagingBuilder instance
        """
        return MessagingBuilder()


class DefaultContainerSerializer:
    """
    Default implementation of IContainerSerializer.

    Provides standard serialization/deserialization using the
    container's built-in methods.

    Example:
        ```python
        serializer = DefaultContainerSerializer()
        data = serializer.serialize(container)
        restored = serializer.deserialize(data, parse_only_header=False)
        ```
    """

    def serialize(self, container: ValueContainer) -> str:
        """
        Serialize a container to string format.

        Args:
            container: The container to serialize

        Returns:
            Serialized string representation
        """
        return container.serialize()

    def serialize_bytes(self, container: ValueContainer) -> bytes:
        """
        Serialize a container to bytes.

        Args:
            container: The container to serialize

        Returns:
            Serialized byte representation
        """
        return container.serialize_array()

    def deserialize(
        self,
        data: str,
        parse_only_header: bool = True,
    ) -> ValueContainer:
        """
        Deserialize a container from string data.

        Args:
            data: Serialized string data
            parse_only_header: If True, only parse header fields

        Returns:
            Deserialized ValueContainer
        """
        return ValueContainer(
            data_string=data,
            parse_only_header=parse_only_header,
        )

    def deserialize_bytes(
        self,
        data: bytes,
        parse_only_header: bool = True,
    ) -> ValueContainer:
        """
        Deserialize a container from bytes.

        Args:
            data: Serialized byte data
            parse_only_header: If True, only parse header fields

        Returns:
            Deserialized ValueContainer
        """
        return ValueContainer(
            data_array=data,
            parse_only_header=parse_only_header,
        )


# Convenience functions for quick serialization without instantiating classes


def serialize_container(container: ValueContainer) -> str:
    """
    Serialize a ValueContainer to string format.

    Convenience function for quick serialization without
    instantiating a serializer class.

    Args:
        container: The container to serialize

    Returns:
        Serialized string representation

    Example:
        ```python
        from container_module.di import serialize_container

        container = ValueContainer(source_id="client1")
        data = serialize_container(container)
        ```
    """
    return container.serialize()


def deserialize_container(
    data: str,
    parse_only_header: bool = True,
) -> ValueContainer:
    """
    Deserialize a ValueContainer from string data.

    Convenience function for quick deserialization without
    instantiating a serializer class.

    Args:
        data: Serialized string data
        parse_only_header: If True, only parse header fields

    Returns:
        Deserialized ValueContainer

    Example:
        ```python
        from container_module.di import deserialize_container

        container = deserialize_container(data, parse_only_header=False)
        print(container.source_id)
        ```
    """
    return ValueContainer(
        data_string=data,
        parse_only_header=parse_only_header,
    )
