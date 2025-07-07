#!/bin/bash
# Development setup script for 2048-CLI

set -e

echo "Setting up 2048-CLI development environment..."

# Check if Python 3.13+ is available
if ! python3 --version | grep -E "3\.(13|14|15)" > /dev/null; then
    echo "Error: Python 3.13+ is required"
    echo "Current version: $(python3 --version)"
    exit 1
fi

# Install development dependencies
echo "Installing development dependencies..."
pip install -e ".[dev]"

# Install pre-commit hooks (optional)
read -p "Install pre-commit hooks? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "Installing pre-commit hooks..."
    pre-commit install
    echo "Pre-commit hooks installed. They will run automatically on git commit."
fi

# Run initial code quality checks
echo "Running initial code quality checks..."
echo "Running ruff linter..."
if ruff check src/; then
    echo "✓ Ruff linter passed"
else
    echo "⚠ Ruff linter found issues. Run 'make fix' to auto-fix some issues."
fi

echo "Running mypy type checker..."
if mypy src/; then
    echo "✓ MyPy type checker passed"
else
    echo "⚠ MyPy found type issues"
fi

echo "Running ruff formatter check..."
if ruff format --check src/; then
    echo "✓ Code formatting is correct"
else
    echo "⚠ Code formatting issues found. Run 'make format' to fix."
fi

echo ""
echo "Development environment setup complete!"
echo ""
echo "Available commands:"
echo "  make help       - Show all available commands"
echo "  make lint       - Run linter"
echo "  make format     - Format code"
echo "  make type-check - Run type checker"
echo "  make check      - Run all checks"
echo "  make fix        - Fix auto-fixable issues"
echo "  make build      - Build the application"
echo ""
echo "To run the game:"
echo "  python src/main.py"