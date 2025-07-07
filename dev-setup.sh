#!/bin/bash
# Development setup script for 2048-CLI
# Handles externally managed Python environments

set -e

echo "Setting up 2048-CLI development environment..."
echo "================================================"

# Check if Python 3.13+ is available
if ! python3 --version | grep -E "3\.(13|14|15)" > /dev/null; then
    echo "Error: Python 3.13+ is required"
    echo "Current version: $(python3 --version)"
    exit 1
fi

# Function to create virtual environment if needed
setup_venv() {
    if [ ! -d "venv" ]; then
        echo "Creating virtual environment..."
        python3 -m venv venv
    fi
    
    echo "Activating virtual environment..."
    source venv/bin/activate
    
    echo "Installing dependencies in virtual environment..."
    pip install -e ".[dev,build]"
}

# Check for externally managed environment
if python3 -c "import sys; import os; exit(1 if os.path.exists('/usr/lib/python*/EXTERNALLY-MANAGED') else 0)" 2>/dev/null; then
    echo "Externally managed Python environment detected"
    
    # Check if we have system packages available
    if command -v pacman &> /dev/null; then
        echo "Arch Linux detected - trying system packages first..."
        
        # Install basic Python tools if available
        echo "Installing system Python packages..."
        if pacman -Ss python-pip &> /dev/null; then
            sudo pacman -S --needed python-pip python-setuptools python-wheel || true
        fi
        
        # Install development tools if available
        echo "Installing development tools..."
        if pacman -Ss python-ruff &> /dev/null; then
            sudo pacman -S --needed python-ruff python-mypy || true
        fi
        
        # For PyInstaller, we'll use venv since it's not commonly packaged
        echo "Setting up virtual environment for remaining dependencies..."
        setup_venv
        
    else
        echo "Using virtual environment for all dependencies..."
        setup_venv
    fi
    
else
    echo "Standard Python environment detected"
    
    # Check if pip is available
    if ! command -v pip &> /dev/null; then
        echo "Installing pip..."
        python3 -m ensurepip --upgrade
    fi
    
    # Install development dependencies
    echo "Installing development dependencies..."
    pip install -e ".[dev,build]"
fi

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

# Check if tools are available
if command -v ruff &> /dev/null; then
    echo "Running ruff linter..."
    if ruff check src/; then
        echo "✓ Ruff linter passed"
    else
        echo "⚠ Ruff linter found issues. Run 'make fix' to auto-fix some issues."
    fi
    
    echo "Running ruff formatter check..."
    if ruff format --check src/; then
        echo "✓ Code formatting is correct"
    else
        echo "⚠ Code formatting issues found. Run 'make format' to fix."
    fi
else
    echo "⚠ Ruff not available. Install it or activate virtual environment."
fi

if command -v mypy &> /dev/null; then
    echo "Running mypy type checker..."
    if mypy src/; then
        echo "✓ MyPy type checker passed"
    else
        echo "⚠ MyPy found type issues"
    fi
else
    echo "⚠ MyPy not available. Install it or activate virtual environment."
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
echo ""
echo "Note: If using virtual environment, activate it first:"
echo "  source venv/bin/activate"