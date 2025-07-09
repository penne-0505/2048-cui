#!/bin/bash
# Development setup script for 2048-CLI
# Uses pyenv + poetry for Python environment management

set -e

echo "Setting up 2048-CLI development environment..."
echo "================================================"

# Check if pyenv is installed
if ! command -v pyenv &> /dev/null; then
    echo "Error: pyenv is not installed"
    echo "Please install pyenv first: https://github.com/pyenv/pyenv#installation"
    exit 1
fi

# Check if poetry is installed
if ! command -v poetry &> /dev/null; then
    echo "Error: poetry is not installed"
    echo "Please install poetry first: https://python-poetry.org/docs/#installation"
    exit 1
fi

# Read required Python version from pyproject.toml
REQUIRED_PYTHON_VERSION=$(grep -E "^python\s*=" pyproject.toml | sed 's/.*"\([^"]*\)".*/\1/' | sed 's/[^0-9.]*\([0-9.]*\).*/\1/')

if [ -z "$REQUIRED_PYTHON_VERSION" ]; then
    echo "Error: Could not determine required Python version from pyproject.toml"
    exit 1
fi

echo "Required Python version: $REQUIRED_PYTHON_VERSION"

# Check if the required Python version is available in pyenv
if ! pyenv versions | grep -q "$REQUIRED_PYTHON_VERSION"; then
    echo "Installing Python $REQUIRED_PYTHON_VERSION with pyenv..."
    pyenv install "$REQUIRED_PYTHON_VERSION"
fi

# Set the local Python version
echo "Setting local Python version to $REQUIRED_PYTHON_VERSION..."
pyenv local "$REQUIRED_PYTHON_VERSION"

# Verify Python version
echo "Verifying Python version..."
python --version

# Install dependencies with poetry
echo "Installing dependencies with poetry..."
poetry install --with dev,build

# Install pre-commit hooks (optional)
read -p "Install pre-commit hooks? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "Installing pre-commit hooks..."
    poetry run pre-commit install
    echo "Pre-commit hooks installed. They will run automatically on git commit."
fi

# Run initial code quality checks
echo "Running initial code quality checks..."

echo "Running ruff linter..."
if poetry run ruff check src/; then
    echo "✓ Ruff linter passed"
else
    echo "⚠ Ruff linter found issues. Run 'make fix' to auto-fix some issues."
fi

echo "Running ruff formatter check..."
if poetry run ruff format --check src/; then
    echo "✓ Code formatting is correct"
else
    echo "⚠ Code formatting issues found. Run 'make format' to fix."
fi

echo "Running mypy type checker..."
if poetry run mypy src/; then
    echo "✓ MyPy type checker passed"
else
    echo "⚠ MyPy found type issues"
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
echo "  poetry run python src/main.py"
echo ""
echo "Note: Poetry will automatically manage the virtual environment."
echo "To activate the poetry shell: poetry shell"