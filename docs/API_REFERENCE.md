# python_container_system API Reference

> **Version**: 1.2.0
> **Last Updated**: 2025-12-17
> **Status**: Production Ready

## Table of Contents

1. [Namespace](#namespace)
2. [ValueContainer](#valuecontainer)
3. [MessagingBuilder](#messagingbuilder)
4. [Value Types](#value-types)
5. [Serialization](#serialization)
6. [Adapters](#adapters)

---

## Namespace

### `container_module`

All public APIs of python_container_system are contained in this package

**Included Items**:
- `ValueContainer` - Main container class
- `Value` - Abstract base class for all values
- `ValueTypes` - Value type enumerations
- Value implementations - All concrete value classes

---

## ValueContainer

### Overview

**Module**: `from container_module import ValueContainer`

**Description**: Main container class for managing messages with header information

### Constructor

```python
def __init__(
    self,
    source_id: str = "",
    source_sub_id: str = "",
    target_id: str = "",
    target_sub_id: str = "",
    message_type: str = "",
    units: Optional[List[Value]] = None,
    data_string: Optional[str] = None
) -> None:
    """
    Initialize a ValueContainer.

    Args:
        source_id: Source identifier
        source_sub_id: Source sub-identifier
        target_id: Target identifier
        target_sub_id: Target sub-identifier
        message_type: Message type identifier
        units: Initial list of values
        data_string: Serialized data to deserialize from

    Example:
        container = ValueContainer(
            source_id="client_01",
            target_id="server",
            message_type="user_data"
        )
    """
```

### Properties

#### Header Properties (Read-Only)

```python
@property
def source_id(self) -> str:
    """Get source ID."""

@property
def source_sub_id(self) -> str:
    """Get source sub-ID."""

@property
def target_id(self) -> str:
    """Get target ID."""

@property
def target_sub_id(self) -> str:
    """Get target sub-ID."""

@property
def message_type(self) -> str:
    """Get message type."""

@property
def version(self) -> str:
    """Get container version."""

@property
def units(self) -> List[Value]:
    """Get list of all values."""
```

**Example**:
```python
container = ValueContainer(source_id="client", target_id="server")
print(container.source_id)  # "client"
print(container.target_id)  # "server"
```

### Header Management

#### `set_source()`

```python
def set_source(self, source_id: str, source_sub_id: str = "") -> None:
    """
    Set source information.

    Args:
        source_id: Source identifier
        source_sub_id: Source sub-identifier (optional)

    Example:
        container.set_source("client_01", "session_123")
    """
```

#### `set_target()`

```python
def set_target(self, target_id: str, target_sub_id: str = "") -> None:
    """
    Set target information.

    Args:
        target_id: Target identifier
        target_sub_id: Target sub-identifier (optional)

    Example:
        container.set_target("server", "handler_main")
    """
```

#### `set_message_type()`

```python
def set_message_type(self, message_type: str) -> None:
    """
    Set message type.

    Args:
        message_type: Message type identifier

    Example:
        container.set_message_type("user_data")
    """
```

#### `swap_header()`

```python
def swap_header(self) -> None:
    """
    Swap source and target for request-response pattern.

    Example:
        # Request: client -> server
        request = ValueContainer(source_id="client", target_id="server")

        # Response: server -> client (automatically swapped)
        response = request.copy()
        response.swap_header()
        # Now: source_id="server", target_id="client"
    """
```

### Value Management

#### `add()`

```python
def add(self, target_value: Value, update_immediately: bool = False) -> Value:
    """
    Add a value to this container.

    Args:
        target_value: Value to add
        update_immediately: Legacy parameter (ignored)

    Returns:
        The added value

    Example:
        from container_module.values import StringValue
        container.add(StringValue("name", "Alice"))
    """
```

#### `get_value()`

```python
def get_value(self, target_name: str, index: int = 0) -> Optional[Value]:
    """
    Get value by name with optional index.

    Args:
        target_name: Name of the value to retrieve
        index: Index if multiple values with same name (default: 0)

    Returns:
        Value if found, None otherwise

    Example:
        value = container.get_value("user_id")
        if value:
            user_id = value.to_int()
    """
```

#### `value_array()`

```python
def value_array(self, target_name: str) -> List[Value]:
    """
    Get all values with the given name.

    Args:
        target_name: Name of values to retrieve

    Returns:
        List of matching values (may be empty)

    Example:
        # Get all values named "score"
        scores = container.value_array("score")
        for score in scores:
            print(score.to_int())
    """
```

#### `remove()`

```python
def remove(self, target: Union[str, Value], update_immediately: bool = False) -> None:
    """
    Remove value(s) by name or object.

    Args:
        target: Value name (str) or Value object
        update_immediately: Legacy parameter (ignored)

    Example:
        # Remove by name
        container.remove("old_field")

        # Remove by object
        value = container.get_value("temp")
        container.remove(value)
    """
```

#### `clear_value()`

```python
def clear_value(self) -> None:
    """
    Remove all values from container.

    Example:
        container.clear_value()
        assert len(container.units) == 0
    """
```

### Serialization

#### `serialize()`

```python
def serialize(self) -> str:
    """
    Serialize to binary format string (C++ compatible).

    Returns:
        Serialized string in binary format

    Example:
        data = container.serialize()
        # Save or send data
    """
```

#### `serialize_array()`

```python
def serialize_array(self) -> bytes:
    """
    Serialize to bytes array.

    Returns:
        Serialized data as bytes

    Example:
        data = container.serialize_array()
        with open("data.bin", "wb") as f:
            f.write(data)
    """
```

#### `deserialize()`

```python
def deserialize(self, data_string: str, parse_only_header: bool = True) -> bool:
    """
    Deserialize from string.

    Args:
        data_string: Serialized data string
        parse_only_header: If True, parse only header; if False, parse all data

    Returns:
        True if successful, False otherwise

    Example:
        success = container.deserialize(data_string, parse_only_header=False)
        if not success:
            print("Deserialization failed")
    """
```

#### `to_json()`

```python
def to_json(self) -> str:
    """
    Convert to JSON format.

    Returns:
        JSON string representation

    Example:
        json_str = container.to_json()
        print(json_str)  # Pretty-printed JSON
    """
```

#### `to_xml()`

```python
def to_xml(self) -> str:
    """
    Convert to XML format.

    Returns:
        XML string representation

    Example:
        xml_str = container.to_xml()
    """
```

### File I/O

#### `save_to_file()` / `save_packet()`

```python
def save_to_file(self, file_path: str) -> None:
    """
    Save container to file in binary format.

    Args:
        file_path: Path to save file

    Raises:
        IOError: If file cannot be written

    Example:
        container.save_to_file("data/message.bin")
    """
```

#### `load_from_file()` / `load_packet()`

```python
def load_from_file(self, file_path: str) -> None:
    """
    Load container from file.

    Args:
        file_path: Path to load file

    Raises:
        IOError: If file cannot be read

    Example:
        container.load_from_file("data/message.bin")
    """
```

### Utility Methods

#### `copy()`

```python
def copy(self, containing_values: bool = True) -> ValueContainer:
    """
    Create a copy of this container.

    Args:
        containing_values: If True, copy values; if False, copy only header

    Returns:
        New ValueContainer instance

    Example:
        # Deep copy
        copy_with_values = container.copy(containing_values=True)

        # Shallow copy (header only)
        copy_header_only = container.copy(containing_values=False)
    """
```

#### `enable_thread_safety()`

```python
def enable_thread_safety(self, enabled: bool = True) -> None:
    """
    Enable or disable thread-safe operations.

    Args:
        enabled: True to enable thread safety, False to disable

    Example:
        container.enable_thread_safety(True)
        # Now safe for concurrent access
    """
```

---

## MessagingBuilder

### Overview

**Module**: `from container_module import MessagingBuilder`

**Description**: Builder class for creating ValueContainer instances with fluent API

### Constructor

```python
def __init__(self) -> None:
    """
    Initialize a new MessagingBuilder with default values.

    Example:
        builder = MessagingBuilder()
    """
```

### Methods

#### `set_source()`

```python
def set_source(self, source_id: str, source_sub_id: str = "") -> MessagingBuilder:
    """
    Set the source identifier for the message.

    Args:
        source_id: Source identifier
        source_sub_id: Source sub-identifier (optional)

    Returns:
        Self for method chaining

    Example:
        builder.set_source("client1", "session1")
    """
```

#### `set_target()`

```python
def set_target(self, target_id: str, target_sub_id: str = "") -> MessagingBuilder:
    """
    Set the target identifier for the message.

    Args:
        target_id: Target identifier
        target_sub_id: Target sub-identifier (optional)

    Returns:
        Self for method chaining

    Example:
        builder.set_target("server1", "handler1")
    """
```

#### `set_type()`

```python
def set_type(self, message_type: str) -> MessagingBuilder:
    """
    Set the message type.

    Args:
        message_type: Type of message

    Returns:
        Self for method chaining

    Example:
        builder.set_type("request")
    """
```

#### `add_value()`

```python
def add_value(self, value: Value) -> MessagingBuilder:
    """
    Add a value to the message.

    Args:
        value: Value to add

    Returns:
        Self for method chaining

    Example:
        builder.add_value(StringValue("name", "John"))
    """
```

#### `add_values()`

```python
def add_values(self, values: List[Value]) -> MessagingBuilder:
    """
    Add multiple values to the message.

    Args:
        values: List of values to add

    Returns:
        Self for method chaining

    Example:
        builder.add_values([StringValue("name", "John"), IntValue("age", 30)])
    """
```

#### `build()`

```python
def build(self) -> ValueContainer:
    """
    Build and return the configured ValueContainer.

    Returns:
        A new ValueContainer with the configured settings

    Example:
        container = builder.build()
    """
```

#### `reset()`

```python
def reset(self) -> MessagingBuilder:
    """
    Reset the builder to default state for reuse.

    Returns:
        Self for method chaining

    Example:
        builder.reset()
    """
```

### Complete Usage Example

```python
from container_module import MessagingBuilder
from container_module.values import StringValue, IntValue, BoolValue

# Create container using builder pattern
container = (
    MessagingBuilder()
    .set_source("client1", "session1")
    .set_target("server1", "handler1")
    .set_type("user_request")
    .add_value(StringValue("username", "john_doe"))
    .add_value(IntValue("user_id", 12345))
    .add_value(BoolValue("is_active", True))
    .build()
)

# Builder can be reused after reset
builder = MessagingBuilder()
request = builder.set_source("client").set_type("request").build()
response = builder.reset().set_source("server").set_type("response").build()
```

---

## Value Types

### Abstract Base Class

#### `Value`

**Module**: `from container_module.core import Value`

```python
class Value(ABC):
    """
    Abstract base class for all value types.

    Properties:
        name (str): Value name/key
        type (ValueTypes): Value type enumeration
        size (int): Size of data in bytes
    """

    @abstractmethod
    def serialize(self) -> str:
        """Serialize this value to string."""

    @abstractmethod
    def to_string(self, original: bool = True) -> str:
        """Convert to string representation."""
```

### Primitive Types

#### `BoolValue`

```python
class BoolValue(Value):
    """
    Boolean value (True/False).

    Example:
        value = BoolValue("is_active", True)
        assert value.to_bool() == True
        assert value.to_int() == 1
    """

    def __init__(self, name: str, value: bool) -> None: ...

    def to_bool(self) -> bool: ...
    def to_int(self) -> int: ...  # 1 for True, 0 for False
```

### Numeric Types

#### `ShortValue` (16-bit signed)

```python
class ShortValue(NumericValue):
    """16-bit signed integer (-32,768 to 32,767)."""

    def __init__(self, name: str, value: int) -> None: ...

    @classmethod
    def from_string(cls, name: str, value_str: str) -> "ShortValue": ...
```

#### `IntValue` (32-bit signed)

```python
class IntValue(NumericValue):
    """32-bit signed integer (-2³¹ to 2³¹-1)."""

    def __init__(self, name: str, value: int) -> None: ...

    def to_int(self) -> int: ...
    def to_int32(self) -> int: ...  # Alias
```

#### `LongValue` (32-bit signed, C++ compatible)

```python
class LongValue(NumericValue):
    """
    32-bit signed integer (C++ long compatibility).

    Note: Always 32-bit for cross-platform compatibility.

    Raises:
        OverflowError: If value exceeds 32-bit range
    """

    def __init__(self, name: str, value: int) -> None: ...
```

#### `LLongValue` (64-bit signed)

```python
class LLongValue(NumericValue):
    """64-bit signed integer (-2⁶³ to 2⁶³-1)."""

    def __init__(self, name: str, value: int) -> None: ...

    def to_int64(self) -> int: ...
```

#### `FloatValue` (32-bit float)

```python
class FloatValue(NumericValue):
    """32-bit floating-point number."""

    def __init__(self, name: str, value: float) -> None: ...

    def to_float(self) -> float: ...
```

#### `DoubleValue` (64-bit float)

```python
class DoubleValue(NumericValue):
    """64-bit floating-point number."""

    def __init__(self, name: str, value: float) -> None: ...

    def to_double(self) -> float: ...
```

### String and Binary Types

#### `StringValue`

```python
class StringValue(Value):
    """
    UTF-8 encoded string value.

    Example:
        value = StringValue("name", "Alice")
        assert value.to_string() == "Alice"
    """

    def __init__(self, name: str, value: str) -> None: ...

    def to_string(self, original: bool = True) -> str: ...
```

#### `BytesValue`

```python
class BytesValue(Value):
    """
    Raw byte array value.

    Methods:
        to_bytes() -> bytes: Get raw bytes
        to_hex() -> str: Convert to hex string
        to_base64() -> str: Convert to base64 string

    Example:
        data = BytesValue("image", b"\\x89PNG\\r\\n")
        hex_str = data.to_hex()
        b64_str = data.to_base64()
    """

    def __init__(self, name: str, data: bytes) -> None: ...

    def to_bytes(self) -> bytes: ...
    def to_hex(self) -> str: ...
    def to_base64(self) -> str: ...

    @classmethod
    def from_hex(cls, name: str, hex_str: str) -> "BytesValue": ...

    @classmethod
    def from_base64(cls, name: str, b64_str: str) -> "BytesValue": ...
```

### Container Types

#### `ContainerValue`

```python
class ContainerValue(Value):
    """
    Nested container value for hierarchical data.

    Example:
        address = ContainerValue("address")
        address.add(StringValue("street", "123 Main St"))
        address.add(StringValue("city", "Seattle"))
    """

    def __init__(self, name: str, children: Optional[List[Value]] = None) -> None: ...

    def add(self, item: Value, update_count: bool = True) -> Value: ...
    def child_count(self) -> int: ...
    def children(self, only_container: bool = False) -> List[Value]: ...
    def get_child(self, index: int) -> Optional[Value]: ...
```

#### `ArrayValue`

```python
class ArrayValue(ContainerValue):
    """
    Homogeneous array of values.

    Example:
        scores = ArrayValue("test_scores")
        scores.add(IntValue("", 95))
        scores.add(IntValue("", 87))
        scores.add(IntValue("", 92))
    """

    def __init__(self, name: str) -> None: ...

    def add(self, item: Value) -> Value: ...
    def get_element_type(self) -> Optional[ValueTypes]: ...
```

---

## Serialization

### Binary Format

```python
# Serialize
data = container.serialize()  # str format
binary_data = container.serialize_array()  # bytes format

# Deserialize
container = ValueContainer(data_string=data)
# or
container = ValueContainer()
container.deserialize(data, parse_only_header=False)
```

### JSON Format

```python
# Serialize
json_str = container.to_json()

# Deserialize (requires manual parsing)
import json
data = json.loads(json_str)
# Manual reconstruction needed
```

### JSON v2.0 Format

```python
from container_module.adapters import JSONv2Adapter

# Serialize
json_str = JSONv2Adapter.to_json(container)
json_dict = JSONv2Adapter.to_dict(container)

# Deserialize
container = JSONv2Adapter.from_json(json_str)
container = JSONv2Adapter.from_dict(json_dict)
```

### XML Format

```python
# Serialize
xml_str = container.to_xml()

# Deserialize (requires manual parsing)
import xml.etree.ElementTree as ET
root = ET.fromstring(xml_str)
# Manual reconstruction needed
```

### MessagePack Format

```python
from container_module.serializers import MessagePackSerializer

# Serialize
msgpack_data = MessagePackSerializer.container_to_msgpack(container)

# Deserialize (header only currently)
header = MessagePackSerializer.msgpack_to_container(msgpack_data)
```

---

## Adapters

### JSONv2Adapter

**Module**: `from container_module.adapters import JSONv2Adapter`

Cross-language JSON adapter for interoperability with C++, .NET, Go implementations.

#### Methods

```python
class JSONv2Adapter:
    """JSON v2.0 adapter for cross-language compatibility."""

    @staticmethod
    def to_json(container: ValueContainer, indent: int = 2) -> str:
        """
        Convert container to JSON v2.0 string.

        Args:
            container: Container to convert
            indent: JSON indentation level

        Returns:
            JSON string
        """

    @staticmethod
    def to_dict(container: ValueContainer) -> dict:
        """
        Convert container to dictionary.

        Args:
            container: Container to convert

        Returns:
            Dictionary representation
        """

    @staticmethod
    def from_json(json_str: str) -> ValueContainer:
        """
        Create container from JSON v2.0 string.

        Args:
            json_str: JSON string

        Returns:
            ValueContainer instance
        """

    @staticmethod
    def from_dict(data: dict) -> ValueContainer:
        """
        Create container from dictionary.

        Args:
            data: Dictionary representation

        Returns:
            ValueContainer instance
        """
```

### MessagePackSerializer

**Module**: `from container_module.serializers import MessagePackSerializer`

Pure Python MessagePack serialization (zero dependencies).

#### Methods

```python
class MessagePackSerializer:
    """MessagePack serialization for compact binary format."""

    @staticmethod
    def container_to_msgpack(container: ValueContainer) -> bytes:
        """
        Serialize container to MessagePack format.

        Args:
            container: Container to serialize

        Returns:
            MessagePack bytes
        """

    @staticmethod
    def msgpack_to_container(data: bytes) -> ValueContainer:
        """
        Deserialize container from MessagePack (header only).

        Args:
            data: MessagePack bytes

        Returns:
            ValueContainer with header information
        """
```

---

## Type Conversion Reference

### Numeric Conversions

```python
# All numeric types support these conversions
value = IntValue("count", 42)

value.to_int()      # -> int
value.to_int32()    # -> int (32-bit)
value.to_int64()    # -> int (64-bit)
value.to_float()    # -> float
value.to_double()   # -> float (64-bit)
value.to_string()   # -> str
```

### Type Checking

```python
from container_module.core import ValueTypes

value = container.get_value("field")
if value:
    if value.type == ValueTypes.INT_VALUE:
        # Handle integer
        num = value.to_int()
    elif value.type == ValueTypes.STRING_VALUE:
        # Handle string
        text = value.to_string()
    elif value.type == ValueTypes.CONTAINER_VALUE:
        # Handle nested container
        children = value.children()
```

---

## Performance Notes

### Throughput Benchmarks

| Operation | Throughput | Notes |
|-----------|-----------|-------|
| Value creation | 4-6M ops/sec | Depends on type |
| Container add | 3M ops/sec | Fast append |
| get_value | 1.7M ops/sec | List scan |
| Binary serialize | 6.7M ops/sec | Very fast |
| Binary deserialize | 700K ops/sec | Parser overhead |
| JSON serialize | 50K ops/sec | Use for APIs |

### Memory Usage

| Component | Overhead | Notes |
|-----------|---------|-------|
| Empty container | ~600 bytes | Python object overhead |
| Per value | ~420-450 bytes | Includes name, type, data |
| String value | +length | UTF-8 encoding |

---

## See Also

- [FEATURES.md](FEATURES.md) - Complete feature documentation
- [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) - File organization
- [ARCHITECTURE.md](ARCHITECTURE.md) - Design patterns and architecture
- [guides/FAQ.md](guides/FAQ.md) - Frequently asked questions

---

**Created**: 2025-11-26
**Version**: 1.1.0
**Python Version**: 3.8+
