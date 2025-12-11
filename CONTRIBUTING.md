# Contributing to Document Parser MCP

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## Development Setup

### 1. Fork and Clone

```bash
# Fork the repository on GitHub
# Then clone your fork
git clone https://github.com/YOUR_USERNAME/document-parser-mcp.git
cd document-parser-mcp
```

### 2. Set Up Development Environment

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -r requirements-dev.txt
pip install -e .
```

### 3. Create a Branch

```bash
git checkout -b feature/your-feature-name
```

## Development Workflow

### Code Style

We use several tools to maintain code quality:

```bash
# Format code with black
black document_parser tests

# Sort imports
isort document_parser tests

# Lint with ruff
ruff check document_parser tests

# Type checking
mypy document_parser
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=document_parser

# Run specific test file
pytest tests/test_config.py

# Run specific test
pytest tests/test_config.py::TestConfigurationModels::test_default_application_settings
```

### Writing Tests

- Write tests for all new functionality
- Maintain or improve test coverage
- Use descriptive test names
- Follow the existing test structure

Example test:

```python
def test_my_new_feature():
    """Test description of what this tests."""
    # Arrange
    input_data = "test"

    # Act
    result = my_function(input_data)

    # Assert
    assert result == expected_output
```

## Commit Guidelines

### Commit Message Format

We use conventional commits:

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks
- `perf`: Performance improvements

**Examples:**

```bash
git commit -m "feat(processor): add support for EPUB files"
git commit -m "fix(queue): resolve race condition in task dequeue"
git commit -m "docs: update README with new examples"
git commit -m "test: add tests for configuration validation"
```

## Pull Request Process

### 1. Update Your Branch

```bash
git fetch upstream
git rebase upstream/main
```

### 2. Push to Your Fork

```bash
git push origin feature/your-feature-name
```

### 3. Create Pull Request

- Go to GitHub and create a pull request
- Fill out the pull request template
- Link any related issues
- Ensure CI checks pass

### Pull Request Checklist

- [ ] Code follows project style guidelines
- [ ] Tests added for new functionality
- [ ] All tests pass
- [ ] Documentation updated
- [ ] Commit messages follow conventions
- [ ] No merge conflicts with main

## Code Review Process

### What to Expect

- Maintainers will review your PR
- You may be asked to make changes
- Discussion about implementation details
- Once approved, your PR will be merged

### Responding to Feedback

- Be respectful and professional
- Ask questions if feedback is unclear
- Make requested changes in new commits
- Push updates to your branch

## Areas for Contribution

### Good First Issues

Look for issues labeled `good first issue` for beginner-friendly tasks.

### Areas Needing Help

- **Documentation**: Improve guides, add examples
- **Tests**: Increase test coverage
- **Performance**: Optimize processing speed
- **Features**: Add support for new formats
- **Bug Fixes**: Fix reported issues

## Project Structure

```
document_parser/
├── config/          # Configuration system
├── core/            # Core exceptions and types
├── engine/          # Document processing
├── mcp/             # MCP server
├── processing/      # Job management
└── utils/           # Utilities
```

### Adding New Features

1. **Configuration**: Add settings to `config/models.py`
2. **Processing**: Implement logic in `engine/`
3. **MCP Tools**: Add tools in `mcp/tools.py`
4. **Handlers**: Implement in `mcp/handlers.py`
5. **Tests**: Add to `tests/`
6. **Documentation**: Update README and guides

## Documentation

### Updating Documentation

- Keep README.md up to date
- Add docstrings to all public APIs
- Update guides in `docs/`
- Add examples for new features

### Docstring Format

Use Google-style docstrings:

```python
def process_document(source: str, pipeline: str) -> str:
    """
    Process a document using specified pipeline.

    Args:
        source: Path or URL to document
        pipeline: Processing pipeline to use

    Returns:
        Markdown content

    Raises:
        ProcessingError: If processing fails
    """
    pass
```

## Release Process

Maintainers handle releases, but contributors should:

- Keep CHANGELOG.md updated
- Note breaking changes
- Update version numbers in PRs if needed

## Questions?

- Open an issue for discussion
- Join community chat (if available)
- Email maintainers

## Code of Conduct

Be respectful, inclusive, and professional in all interactions.

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

Thank you for contributing to Document Parser MCP! 🎉
