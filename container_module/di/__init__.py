"""
Dependency Injection support module for container system

This module provides DI-compatible factory classes to support modern
Python application architectures like FastAPI.

Equivalent to C++ Kcenon module DI patterns.
"""

from container_module.di.adapters import (
    IContainerFactory,
    IContainerSerializer,
    DefaultContainerFactory,
    DefaultContainerSerializer,
    serialize_container,
    deserialize_container,
)

__all__ = [
    "IContainerFactory",
    "IContainerSerializer",
    "DefaultContainerFactory",
    "DefaultContainerSerializer",
    "serialize_container",
    "deserialize_container",
]
