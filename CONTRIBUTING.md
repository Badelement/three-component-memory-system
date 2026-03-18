# Contributing to Three-Component Memory System

Thank you for your interest in contributing! This document provides guidelines and instructions for contributing to the project.

## 🎯 Code of Conduct

Please be respectful and considerate of others when contributing to this project. We aim to foster an inclusive and welcoming community.

## 🚀 Getting Started

### Development Environment Setup

1. **Fork and clone the repository**
   ```bash
   git clone https://github.com/yourusername/three-component-memory-system.git
   cd three-component-memory-system
   ```

2. **Set up virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install development dependencies**
   ```bash
   pip install -r requirements-dev.txt
   ```

4. **Run tests to verify setup**
   ```bash
   pytest tests/
   ```

## 📁 Project Structure

```
three-component-memory-system/
├── src/                    # Source code
│   ├── __init__.py        # Main entry point
│   ├── memory_core.py     # Core implementation
│   └── utils/             # Utility modules
├── docs/                  # Documentation
├── examples/              # Usage examples
├── tests/                 # Test suite
├── scripts/               # Utility scripts
└── pyproject.toml         # Project configuration
```

## 🔧 Development Workflow

### 1. Create a Branch
```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/issue-description
```

### 2. Make Changes
- Follow the existing code style
- Write tests for new functionality
- Update documentation as needed

### 3. Run Tests
```bash
# Run all tests
pytest tests/

# Run with coverage
pytest --cov=src tests/

# Run specific test file
pytest tests/test_basic.py -v
```

### 4. Code Quality Checks
```bash
# Format code with black
black src/ tests/

# Check code style with flake8
flake8 src/ tests/

# Type checking with mypy
mypy src/
```

### 5. Commit Changes
```bash
git add .
git commit -m "Description of changes"
```

### 6. Push and Create Pull Request
```bash
git push origin your-branch-name
```

Then create a Pull Request on GitHub.

## 📝 Coding Standards

### Python Style
- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/)
- Use type hints where appropriate
- Write docstrings for public functions and classes
- Keep functions focused and small

### Documentation
- Update relevant documentation files
- Add docstrings to new functions/classes
- Include examples for new features
- Update README if needed

### Testing
- Write unit tests for new functionality
- Maintain or improve test coverage
- Test edge cases and error conditions
- Use descriptive test names

## 🐛 Reporting Issues

When reporting issues, please include:

1. **Clear description** of the problem
2. **Steps to reproduce**
3. **Expected vs actual behavior**
4. **Environment information** (Python version, OS, etc.)
5. **Error messages** and stack traces

## 💡 Feature Requests

We welcome feature requests! When suggesting new features:

1. **Describe the problem** the feature would solve
2. **Explain the proposed solution**
3. **Provide use cases** or examples
4. **Consider alternatives** you've explored

## 🧪 Testing Guidelines

### Writing Tests
```python
def test_feature_description():
    """Test description of what is being tested."""
    # Arrange - set up test conditions
    # Act - perform the action being tested
    # Assert - verify the results
```

### Test Structure
- One assertion per test (when possible)
- Descriptive test names
- Use fixtures for common setup
- Mock external dependencies

### Running Tests
```bash
# Run all tests
pytest

# Run specific test
pytest tests/test_file.py::test_function

# Run with verbose output
pytest -v

# Run with coverage report
pytest --cov=src --cov-report=html
```

## 📚 Documentation

### Updating Documentation
- Keep documentation in sync with code changes
- Use clear, concise language
- Include code examples
- Update both `docs/` directory and docstrings

### Building Documentation
```bash
# Install documentation dependencies
pip install mkdocs mkdocs-material

# Serve documentation locally
mkdocs serve
```

## 🚀 Release Process

### Versioning
We follow [Semantic Versioning](https://semver.org/):
- **MAJOR** version for incompatible API changes
- **MINOR** version for new functionality (backwards compatible)
- **PATCH** version for bug fixes

### Release Checklist
- [ ] Update version in `src/__init__.py`
- [ ] Update CHANGELOG.md
- [ ] Run full test suite
- [ ] Update documentation
- [ ] Create GitHub release
- [ ] Update PyPI package (if applicable)

## 🤝 Getting Help

- **Documentation**: Check the `docs/` directory
- **Issues**: Search existing issues before creating new ones
- **Discussions**: Use GitHub Discussions for questions and ideas
- **Code Review**: Request review from maintainers

## 🙏 Acknowledgments

Thank you for contributing! Your efforts help make this project better for everyone.

---

**Last Updated**: 2026-03-18
