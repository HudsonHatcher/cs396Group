# Makefile for Calculation Service API
# Provides convenient commands for development and deployment

.PHONY: help install format lint type test cov run clean docker-build docker-run

# Default target
help:
	@echo "Available commands:"
	@echo "  install     - Install dependencies"
	@echo "  format      - Format code with black"
	@echo "  lint        - Lint code with ruff"
	@echo "  type        - Type check with mypy"
	@echo "  test        - Run tests with pytest"
	@echo "  cov         - Run tests with coverage report"
	@echo "  run         - Run the application locally"
	@echo "  clean       - Clean up temporary files"
	@echo "  docker-build - Build Docker image"
	@echo "  docker-run  - Run Docker container"
	@echo "  all-checks  - Run format, lint, type, and test"

# Install dependencies
install:
	pip install -e .[dev]
	pre-commit install

# Format code
format:
	black app tests
	ruff format app tests

# Lint code
lint:
	ruff check app tests
	ruff format --check app tests

# Type check
type:
	mypy app

# Run tests
test:
	pytest

# Run tests with coverage
cov:
	pytest --cov=app --cov-report=term-missing --cov-report=html
	@echo "Coverage report generated in htmlcov/index.html"

# Run the application
run:
	uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Clean up temporary files
clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf build/
	rm -rf dist/
	rm -rf htmlcov/
	rm -rf .coverage
	rm -rf coverage.xml
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	rm -rf .ruff_cache/

# Build Docker image
docker-build:
	docker build -t calculation-service:latest .

# Run Docker container
docker-run:
	docker run -p 8000:8000 calculation-service:latest

# Run all quality checks
all-checks: format lint type test
	@echo "All quality checks passed!"

# Development setup
dev-setup: install
	@echo "Development environment setup complete!"
	@echo "Run 'make run' to start the development server"
