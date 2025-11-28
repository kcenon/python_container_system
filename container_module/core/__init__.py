"""
Core module for container system

This module contains the fundamental classes and types:
- ValueTypes: Enumeration of supported value types
- Value: Abstract base class for all values
- ValueContainer: Main container class for message management
- ValueStore: Domain-agnostic value storage (new)
"""

from container_module.core.value_types import ValueTypes, convert_value_type
from container_module.core.value import Value
from container_module.core.container import ValueContainer
from container_module.core.value_store import ValueStore

__all__ = ["ValueTypes", "convert_value_type", "Value", "ValueContainer", "ValueStore"]
