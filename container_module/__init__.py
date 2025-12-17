"""
BSD 3-Clause License

Copyright (c) 2021, 🍀☀🌕🌥 🌊
All rights reserved.

Python Container System - A high-performance type-safe container framework
Equivalent to the C++ container_system implementation
"""

__version__ = "1.3.0"
__author__ = "kcenon"
__email__ = "kcenon@naver.com"

from container_module.core.value_types import ValueTypes, convert_value_type
from container_module.core.value import Value
from container_module.core.container import ValueContainer
from container_module.core.value_store import ValueStore
from container_module.messaging.builder import MessagingBuilder
from container_module.di.adapters import (
    IContainerFactory,
    IContainerSerializer,
    DefaultContainerFactory,
    DefaultContainerSerializer,
    serialize_container,
    deserialize_container,
)

__all__ = [
    "ValueTypes",
    "convert_value_type",
    "Value",
    "ValueContainer",
    "ValueStore",
    "MessagingBuilder",
    "IContainerFactory",
    "IContainerSerializer",
    "DefaultContainerFactory",
    "DefaultContainerSerializer",
    "serialize_container",
    "deserialize_container",
]
