# Calculation Service API

A production-ready FastAPI application demonstrating robust test automation and CI/CD practices. This project showcases comprehensive testing strategies, code quality gates, and automated deployment workflows.

## 🎯 Project Overview

This application provides a RESTful API for mathematical calculations with comprehensive test coverage and quality assurance. It demonstrates how automated testing improves code quality by:

- **Preventing regressions**: Automated tests catch bugs before they reach production
- **Enabling confident refactoring**: Tests provide safety net for code improvements
- **Documenting behavior**: Tests serve as living documentation of expected functionality
- **Improving design**: Writing testable code leads to better architecture
- **Reducing manual testing**: Automated validation reduces human error and time investment

## 🚀 Quickstart

### Prerequisites

- Python 3.12+
- pip or uv package manager
- Docker (optional, for containerized deployment)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd cs396Group
   ```

2. **Install dependencies**
   ```bash
   make install
   # or manually: pip install -e .[dev]
   ```

3. **Set up pre-commit hooks**
   ```bash
   pre-commit install
   ```

4. **Run the application**
   ```bash
   make run
   # or manually: uvicorn app.main:app --reload
   ```

The API will be available at `http://localhost:8000`

### API Documentation

- **Interactive docs**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## 🧪 Testing

### Running Tests

```bash
# Run all tests
make test

# Run tests with coverage
make cov

# Run specific test types
pytest tests/unit/          # Unit tests only
pytest tests/integration/   # Integration tests only
pytest tests/               # All tests
```

### Test Coverage

The project maintains **≥90% test coverage** enforced by CI/CD:

- **Unit Tests**: Test individual functions in isolation (`tests/test_services.py`)
- **Integration Tests**: Test API endpoints with TestClient (`tests/test_api.py`)
- **E2E Tests**: Test complete application flow (`tests/test_health.py`)

Coverage reports are generated in multiple formats:
- Terminal output with missing lines
- HTML report in `htmlcov/` directory
- XML report for CI integration

## 🛠️ Quality Gates

### Code Quality Tools

| Tool | Purpose | Command |
|------|---------|---------|
| **Black** | Code formatting | `make format` |
| **Ruff** | Linting and import sorting | `make lint` |
| **MyPy** | Static type checking | `make type` |
| **Pytest** | Testing framework | `make test` |

### Quality Thresholds

- **Test Coverage**: ≥90% (enforced in CI)
- **Code Formatting**: Black compliance (enforced in CI)
- **Linting**: Ruff compliance (enforced in CI)
- **Type Safety**: MyPy strict mode (enforced in CI)

### Fixing Quality Issues

```bash
# Auto-fix formatting and import issues
make format

# Check and fix linting issues
ruff check --fix app tests

# Run all quality checks
make all-checks
```

## 📋 API Endpoints

### Health Check
```http
GET /health
```
Returns service status and version information.

**Response:**
```json
{
  "status": "ok",
  "version": "1.0.0"
}
```

### Calculate Summary Statistics
```http
POST /calc/summarize
```

**Request Body:**
```json
{
  "values": [1.0, 2.0, 3.0, 4.0, 5.0]
}
```

**Response:**
```json
{
  "count": 5,
  "mean": 3.0,
  "min": 1.0,
  "max": 5.0
}
```

## 🐳 Docker Deployment

### Build and Run with Docker

```bash
# Build the Docker image
make docker-build

# Run the container
make docker-run

# Or use docker-compose for development
docker-compose up --build
```

### Production Deployment

```bash
# Build production image
docker build -t calculation-service:latest .

# Run with production settings
docker run -p 8000:8000 \
  -e ENVIRONMENT=production \
  -e DEBUG=false \
  calculation-service:latest
```

## 🔄 CI/CD Pipeline

The project uses GitHub Actions for continuous integration:

### Pipeline Steps

1. **Checkout code** and setup Python 3.12
2. **Cache dependencies** for faster builds
3. **Install dependencies** including dev tools
4. **Lint code** with Ruff (formatting and style)
5. **Type check** with MyPy (static analysis)
6. **Run tests** with pytest (unit, integration, E2E)
7. **Generate coverage** report (≥90% required)
8. **Upload artifacts** (coverage.xml, test results)

### Build Status

[![CI](https://github.com/your-org/cs396Group/workflows/CI/badge.svg)](https://github.com/your-org/cs396Group/actions)
[![Coverage](https://codecov.io/gh/your-org/cs396Group/branch/main/graph/badge.svg)](https://codecov.io/gh/your-org/cs396Group)

## 📊 Rubric Mapping

| Rubric Category | Implementation | Location |
|----------------|----------------|----------|
| **Functionality** | Complete API with health check and calculation endpoints | `app/main.py`, `app/services.py` |
| **Test Depth** | Unit, integration, and E2E tests with edge cases | `tests/test_*.py` |
| **Coverage** | ≥90% coverage enforced in CI | `pyproject.toml`, `.github/workflows/ci.yml` |
| **Code Quality** | Ruff, Black, MyPy with strict configurations | `pyproject.toml`, `.pre-commit-config.yaml` |
| **Documentation** | Comprehensive README with API docs | `README.md`, `app/main.py` (docstrings) |
| **Version Control** | Conventional commits, pre-commit hooks, CI/CD | `.pre-commit-config.yaml`, `.github/workflows/ci.yml` |

## 🔧 Development

### Pre-commit Hooks

Pre-commit hooks automatically run quality checks before each commit:

```bash
# Install pre-commit hooks
pre-commit install

# Run hooks manually
pre-commit run --all-files
```

### Available Make Commands

```bash
make help          # Show all available commands
make install       # Install dependencies
make format        # Format code with Black
make lint          # Lint with Ruff
make type          # Type check with MyPy
make test          # Run tests
make cov           # Run tests with coverage
make run           # Start development server
make clean         # Clean temporary files
make all-checks    # Run all quality checks
```

## 🚀 Future Improvements

### Advanced Testing Strategies

1. **Property-based Testing**: Use Hypothesis for generating test cases
   ```python
   from hypothesis import given, strategies as st
   
   @given(st.lists(st.floats(), min_size=1))
   def test_summarize_property(values):
       result = summarize(values)
       assert result["count"] == len(values)
       assert result["min"] <= result["mean"] <= result["max"]
   ```

2. **Fuzzing**: Implement fuzz testing for API endpoints
   ```python
   # Use tools like python-afl or custom fuzzers
   # to test edge cases and malformed inputs
   ```

3. **Mutation Testing**: Use mutmut to validate test quality
   ```bash
   pip install mutmut
   mutmut run
   ```

### Additional Quality Improvements

- **Security Scanning**: Add bandit for security vulnerability detection
- **Performance Testing**: Implement load testing with locust
- **Dependency Scanning**: Regular security updates and vulnerability checks
- **Database Testing**: Add database integration tests when data layer is added

## 📝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run quality checks (`make all-checks`)
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

### PR Checklist

- [ ] Tests pass locally
- [ ] Coverage ≥90%
- [ ] Code formatted with Black
- [ ] Linting passes with Ruff
- [ ] Type checking passes with MyPy
- [ ] Documentation updated
- [ ] Pre-commit hooks pass

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Team

CS396 Group Project - Demonstrating production-ready development practices with comprehensive testing and CI/CD.