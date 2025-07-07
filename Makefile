# 2048-CLI Development Makefile

.PHONY: help install lint format type-check test clean build dev-install

# Default target
help:
	@echo "Available targets:"
	@echo "  install     - Install production dependencies"
	@echo "  dev-install - Install development dependencies"
	@echo "  lint        - Run ruff linter"
	@echo "  format      - Format code with ruff"
	@echo "  type-check  - Run mypy type checker"
	@echo "  check       - Run all checks (lint + type-check)"
	@echo "  fix         - Fix auto-fixable issues"
	@echo "  test        - Run tests (when available)"
	@echo "  clean       - Clean build artifacts"
	@echo "  build       - Build the application"

# Install production dependencies
install:
	pip install -e .

# Install development dependencies
dev-install:
	pip install -e ".[dev]"

# Run linter
lint:
	ruff check src/

# Format code
format:
	ruff format src/

# Run type checker
type-check:
	mypy src/

# Run all checks
check: lint type-check
	@echo "All checks completed"

# Fix auto-fixable issues
fix:
	ruff check --fix src/
	ruff format src/

# Run tests (placeholder for future test implementation)
test:
	@echo "No tests configured yet"

# Clean build artifacts
clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

# Build the application
build: clean
	python build.py