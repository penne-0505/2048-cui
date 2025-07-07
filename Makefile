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
	@if command -v poetry >/dev/null 2>&1; then \
		poetry run ruff check src/; \
	elif command -v ruff >/dev/null 2>&1; then \
		ruff check src/; \
	elif [ -f venv/bin/ruff ]; then \
		venv/bin/ruff check src/; \
	else \
		echo "Error: ruff not found. Run 'poetry install -E dev' or activate virtual environment"; \
		exit 1; \
	fi

# Format code
format:
	@if command -v poetry >/dev/null 2>&1; then \
		poetry run ruff format src/; \
	elif command -v ruff >/dev/null 2>&1; then \
		ruff format src/; \
	elif [ -f venv/bin/ruff ]; then \
		venv/bin/ruff format src/; \
	else \
		echo "Error: ruff not found. Run 'poetry install -E dev' or activate virtual environment"; \
		exit 1; \
	fi

# Run type checker
type-check:
	@if command -v poetry >/dev/null 2>&1; then \
		poetry run mypy src/; \
	elif command -v mypy >/dev/null 2>&1; then \
		mypy src/; \
	elif [ -f venv/bin/mypy ]; then \
		venv/bin/mypy src/; \
	else \
		echo "Error: mypy not found. Run 'poetry install -E dev' or activate virtual environment"; \
		exit 1; \
	fi

# Run all checks
check: lint type-check
	@echo "All checks completed"

# Fix auto-fixable issues
fix:
	@if command -v poetry >/dev/null 2>&1; then \
		poetry run ruff check --fix src/; \
		poetry run ruff format src/; \
	elif command -v ruff >/dev/null 2>&1; then \
		ruff check --fix src/; \
		ruff format src/; \
	elif [ -f venv/bin/ruff ]; then \
		venv/bin/ruff check --fix src/; \
		venv/bin/ruff format src/; \
	else \
		echo "Error: ruff not found. Run 'poetry install -E dev' or activate virtual environment"; \
		exit 1; \
	fi

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