"""
MessagePack serialization for Container System

MessagePack is a binary serialization format that is:
- Faster than JSON
- More compact than JSON
- Cross-platform compatible
- Not human-readable (binary format)

This implementation does NOT require the msgpack library.
It implements a minimal MessagePack encoder/decoder for basic types.
"""

import struct
from typing import Any, List, Dict, Union
from container_module.core.value import Value
from container_module.core.container import ValueContainer
from container_module.core.value_types import ValueTypes


class MessagePackSerializer:
    """
    Pure Python MessagePack serializer (no external dependencies).

    Supports MessagePack format:
    - fixint: 0x00-0x7f (positive), 0xe0-0xff (negative)
    - nil: 0xc0
    - false/true: 0xc2/0xc3
    - bin8/bin16/bin32: 0xc4/0xc5/0xc6
    - float32/float64: 0xca/0xcb
    - uint8/uint16/uint32/uint64: 0xcc/0xcd/0xce/0xcf
    - int8/int16/int32/int64: 0xd0/0xd1/0xd2/0xd3
    - fixstr: 0xa0-0xbf
    - str8/str16/str32: 0xd9/0xda/0xdb
    - fixarray: 0x90-0x9f
    - array16/array32: 0xdc/0xdd
    - fixmap: 0x80-0x8f
    - map16/map32: 0xde/0xdf
    """

    # MessagePack type codes
    NIL = 0xC0
    FALSE = 0xC2
    TRUE = 0xC3
    BIN8 = 0xC4
    BIN16 = 0xC5
    BIN32 = 0xC6
    FLOAT32 = 0xCA
    FLOAT64 = 0xCB
    UINT8 = 0xCC
    UINT16 = 0xCD
    UINT32 = 0xCE
    UINT64 = 0xCF
    INT8 = 0xD0
    INT16 = 0xD1
    INT32 = 0xD2
    INT64 = 0xD3
    STR8 = 0xD9
    STR16 = 0xDA
    STR32 = 0xDB
    ARRAY16 = 0xDC
    ARRAY32 = 0xDD
    MAP16 = 0xDE
    MAP32 = 0xDF

    @staticmethod
    def pack(obj: Any) -> bytes:
        """Pack a Python object into MessagePack format."""
        if obj is None:
            return bytes([MessagePackSerializer.NIL])

        elif isinstance(obj, bool):
            return bytes(
                [MessagePackSerializer.TRUE if obj else MessagePackSerializer.FALSE]
            )

        elif isinstance(obj, int):
            return MessagePackSerializer._pack_int(obj)

        elif isinstance(obj, float):
            return MessagePackSerializer._pack_float(obj)

        elif isinstance(obj, str):
            return MessagePackSerializer._pack_str(obj)

        elif isinstance(obj, bytes):
            return MessagePackSerializer._pack_bin(obj)

        elif isinstance(obj, list):
            return MessagePackSerializer._pack_array(obj)

        elif isinstance(obj, dict):
            return MessagePackSerializer._pack_map(obj)

        else:
            raise TypeError(f"Unsupported type for MessagePack: {type(obj)}")

    @staticmethod
    def _pack_int(n: int) -> bytes:
        """Pack an integer."""
        if 0 <= n <= 0x7F:
            # Positive fixint
            return bytes([n])
        elif -32 <= n < 0:
            # Negative fixint
            return bytes([0x100 + n])
        elif 0 <= n <= 0xFF:
            return bytes([MessagePackSerializer.UINT8, n])
        elif 0 <= n <= 0xFFFF:
            return bytes([MessagePackSerializer.UINT16]) + struct.pack(">H", n)
        elif 0 <= n <= 0xFFFFFFFF:
            return bytes([MessagePackSerializer.UINT32]) + struct.pack(">I", n)
        elif 0 <= n <= 0xFFFFFFFFFFFFFFFF:
            return bytes([MessagePackSerializer.UINT64]) + struct.pack(">Q", n)
        elif -0x80 <= n < 0:
            return bytes([MessagePackSerializer.INT8]) + struct.pack("b", n)
        elif -0x8000 <= n < 0:
            return bytes([MessagePackSerializer.INT16]) + struct.pack(">h", n)
        elif -0x80000000 <= n < 0:
            return bytes([MessagePackSerializer.INT32]) + struct.pack(">i", n)
        else:
            return bytes([MessagePackSerializer.INT64]) + struct.pack(">q", n)

    @staticmethod
    def _pack_float(f: float) -> bytes:
        """Pack a float (always as float64 for precision)."""
        return bytes([MessagePackSerializer.FLOAT64]) + struct.pack(">d", f)

    @staticmethod
    def _pack_str(s: str) -> bytes:
        """Pack a string."""
        data = s.encode("utf-8")
        length = len(data)

        if length <= 31:
            # fixstr
            return bytes([0xA0 | length]) + data
        elif length <= 0xFF:
            return bytes([MessagePackSerializer.STR8, length]) + data
        elif length <= 0xFFFF:
            return (
                bytes([MessagePackSerializer.STR16]) + struct.pack(">H", length) + data
            )
        else:
            return (
                bytes([MessagePackSerializer.STR32]) + struct.pack(">I", length) + data
            )

    @staticmethod
    def _pack_bin(b: bytes) -> bytes:
        """Pack binary data."""
        length = len(b)

        if length <= 0xFF:
            return bytes([MessagePackSerializer.BIN8, length]) + b
        elif length <= 0xFFFF:
            return bytes([MessagePackSerializer.BIN16]) + struct.pack(">H", length) + b
        else:
            return bytes([MessagePackSerializer.BIN32]) + struct.pack(">I", length) + b

    @staticmethod
    def _pack_array(arr: list) -> bytes:
        """Pack an array."""
        length = len(arr)

        if length <= 15:
            # fixarray
            header = bytes([0x90 | length])
        elif length <= 0xFFFF:
            header = bytes([MessagePackSerializer.ARRAY16]) + struct.pack(">H", length)
        else:
            header = bytes([MessagePackSerializer.ARRAY32]) + struct.pack(">I", length)

        return header + b"".join(MessagePackSerializer.pack(item) for item in arr)

    @staticmethod
    def _pack_map(m: dict) -> bytes:
        """Pack a map/dictionary."""
        length = len(m)

        if length <= 15:
            # fixmap
            header = bytes([0x80 | length])
        elif length <= 0xFFFF:
            header = bytes([MessagePackSerializer.MAP16]) + struct.pack(">H", length)
        else:
            header = bytes([MessagePackSerializer.MAP32]) + struct.pack(">I", length)

        items = b"".join(
            MessagePackSerializer.pack(k) + MessagePackSerializer.pack(v)
            for k, v in m.items()
        )

        return header + items

    @staticmethod
    def unpack(data: bytes) -> Any:
        """Unpack MessagePack data into Python object."""
        result, _ = MessagePackSerializer._unpack_one(data, 0)
        return result

    @staticmethod
    def _unpack_one(data: bytes, offset: int) -> tuple:
        """Unpack one MessagePack object, return (value, new_offset)."""
        if offset >= len(data):
            raise ValueError("Unexpected end of data")

        code = data[offset]
        offset += 1

        # Positive fixint
        if 0x00 <= code <= 0x7F:
            return code, offset

        # Negative fixint
        elif 0xE0 <= code <= 0xFF:
            return code - 0x100, offset

        # nil
        elif code == MessagePackSerializer.NIL:
            return None, offset

        # bool
        elif code == MessagePackSerializer.FALSE:
            return False, offset
        elif code == MessagePackSerializer.TRUE:
            return True, offset

        # unsigned ints
        elif code == MessagePackSerializer.UINT8:
            return data[offset], offset + 1
        elif code == MessagePackSerializer.UINT16:
            return struct.unpack(">H", data[offset : offset + 2])[0], offset + 2
        elif code == MessagePackSerializer.UINT32:
            return struct.unpack(">I", data[offset : offset + 4])[0], offset + 4
        elif code == MessagePackSerializer.UINT64:
            return struct.unpack(">Q", data[offset : offset + 8])[0], offset + 8

        # signed ints
        elif code == MessagePackSerializer.INT8:
            return struct.unpack("b", data[offset : offset + 1])[0], offset + 1
        elif code == MessagePackSerializer.INT16:
            return struct.unpack(">h", data[offset : offset + 2])[0], offset + 2
        elif code == MessagePackSerializer.INT32:
            return struct.unpack(">i", data[offset : offset + 4])[0], offset + 4
        elif code == MessagePackSerializer.INT64:
            return struct.unpack(">q", data[offset : offset + 8])[0], offset + 8

        # floats
        elif code == MessagePackSerializer.FLOAT32:
            return struct.unpack(">f", data[offset : offset + 4])[0], offset + 4
        elif code == MessagePackSerializer.FLOAT64:
            return struct.unpack(">d", data[offset : offset + 8])[0], offset + 8

        # strings
        elif 0xA0 <= code <= 0xBF:
            # fixstr
            length = code & 0x1F
            return data[offset : offset + length].decode("utf-8"), offset + length
        elif code == MessagePackSerializer.STR8:
            length = data[offset]
            return (
                data[offset + 1 : offset + 1 + length].decode("utf-8"),
                offset + 1 + length,
            )
        elif code == MessagePackSerializer.STR16:
            length = struct.unpack(">H", data[offset : offset + 2])[0]
            return (
                data[offset + 2 : offset + 2 + length].decode("utf-8"),
                offset + 2 + length,
            )
        elif code == MessagePackSerializer.STR32:
            length = struct.unpack(">I", data[offset : offset + 4])[0]
            return (
                data[offset + 4 : offset + 4 + length].decode("utf-8"),
                offset + 4 + length,
            )

        # binary
        elif code == MessagePackSerializer.BIN8:
            length = data[offset]
            return data[offset + 1 : offset + 1 + length], offset + 1 + length
        elif code == MessagePackSerializer.BIN16:
            length = struct.unpack(">H", data[offset : offset + 2])[0]
            return data[offset + 2 : offset + 2 + length], offset + 2 + length
        elif code == MessagePackSerializer.BIN32:
            length = struct.unpack(">I", data[offset : offset + 4])[0]
            return data[offset + 4 : offset + 4 + length], offset + 4 + length

        # arrays
        elif 0x90 <= code <= 0x9F:
            # fixarray
            length = code & 0x0F
            return MessagePackSerializer._unpack_array(data, offset, length)
        elif code == MessagePackSerializer.ARRAY16:
            length = struct.unpack(">H", data[offset : offset + 2])[0]
            return MessagePackSerializer._unpack_array(data, offset + 2, length)
        elif code == MessagePackSerializer.ARRAY32:
            length = struct.unpack(">I", data[offset : offset + 4])[0]
            return MessagePackSerializer._unpack_array(data, offset + 4, length)

        # maps
        elif 0x80 <= code <= 0x8F:
            # fixmap
            length = code & 0x0F
            return MessagePackSerializer._unpack_map(data, offset, length)
        elif code == MessagePackSerializer.MAP16:
            length = struct.unpack(">H", data[offset : offset + 2])[0]
            return MessagePackSerializer._unpack_map(data, offset + 2, length)
        elif code == MessagePackSerializer.MAP32:
            length = struct.unpack(">I", data[offset : offset + 4])[0]
            return MessagePackSerializer._unpack_map(data, offset + 4, length)

        else:
            raise ValueError(f"Unknown MessagePack type code: 0x{code:02x}")

    @staticmethod
    def _unpack_array(data: bytes, offset: int, length: int) -> tuple:
        """Unpack array elements."""
        result = []
        for _ in range(length):
            item, offset = MessagePackSerializer._unpack_one(data, offset)
            result.append(item)
        return result, offset

    @staticmethod
    def _unpack_map(data: bytes, offset: int, length: int) -> tuple:
        """Unpack map elements."""
        result = {}
        for _ in range(length):
            key, offset = MessagePackSerializer._unpack_one(data, offset)
            value, offset = MessagePackSerializer._unpack_one(data, offset)
            result[key] = value
        return result, offset

    @staticmethod
    def container_to_msgpack(container: ValueContainer) -> bytes:
        """
        Serialize a ValueContainer to MessagePack format.

        Format: Map with keys:
        - header: {source_id, source_sub_id, target_id, target_sub_id, message_type, version}
        - values: [array of value dicts]
        """
        header = {
            "source_id": container.source_id,
            "source_sub_id": container.source_sub_id,
            "target_id": container.target_id,
            "target_sub_id": container.target_sub_id,
            "message_type": container.message_type,
            "version": container.version,
        }

        values_list = []
        for unit in container.units:
            value_dict = {
                "name": unit.name,
                "type": str(unit.type.value),
                "data": unit.data,
            }
            values_list.append(value_dict)

        container_dict = {"header": header, "values": values_list}

        return MessagePackSerializer.pack(container_dict)

    @staticmethod
    def msgpack_to_container(msgpack_data: bytes) -> ValueContainer:
        """
        Deserialize MessagePack data into a ValueContainer with full value reconstruction.

        Args:
            msgpack_data: MessagePack encoded data

        Returns:
            Fully reconstructed ValueContainer with all values

        Raises:
            ValueError: If data format is invalid
        """
        from container_module.values import (
            BoolValue,
            ShortValue,
            UShortValue,
            IntValue,
            UIntValue,
            LongValue,
            ULongValue,
            LLongValue,
            ULLongValue,
            FloatValue,
            DoubleValue,
            StringValue,
            BytesValue,
            ContainerValue,
        )

        data = MessagePackSerializer.unpack(msgpack_data)

        if not isinstance(data, dict) or "header" not in data or "values" not in data:
            raise ValueError("Invalid MessagePack container format")

        header = data["header"]
        values_data = data["values"]

        # Create container from header
        container = ValueContainer(
            source_id=header.get("source_id", ""),
            source_sub_id=header.get("source_sub_id", ""),
            target_id=header.get("target_id", ""),
            target_sub_id=header.get("target_sub_id", ""),
            message_type=header.get("message_type", ""),
        )

        # Reconstruct values
        for value_dict in values_data:
            if not isinstance(value_dict, dict):
                continue

            name = value_dict.get("name", "")
            type_value = int(value_dict.get("type", "0"))  # Convert string to int
            data_bytes = value_dict.get("data", b"")

            # Convert bytes if needed
            if not isinstance(data_bytes, bytes):
                data_bytes = bytes(data_bytes) if data_bytes else b""

            # Get ValueTypes enum
            value_type = ValueTypes(type_value)

            # Create value from type and data
            value = None
            try:
                if value_type == ValueTypes.BOOL_VALUE:
                    value = BoolValue.from_data(name, data_bytes)
                elif value_type == ValueTypes.SHORT_VALUE:
                    value = ShortValue.from_data(name, data_bytes)
                elif value_type == ValueTypes.USHORT_VALUE:
                    value = UShortValue.from_data(name, data_bytes)
                elif value_type == ValueTypes.INT_VALUE:
                    value = IntValue.from_data(name, data_bytes)
                elif value_type == ValueTypes.UINT_VALUE:
                    value = UIntValue.from_data(name, data_bytes)
                elif value_type == ValueTypes.LONG_VALUE:
                    value = LongValue.from_data(name, data_bytes)
                elif value_type == ValueTypes.ULONG_VALUE:
                    value = ULongValue.from_data(name, data_bytes)
                elif value_type == ValueTypes.LLONG_VALUE:
                    value = LLongValue.from_data(name, data_bytes)
                elif value_type == ValueTypes.ULLONG_VALUE:
                    value = ULLongValue.from_data(name, data_bytes)
                elif value_type == ValueTypes.FLOAT_VALUE:
                    value = FloatValue.from_data(name, data_bytes)
                elif value_type == ValueTypes.DOUBLE_VALUE:
                    value = DoubleValue.from_data(name, data_bytes)
                elif value_type == ValueTypes.STRING_VALUE:
                    value = StringValue.from_data(name, data_bytes)
                elif value_type == ValueTypes.BYTES_VALUE:
                    value = BytesValue.from_data(name, data_bytes)
                elif value_type == ValueTypes.CONTAINER_VALUE:
                    # Container values need special handling
                    value = ContainerValue.from_data(name, data_bytes)

                if value:
                    container.add(value)

            except Exception as e:
                print(f"Error reconstructing value {name}: {e}")
                continue

        return container
