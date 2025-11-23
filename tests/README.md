# MicroFrame Test Suite

Comprehensive test suite for the MicroFrame framework and MicroUI component library.

## 📁 Test Structure

```
tests/
├── conftest.py              # Pytest configuration and shared fixtures
├── microframe/              # Framework core tests
│   ├── test_application.py  # Application class tests
│   ├── test_router.py       # Router and routing tests
│   ├── test_dependencies.py # Dependency injection tests
│   ├── test_validation.py   # Request validation tests
│   ├── test_config.py       # AppConfig tests
│   ├── test_exceptions.py   # Exception handling tests
│   └── test_middleware.py   # Middleware tests (CORS, Security)
├── microui/                 # MicroUI component tests
│   └── test_components.py   # UI component tests
└── test_integration.py      # End-to-end integration tests
```

## 🚀 Running Tests

### Run all tests
```bash
pytest tests/ -v
```

### Run specific test file
```bash
pytest tests/microframe/test_application.py -v
```

### Run with coverage
```bash
pytest tests/ --cov=microframe --cov=microui --cov-report=html
```

### Run tests matching a pattern
```bash
pytest tests/ -k "test_router" -v
```

### Run only integration tests
```bash
pytest tests/test_integration.py -v
```

## 📊 Test Coverage

### MicroFrame Core Tests

**Application Tests** (`test_application.py`)
- ✅ Application initialization
- ✅ Route registration (GET, POST, PUT, PATCH, DELETE)
- ✅ Path parameters
- ✅ Request body validation
- ✅ Router inclusion
- ✅ Sync and async handlers

**Router Tests** (`test_router.py`)
- ✅ Router initialization and configuration
- ✅ HTTP method decorators
- ✅ Nested router inclusion
- ✅ Tag merging
- ✅ Path parameter handling
- ✅ Prefix normalization

**Dependency Injection Tests** (`test_dependencies.py`)
- ✅ Simple dependencies
- ✅ Nested dependencies
- ✅ Async dependencies
- ✅ Request-aware dependencies
- ✅ Multiple dependencies
- ✅ Dependency caching
- ✅ DependencyManager direct testing

**Validation Tests** (`test_validation.py`)
- ✅ Valid request body parsing
- ✅ Invalid request handling (422 errors)
- ✅ Field constraints (min, max, regex)
- ✅ Nested Pydantic models
- ✅ Optional fields
- ✅ List field validation

**Config Tests** (`test_config.py`)
- ✅ Default configuration
- ✅ Custom configuration
- ✅ Documentation endpoints
- ✅ CORS configuration
- ✅ Security settings

**Exception Tests** (`test_exceptions.py`)
- ✅ NotFoundException (404)
- ✅ UnauthorizedException (401)
- ✅ ForbiddenException (403)
- ✅ BadRequestException (400)
- ✅ Generic exception handling (500)
- ✅ Route not found (404)

**Middleware Tests** (`test_middleware.py`)
- ✅ CORS headers
- ✅ CORS preflight requests
- ✅ Wildcard origins
- ✅ Security headers

### MicroUI Component Tests

**Component Tests** (`test_components.py`)
- ✅ Button rendering
- ✅ Card rendering
- ✅ Alert rendering
- ✅ Input rendering
- ✅ HTMX integration
- ✅ Modal rendering
- ✅ Table rendering
- ✅ Badge rendering
- ✅ Navbar rendering
- ✅ Advanced components (Sidebar, Tabs, Avatar, Progress, Stats)
- ✅ Layout components (Pricing, Contact Form)

### Integration Tests

**Integration Tests** (`test_integration.py`)
- ✅ Full CRUD API flow
- ✅ Nested routers with dependencies
- ✅ Middleware + validation integration
- ✅ OpenAPI documentation generation

## 🔧 Fixtures

### Available Fixtures (from `conftest.py`)

- **`app_config`** - Pre-configured AppConfig for testing
- **`app`** - Basic Application instance
- **`client`** - AsyncClient for making HTTP requests
- **`sample_routes`** - Sample route data for testing

## 📝 Writing New Tests

### Example Test

```python
import pytest
from httpx import AsyncClient
from microframe import Application

@pytest.mark.asyncio
async def test_my_feature():
    """Test description"""
    app = Application()
    
    @app.get("/test")
    async def test_route():
        return {"message": "ok"}
    
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/test")
        assert response.status_code == 200
        assert response.json() == {"message": "ok"}
```

### Test Best Practices

1. **Use descriptive test names** - `test_router_includes_nested_routes`
2. **One assertion per concept** - Test one thing at a time
3. **Use fixtures** - Leverage pytest fixtures for common setup
4. **Test edge cases** - Include error conditions and boundary cases
5. **Async tests** - Mark async tests with `@pytest.mark.asyncio`

## 🐛 Debugging Tests

### Run with verbose output
```bash
pytest tests/ -vv
```

### Show print statements
```bash
pytest tests/ -s
```

### Stop on first failure
```bash
pytest tests/ -x
```

### Run last failed tests
```bash
pytest tests/ --lf
```

### Debug with pdb
```bash
pytest tests/ --pdb
```

## 📈 CI/CD Integration

Add to your CI pipeline:

```yaml
# .github/workflows/test.yml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      - name: Install dependencies
        run: |
          pip install -e .
          pip install pytest pytest-asyncio pytest-cov httpx
      - name: Run tests
        run: pytest tests/ --cov --cov-report=xml
      - name: Upload coverage
        uses: codecov/codecov-action@v2
```

## 🎯 Test Goals

- ✅ **High Coverage** - Aim for >80% code coverage
- ✅ **Fast Execution** - Tests should run quickly
- ✅ **Isolated** - Tests don't depend on each other
- ✅ **Reliable** - Tests are deterministic
- ✅ **Readable** - Clear test names and structure

## 📚 Additional Resources

- [pytest documentation](https://docs.pytest.org/)
- [pytest-asyncio](https://github.com/pytest-dev/pytest-asyncio)
- [HTTPX testing](https://www.python-httpx.org/advanced/#calling-into-python-web-apps)
- [MicroFrame documentation](../README.md)
