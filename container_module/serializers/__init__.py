"""
Serializers for Container System

Provides various serialization formats:
- Binary (default, fastest)
- JSON (human-readable)
- XML (interoperable)
- MessagePack (compact binary)
"""

from container_module.serializers.messagepack_serializer import MessagePackSerializer

__all__ = ["MessagePackSerializer"]
