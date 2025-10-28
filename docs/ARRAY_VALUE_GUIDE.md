# ArrayValue Implementation Guide (Python)

## Overview

`ArrayValue` provides Python's implementation of type-15 heterogeneous array collections with Pythonic API design and full cross-language compatibility. It leverages Python's dynamic typing, list operations, and duck typing.

## Architecture

### Class Hierarchy

```
Value (base class)
├── BoolValue
├── NumericValue
│   ├── IntValue
│   ├── LongValue
│   └── DoubleValue
├── BytesValue
├── StringValue
├── ContainerValue
└── ArrayValue ← List-based heterogeneous collection
```

### Module Structure

```
python_container_system/
├── container_module/
│   ├── __init__.py           # Exports ValueContainer
│   ├── core/
│   │   ├── value.py          # Value base class
│   │   ├── value_types.py    # ValueTypes enum with ARRAY_VALUE
│   │   └── container.py      # ValueContainer
│   └── values/
│       ├── __init__.py       # Exports all value types
│       ├── array_value.py    # ArrayValue implementation
│       ├── int_value.py
│       ├── string_value.py
│       └── ...
└── tests/
    ├── test_array_value.py
    └── test_cross_language_array.py
```

### Class Diagram

```
┌────────────────────────────────────┐
│        Value (base)                │
├────────────────────────────────────┤
│ _name: str                         │
│ _type: ValueTypes                  │
│ _data: bytes                       │
│ _parent: Optional[Value]           │
├────────────────────────────────────┤
│ name() -> str                      │
│ type() -> ValueTypes               │
│ to_bytes() -> bytes                │
│ to_json() -> str                   │
│ to_xml() -> str                    │
│ set_parent(parent)                 │
└────────────────────────────────────┘
                ▲
                │ inherits
                │
┌────────────────────────────────────┐
│        ArrayValue                  │
├────────────────────────────────────┤
│ _values: List[Value]               │
├────────────────────────────────────┤
│ __init__(name, values=None)       │
│ from_data(name, data) -> ArrayValue│
│ count() -> int                     │
│ is_empty() -> bool                 │
│ values() -> List[Value]           │
│ push_back(value: Value)           │
│ at(index: int) -> Value           │
│ clear()                            │
│ to_bytes() -> bytes                │
│ to_json() -> str                   │
│ to_xml() -> str                    │
└────────────────────────────────────┘
```

## Usage Examples

### Basic Creation

```python
from container_module.values import ArrayValue, IntValue, StringValue

# Create empty array
numbers = ArrayValue("numbers")

# Add elements
numbers.push_back(IntValue("", 10))
numbers.push_back(IntValue("", 20))
numbers.push_back(IntValue("", 30))

print(f"Array has {numbers.count()} elements")
# Output: Array has 3 elements
```

### Constructor with Initial Values

```python
# Create array with list of values
colors = ArrayValue("colors", [
    StringValue("", "red"),
    StringValue("", "green"),
    StringValue("", "blue"),
])

print(f"Created array with {colors.count()} colors")
```

### Heterogeneous Collections

```python
from container_module.values import (
    ArrayValue, IntValue, StringValue,
    DoubleValue, BoolValue
)

# Mix different value types
mixed = ArrayValue("mixed")

mixed.push_back(IntValue("", 42))
mixed.push_back(StringValue("", "hello"))
mixed.push_back(DoubleValue("", 3.14))
mixed.push_back(BoolValue("", True))

# Access elements
first = mixed.at(0)
print(f"First element type: {first.type()}")
```

### Integration with ValueContainer

```python
from container_module import ValueContainer
from container_module.values import ArrayValue, IntValue, StringValue

# Create container
container = ValueContainer()
container.set_message_type("user_data")

# Create array
scores = ArrayValue("test_scores")
scores.push_back(IntValue("", 95))
scores.push_back(IntValue("", 87))
scores.push_back(IntValue("", 92))

# Add to container
container.add(scores)

# Serialize to wire protocol
wire_data = container.serialize()
print("Wire format:", wire_data)
# Output: @header={{...}};@data={{[test_scores,15,3];...}};
```

## Iteration and Access

### List-like Access

```python
array = ArrayValue("data", [
    IntValue("", 10),
    IntValue("", 20),
    IntValue("", 30),
])

# Direct indexing
first = array.at(0)
print(f"First element: {first.to_string()}")

# Check bounds
if array.count() > 5:
    fifth = array.at(5)
else:
    print("Array has fewer than 6 elements")
```

### Iterating Elements

```python
array = ArrayValue("items")
# ... populate array ...

# Iterate through values (Pythonic way)
for i, element in enumerate(array.values()):
    print(f"Element {i}: {element.name()}")

# Get count
count = array.count()
print(f"Total elements: {count}")

# Check if empty
if array.is_empty():
    print("Array is empty")
```

### List Comprehensions

```python
# Filter elements by type
integers = [
    val for val in array.values()
    if val.type() == ValueTypes.INT_VALUE
]

# Transform elements
doubled = ArrayValue("doubled")
for val in array.values():
    if isinstance(val, IntValue):
        doubled.push_back(IntValue("", val.to_int() * 2))
```

## Serialization

### Binary Format

```python
array = ArrayValue("data", [
    IntValue("", 42),
    StringValue("", "test"),
])

# Serialize to bytes
binary_data = array.to_bytes()
print(f"Serialized {len(binary_data)} bytes")
```

### JSON Format

```python
colors = ArrayValue("colors", [
    StringValue("", "red"),
    StringValue("", "blue"),
])

json_str = array.to_json()
print("JSON:", json_str)
# Output: {"name": "colors", "type": "array", "elements": [...]}
```

### XML Format

```python
scores = ArrayValue("scores", [
    IntValue("", 95),
    IntValue("", 87),
])

xml_str = array.to_xml()
print("XML:", xml_str)
# Output: <array name="scores" count="2">...</array>
```

### Wire Protocol Format

```python
from container_module import ValueContainer

container = ValueContainer()
array = ArrayValue("items", [
    IntValue("", 1),
    IntValue("", 2),
])
container.add(array)

# Serialize to cross-language format
wire_format = container.serialize()
print(wire_format)
# Output: @header={{...}};@data={{[items,15,2];...}};
```

## Type Checking and Casting

### Duck Typing Pattern

```python
element = array.at(0)

# Check type
if isinstance(element, IntValue):
    print(f"Integer value: {element.to_int()}")
elif isinstance(element, StringValue):
    print(f"String value: {element.to_string()}")
```

### ValueTypes Enum Check

```python
from container_module.core.value_types import ValueTypes

element = array.at(0)

if element.type() == ValueTypes.INT_VALUE:
    int_val = element.to_int()
    print(f"Integer: {int_val}")
elif element.type() == ValueTypes.STRING_VALUE:
    str_val = element.to_string()
    print(f"String: {str_val}")
elif element.type() == ValueTypes.ARRAY_VALUE:
    print("Nested array detected")
```

### Safe Type Conversion

```python
def safe_get_int(value):
    """Safely convert Value to int."""
    try:
        return value.to_int()
    except (AttributeError, ValueError):
        return None

element = array.at(0)
int_value = safe_get_int(element)
if int_value is not None:
    print(f"Integer: {int_value}")
```

## Error Handling

```python
def process_array(array: ArrayValue) -> None:
    """Process array with error handling."""
    if array.is_empty():
        raise ValueError("Array cannot be empty")

    for i, element in enumerate(array.values()):
        try:
            json_str = element.to_json()
            print(f"Element {i} JSON: {json_str}")
        except Exception as e:
            print(f"Error processing element {i}: {e}")
```

## Cross-Language Interoperability

### Receiving from C++/Rust

```python
from container_module import ValueContainer

# Receive wire format from C++/Rust
cpp_wire_data = "@header={{[5,test];}};@data={{[nums,array_value,3];}};".strip()

# Note: Full deserialization with nested elements not yet implemented
# This tests that the format is recognized

# In future with full support:
# container = ValueContainer.from_string(cpp_wire_data)
# array = container.get_value("nums")
```

### Sending to Go/.NET

```python
from container_module import ValueContainer
from container_module.values import ArrayValue, IntValue, StringValue

container = ValueContainer()
array = ArrayValue("data", [
    IntValue("", 100),
    StringValue("", "test"),
])
container.add(array)

# Serialize for cross-language transmission
wire_data = container.serialize()

# Send wire_data over network/IPC
# Go: container, _ := wireprotocol.DeserializeCppWire(wireData)
# C#: var container = ValueContainer.FromString(wireData);
```

## Pythonic Features

### Context Manager Support (Future)

```python
# Potential future implementation
class ArrayValueContext(ArrayValue):
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.clear()
        return False

# Usage
with ArrayValueContext("temp") as temp_array:
    temp_array.push_back(IntValue("", 42))
    # ... use temp_array
# Automatically cleared on exit
```

### Len and Indexing (Current)

```python
# Get length
length = array.count()

# Access by index
for i in range(array.count()):
    element = array.at(i)
    print(element)
```

### String Representation

```python
array = ArrayValue("colors", [
    StringValue("", "red"),
    StringValue("", "blue"),
])

# String conversion
print(str(array))
# Output: Array(2 elements)
```

## Best Practices

### 1. Use List Initialization

```python
# Good: Clean initialization
array = ArrayValue("colors", [
    StringValue("", "red"),
    StringValue("", "green"),
    StringValue("", "blue"),
])

# Avoid: Verbose step-by-step
array = ArrayValue("colors")
array.push_back(StringValue("", "red"))
array.push_back(StringValue("", "green"))
array.push_back(StringValue("", "blue"))
```

### 2. Type Hints

```python
from typing import List
from container_module.values import ArrayValue, Value

def create_int_array(name: str, values: List[int]) -> ArrayValue:
    """Create ArrayValue from list of integers."""
    array = ArrayValue(name)
    for val in values:
        array.push_back(IntValue("", val))
    return array
```

### 3. Defensive Programming

```python
# Good: Check before accessing
if not array.is_empty():
    first = array.at(0)
    # Use first
else:
    print("Array is empty")

# Avoid: Assuming array has elements
first = array.at(0)  # May raise error if empty
```

### 4. Descriptive Names

```python
# Good
user_ids = ArrayValue("user_ids")
test_scores = ArrayValue("test_scores")

# Avoid
arr = ArrayValue("a")
data = ArrayValue("d")
```

## Testing

```python
import unittest
from container_module.values import ArrayValue, IntValue, StringValue

class TestArrayValue(unittest.TestCase):
    def test_creation(self):
        array = ArrayValue("test")
        self.assertEqual(array.count(), 0)
        self.assertTrue(array.is_empty())

    def test_heterogeneous_array(self):
        array = ArrayValue("mixed", [
            IntValue("", 42),
            StringValue("", "hello"),
        ])

        self.assertEqual(array.count(), 2)

        first = array.at(0)
        self.assertIsInstance(first, IntValue)

        second = array.at(1)
        self.assertIsInstance(second, StringValue)

    def test_push_back(self):
        array = ArrayValue("test")
        array.push_back(IntValue("", 1))
        array.push_back(IntValue("", 2))

        self.assertEqual(array.count(), 2)

    def test_clear(self):
        array = ArrayValue("test", [IntValue("", 1)])
        self.assertFalse(array.is_empty())

        array.clear()
        self.assertTrue(array.is_empty())

if __name__ == "__main__":
    unittest.main()
```

## Performance Considerations

- **List overhead**: Python lists are dynamic arrays with amortized O(1) append
- **Object references**: Elements stored as object references (lightweight)
- **Type checking**: `isinstance()` is fast for built-in types
- **Iteration**: List iteration is optimized in CPython

## Common Patterns

### Building from Existing List

```python
numbers = [1, 2, 3, 4, 5]

array = ArrayValue("numbers", [
    IntValue("", num) for num in numbers
])
```

### Filtering Elements

```python
def filter_integers(array: ArrayValue) -> ArrayValue:
    """Filter array to include only integers."""
    filtered = ArrayValue("filtered")

    for val in array.values():
        if val.type() == ValueTypes.INT_VALUE:
            filtered.push_back(val)

    return filtered
```

### Mapping Elements

```python
def double_integers(array: ArrayValue) -> ArrayValue:
    """Create new array with doubled integer values."""
    result = ArrayValue("doubled")

    for val in array.values():
        if isinstance(val, IntValue):
            doubled = val.to_int() * 2
            result.push_back(IntValue("", doubled))

    return result
```

### Reduce/Aggregate

```python
def sum_integers(array: ArrayValue) -> int:
    """Sum all integer values in array."""
    total = 0
    for val in array.values():
        if isinstance(val, IntValue):
            total += val.to_int()
    return total
```

## Integration with Python Ecosystem

### JSON with Standard Library

```python
import json

def array_to_dict(array: ArrayValue) -> dict:
    """Convert ArrayValue to Python dict."""
    return {
        "name": array.name(),
        "count": array.count(),
        "elements": [
            val.to_string() for val in array.values()
        ]
    }

# Convert to JSON
array_dict = array_to_dict(my_array)
json_str = json.dumps(array_dict, indent=2)
```

### Dataclasses Integration

```python
from dataclasses import dataclass
from typing import List

@dataclass
class ArrayData:
    name: str
    elements: List[str]

def array_to_dataclass(array: ArrayValue) -> ArrayData:
    """Convert ArrayValue to dataclass."""
    return ArrayData(
        name=array.name(),
        elements=[val.to_string() for val in array.values()]
    )
```

### Generator Pattern

```python
def array_generator(array: ArrayValue):
    """Generate elements lazily."""
    for val in array.values():
        yield val

# Usage
for element in array_generator(my_array):
    print(element.to_string())
```

## Migration from Raw Lists

### Before

```python
values = []
values.append(IntValue("", 10))
values.append(IntValue("", 20))
```

### After

```python
array = ArrayValue("values")
array.push_back(IntValue("", 10))
array.push_back(IntValue("", 20))
```

**Benefits:**
- Type-safe with `ValueTypes.ARRAY_VALUE`
- Serialization methods (to_bytes, to_json, to_xml)
- Cross-language wire protocol support
- Parent-child relationship tracking
- Consistent API with other languages

## Advanced Usage

### Custom ArrayValue Subclass

```python
class TypedArrayValue(ArrayValue):
    """ArrayValue that enforces element type."""

    def __init__(self, name: str, allowed_type: ValueTypes):
        super().__init__(name)
        self.allowed_type = allowed_type

    def push_back(self, value: Value) -> None:
        """Push value with type checking."""
        if value.type() != self.allowed_type:
            raise TypeError(
                f"Expected {self.allowed_type}, got {value.type()}"
            )
        super().push_back(value)

# Usage
int_array = TypedArrayValue("integers", ValueTypes.INT_VALUE)
int_array.push_back(IntValue("", 42))  # OK
# int_array.push_back(StringValue("", "fail"))  # Raises TypeError
```

### Serialization Hooks

```python
class CustomArrayValue(ArrayValue):
    """ArrayValue with custom serialization."""

    def to_json(self) -> str:
        """Custom JSON format."""
        data = {
            "type": "custom_array",
            "name": self.name(),
            "size": self.count(),
            "data": [val.to_json() for val in self.values()]
        }
        return json.dumps(data)
```

## See Also

- [Python Value Base Class](../container_module/core/value.py)
- [ValueTypes Enum](../container_module/core/value_types.py)
- [ValueContainer Documentation](../container_module/core/container.py)
- [Cross-Language Tests](../tests/test_cross_language_array.py)
- [Architecture Overview](ARCHITECTURE.md)
