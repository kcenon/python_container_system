# Contributing to Python Container System

Thank you for your interest in contributing to the Python Container System! This document provides guidelines and instructions for contributing.

---

## Table of Contents

1. [Code of Conduct](#code-of-conduct)
2. [Getting Started](#getting-started)
3. [Development Setup](#development-setup)
4. [How to Contribute](#how-to-contribute)
5. [Coding Standards](#coding-standards)
6. [Testing Requirements](#testing-requirements)
7. [Pull Request Process](#pull-request-process)
8. [Release Process](#release-process)

---

## Code of Conduct

This project adheres to a code of conduct that all contributors are expected to follow:

- **Be respectful**: Treat everyone with respect and consideration
- **Be constructive**: Provide helpful feedback and suggestions
- **Be inclusive**: Welcome newcomers and help them get started
- **Be patient**: Remember that everyone has different skill levels

---

## Getting Started

### Prerequisites

- Python 3.8 or later
- Git
- pip (Python package manager)
- A GitHub account

### Fork and Clone

1. Fork the repository on GitHub
2. Clone your fork locally:

```bash
git clone https://github.com/YOUR_USERNAME/python_container_system.git
cd python_container_system
```

3. Add the upstream remote:

```bash
git remote add upstream https://github.com/kcenon/python_container_system.git
```

---

## Development Setup

### Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate (Linux/macOS)
source venv/bin/activate

# Activate (Windows)
.\venv\Scripts\activate
```

### Install Dependencies

```bash
# Install in development mode with all dependencies
pip install -e ".[dev]"

# Or install manually
pip install -e .
pip install pytest pytest-cov black mypy pylint
```

### Verify Installation

```bash
# Run tests
pytest

# Run type checking
mypy container_module

# Run linter
pylint container_module
```

---

## How to Contribute

### Reporting Bugs

Before reporting a bug:
1. Search [existing issues](https://github.com/kcenon/python_container_system/issues)
2. Check the [troubleshooting guide](docs/guides/TROUBLESHOOTING.md)

When reporting:
- Use the bug report template
- Include Python version (`python --version`)
- Provide a minimal reproducible example
- Include error messages and stack traces

### Suggesting Features

1. Check [existing discussions](https://github.com/kcenon/python_container_system/discussions)
2. Open a new discussion in the "Ideas" category
3. Describe the feature and its use case
4. Wait for community feedback before implementing

### Contributing Code

1. **Find an issue**: Look for issues labeled `good first issue` or `help wanted`
2. **Discuss**: Comment on the issue to express interest
3. **Implement**: Follow the coding standards
4. **Test**: Add tests for your changes
5. **Submit**: Create a pull request

---

## Coding Standards

### Python Style

Follow [PEP 8](https://pep8.org/) and use [Black](https://black.readthedocs.io/) for formatting:

```bash
# Format code
black container_module tests examples
```

### Type Hints

Use type hints for all public functions and methods:

```python
from typing import Optional, List

def get_value(self, name: str, index: int = 0) -> Optional[Value]:
    """Get a value by name and index.

    Args:
        name: The name of the value to retrieve.
        index: The index if multiple values have the same name.

    Returns:
        The value if found, None otherwise.
    """
    pass
```

### Docstrings

Use Google-style docstrings:

```python
class ValueContainer:
    """Container for typed values with metadata.

    This class provides a type-safe container for storing and managing
    values with support for serialization and cross-language compatibility.

    Attributes:
        source_id: The source identifier for the message.
        target_id: The target identifier for the message.
        message_type: The type of message.

    Example:
        >>> container = ValueContainer(message_type="test")
        >>> container.add(StringValue("name", "Alice"))
        >>> print(container.get_value("name").to_string())
        Alice
    """

    def add(self, value: Value, update_immediately: bool = False) -> Value:
        """Add a value to the container.

        Args:
            value: The value to add.
            update_immediately: If True, update internal state immediately.

        Returns:
            The added value.

        Raises:
            TypeError: If value is not a Value instance.
        """
        pass
```

### File Organization

```python
# 1. Module docstring
"""Container module for value management."""

# 2. Imports (sorted: stdlib, third-party, local)
import threading
from typing import Optional, List

from .core.value import Value
from .core.value_types import ValueType

# 3. Constants
DEFAULT_BUFFER_SIZE = 4096

# 4. Classes
class ValueContainer:
    """Container class definition."""
    pass

# 5. Functions
def create_container() -> ValueContainer:
    """Factory function."""
    pass
```

### Naming Conventions

```python
# Classes: PascalCase
class ValueContainer:
    pass

# Functions and methods: snake_case
def get_value(name: str) -> Optional[Value]:
    pass

# Constants: UPPER_SNAKE_CASE
MAX_VALUE_COUNT = 1000
DEFAULT_ENCODING = "utf-8"

# Private members: leading underscore
class Container:
    def __init__(self):
        self._internal_state = {}

    def _private_method(self):
        pass
```

---

## Testing Requirements

### Test Coverage

All contributions must include tests:
- Minimum 80% coverage for new code
- All public APIs must have tests
- Edge cases and error conditions must be tested

### Test Structure

```python
def test_feature_name_scenario():
    """Test description explaining what is tested."""
    # Arrange
    container = ValueContainer()

    # Act
    container.add(StringValue("key", "value"))
    result = container.get_value("key")

    # Assert
    assert result is not None
    assert result.to_string() == "value"
```

### Running Tests

```bash
# All tests
pytest

# With coverage
pytest --cov=container_module --cov-report=html

# Specific test
pytest tests/test_container.py::test_add_value

# Verbose
pytest -v
```

See [TESTING.md](docs/contributing/TESTING.md) for detailed testing guidelines.

---

## Pull Request Process

### Before Submitting

1. **Update from upstream**:
   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

2. **Run all checks**:
   ```bash
   black container_module tests
   mypy container_module
   pylint container_module
   pytest
   ```

3. **Update documentation** if needed

### Creating the PR

1. Push your branch:
   ```bash
   git push origin feature/your-feature
   ```

2. Create a pull request on GitHub

3. Fill out the PR template:
   - Description of changes
   - Related issue(s)
   - Testing performed
   - Breaking changes (if any)

### PR Title Format

```
type(scope): description

Examples:
feat(values): add ArrayValue type
fix(serialization): handle empty containers
docs(readme): update installation instructions
test(container): add thread safety tests
refactor(core): simplify value interface
```

### Review Process

1. **Automated checks**: CI must pass
2. **Code review**: At least one maintainer approval
3. **Testing**: Manual testing for complex changes
4. **Documentation**: Verify docs are updated

### After Merge

- Delete your branch
- Update local repository:
  ```bash
  git checkout main
  git pull upstream main
  git branch -d feature/your-feature
  ```

---

## Release Process

### Version Numbering

We follow [Semantic Versioning](https://semver.org/):
- **MAJOR**: Breaking API changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes (backward compatible)

### Release Checklist

1. Update CHANGELOG.md
2. Update version in `pyproject.toml` and `__init__.py`
3. Create release tag
4. Build and publish to PyPI
5. Write release notes

---

## Getting Help

- **Documentation**: [docs/README.md](docs/README.md)
- **FAQ**: [docs/guides/FAQ.md](docs/guides/FAQ.md)
- **Discussions**: [GitHub Discussions](https://github.com/kcenon/python_container_system/discussions)
- **Issues**: [GitHub Issues](https://github.com/kcenon/python_container_system/issues)

---

## Recognition

Contributors are recognized in:
- CHANGELOG.md for each release
- GitHub contributors page
- README.md acknowledgments section

Thank you for contributing to the Python Container System!

---

**Last Updated:** 2025-11-26
