# MicroFrame CLI Documentation

The MicroFrame CLI provides a convenient command-line interface for common development tasks including running the dev server, testing, linting, and project scaffolding.

## Installation

The CLI is automatically installed when you install MicroFrame with Poetry:

```bash
poetry install
```

## Usage

### Basic Syntax

```bash
poetry run python microframe/cli.py [COMMAND] [OPTIONS]
```

Or if the package is installed globally:

```bash
microframe [COMMAND] [OPTIONS]
```

### Available Commands

#### `run-dev` - Launch Development Server

Start the development server with auto-reload enabled.

**Options:**
- `--host, -h TEXT`: Host to bind to (default: `0.0.0.0`)
- `--port, -p INTEGER`: Port to bind to (default: `8000`)
- `--reload/--no-reload`: Enable/disable auto-reload (default: enabled)
- `--app, -a TEXT`: Application path (default: `main:app`)

**Examples:**
```bash
# Start with defaults
poetry run python microframe/cli.py run-dev

# Custom port and host
poetry run python microframe/cli.py run-dev --port 3000 --host localhost

# Disable auto-reload
poetry run python microframe/cli.py run-dev --no-reload
```

---

#### `test` - Run Tests

Execute tests using pytest with optional coverage reporting.

**Options:**
- `--verbose, -v`: Verbose output
- `--coverage/--no-coverage`: Generate coverage report (default: enabled)
- `--path, -p TEXT`: Run specific test file or directory

**Examples:**
```bash
# Run all tests with coverage
poetry run python microframe/cli.py test

# Run tests without coverage
poetry run python microframe/cli.py test --no-coverage

# Run specific test file
poetry run python microframe/cli.py test --path tests/test_routing.py

# Verbose output
poetry run python microframe/cli.py test --verbose
```

---

#### `lint-fix` - Fix Code Style

Automatically fix code style issues using multiple tools in sequence:
1. **autopep8** - Fix PEP8 issues
2. **isort** - Sort imports
3. **black** - Format code
4. **autoflake** - Remove unused variables (conservative)

**Options:**
- `--skip-autoflake`: Skip the autoflake step

**Examples:**
```bash
# Fix all code style issues
poetry run python microframe/cli.py lint-fix

# Skip autoflake
poetry run python microframe/cli.py lint-fix --skip-autoflake
```

---

#### `lint-check` - Check Code Style

Check code style without making changes using black, flake8, and mypy.

**Options:**
- `--tool, -t TEXT`: Check specific tool only (black, flake8, or mypy)

**Examples:**
```bash
# Check all tools
poetry run python microframe/cli.py lint-check

# Check only with black
poetry run python microframe/cli.py lint-check --tool black

# Check only type hints
poetry run python microframe/cli.py lint-check --tool mypy
```

---

#### `clean` - Clean Generated Files

Remove generated files and caches including:
- `__pycache__` directories
- `*.pyc` and `*.pyo` files
- `.pytest_cache` directories
- `*.backup` files

**Examples:**
```bash
poetry run python microframe/cli.py clean
```

---

#### `build` - Build Project

Complete build process including clean, install, lint-fix, and tests.

**Options:**
- `--skip-tests`: Skip test execution
- `--production`: Build for production (creates distribution package)

**Examples:**
```bash
# Standard build
poetry run python microframe/cli.py build

# Build without running tests
poetry run python microframe/cli.py build --skip-tests

# Production build with package creation
poetry run python microframe/cli.py build --production
```

---

#### `start-project` - Create New Project

Create a new MicroFrame project from a template.

**Templates:**
- `basic`: Minimal setup with a single route
- `api`: REST API template with authentication
- `full`: Complete template with auth, database setup, and WebSocket support

**Options:**
- `--path, -p PATH`: Project directory path
- `--template, -t TEXT`: Template to use (default: `basic`)

**Examples:**
```bash
# Create basic project
poetry run python microframe/cli.py start-project my-app

# Create API project with auth
poetry run python microframe/cli.py start-project my-api --template api

# Create in specific directory
poetry run python microframe/cli.py start-project my-app --path /path/to/projects
```

**Generated Project Structure:**
```
my-app/
├── app/              # Application modules
│   └── __init__.py
├── tests/            # Test files
│   └── __init__.py
├── main.py           # Application entry point
├── requirements.txt  # Python dependencies
├── .env.example      # Environment template
├── .gitignore        # Git ignore rules
└── README.md         # Project documentation
```

---

#### `info` - Display Project Information

Show project information and available commands.

**Examples:**
```bash
poetry run python microframe/cli.py info
```

---

## Integration with Makefile

The CLI commands integrate with the existing Makefile. You can use either:

```bash
# Using CLI
poetry run python microframe/cli.py test

# Using Makefile
make test
```

## Development Workflow

### Typical Development Session

```bash
# 1. Start a new feature
poetry run python microframe/cli.py clean

# 2. Run development server
poetry run python microframe/cli.py run-dev

# 3. In another terminal, run tests on save
poetry run python microframe/cli.py test --verbose

# 4. Fix code style before committing
poetry run python microframe/cli.py lint-fix

# 5. Check everything passes
poetry run python microframe/cli.py lint-check
poetry run python microframe/cli.py test
```

### Pre-commit Checklist

```bash
# Clean and format
poetry run python microframe/cli.py clean
poetry run python microframe/cli.py lint-fix

# Verify
poetry run python microframe/cli.py lint-check
poetry run python microframe/cli.py test

# Optional: Full build
poetry run python microframe/cli.py build
```

### Creating a New Project

```bash
# Create API project
poetry run python microframe/cli.py start-project my-api --template api

# Navigate and setup
cd my-api
cp .env.example .env
pip install -r requirements.txt

# Start development
python main.py
# Or: poetry run python microframe/cli.py run-dev
```

## Rich Console Output

The CLI uses [Rich](https://rich.readthedocs.io/) for beautiful terminal output including:
- Colored text and panels
- Progress indicators and spinners
- Tables for organized information
- Syntax highlighting for code

## Shell Completion

Enable shell completion for faster command input:

```bash
# For bash
poetry run python microframe/cli.py --install-completion bash

# For zsh
poetry run python microframe/cli.py --install-completion zsh

# For fish
poetry run python microframe/cli.py --install-completion fish
```

## Troubleshooting

### Command not found

If you get "command not found" errors, ensure you're using the poetry environment:

```bash
poetry run python microframe/cli.py [command]
```

Or activate the virtual environment:

```bash
poetry shell
python microframe/cli.py [command]
```

### Import errors

If you encounter import errors, reinstall dependencies:

```bash
poetry install
```

### Permission errors

On Unix systems, you may need to make the CLI executable:

```bash
chmod +x microframe/cli.py
```

## Advanced Usage

### Chaining Commands

```bash
# Clean, lint, and test in one line
poetry run python microframe/cli.py clean && \
poetry run python microframe/cli.py lint-fix && \
poetry run python microframe/cli.py test
```

### Custom Application Paths

```bash
# Run different application
poetry run python microframe/cli.py run-dev --app "app.server:application"
```

### Environment-Specific Testing

```bash
# Test with specific environment
ENV=testing poetry run python microframe/cli.py test
```

## Contributing

To add new commands to the CLI:

1. Open `microframe/cli.py`
2. Add a new function decorated with `@app.command()`
3. Follow the existing pattern for options and documentation
4. Update this documentation file

Example:

```python
@app.command()
def my_command(
    option: str = typer.Option("default", "--option", "-o", help="My option"),
):
    """
    🎯 My new command description.
    
    Example:
        microframe my-command --option value
    """
    console.print("Executing my command...")
    # Command logic here
```

## See Also

- [MicroFrame Documentation](../README.md)
- [Development Guide](../FEATURES.md)
- [Architecture](../ARCHITECTURE.md)
