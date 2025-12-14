"""
MicroFrame CLI - Development and project management commands.

This CLI provides a convenient interface for common development tasks
including running the dev server, testing, linting, and project scaffolding.
"""

import shutil
import subprocess
import sys
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.syntax import Syntax
from rich.table import Table
from rich.tree import Tree

app = typer.Typer(
    name="microframe",
    help="🚀 MicroFrame CLI - ASGI microframework development tools",
    add_completion=True,
)

console = Console()


def run_command(
    command: str,
    description: str,
    shell: bool = True,
    capture_output: bool = False,
    show_spinner: bool = True,
) -> tuple[int, str, str]:
    """
    Execute a shell command with rich output.

    Args:
        command: Command to execute
        description: Human-readable description for display
        shell: Whether to run through shell
        capture_output: Whether to capture stdout/stderr
        show_spinner: Whether to show a spinner during execution

    Returns:
        Tuple of (exit_code, stdout, stderr)
    """
    if show_spinner and not capture_output:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            progress.add_task(description=description, total=None)
            result = subprocess.run(
                command,
                shell=shell,
                capture_output=capture_output,
                text=True,
            )
    else:
        if not capture_output:
            console.print(f"[cyan]▶[/cyan] {description}")
        result = subprocess.run(
            command,
            shell=shell,
            capture_output=capture_output,
            text=True,
        )

    stdout = result.stdout if capture_output else ""
    stderr = result.stderr if capture_output else ""

    return result.returncode, stdout, stderr


@app.command()
def run_dev(
    host: str = typer.Option("0.0.0.0", "--host", "-h", help="Host to bind to"),
    port: int = typer.Option(8000, "--port", "-p", help="Port to bind to"),
    reload: bool = typer.Option(True, "--reload/--no-reload", help="Enable auto-reload"),
    app_path: str = typer.Option("main:app", "--app", "-a", help="Application path"),
):
    """
    🚀 Launch the development server with auto-reload.

    Example:
        microframe run-dev
        microframe run-dev --port 3000 --host localhost
    """
    console.print(
        Panel.fit(
            "🚀 Starting MicroFrame Development Server",
            border_style="cyan",
        )
    )

    reload_flag = "--reload" if reload else ""
    command = f"poetry run uvicorn {app_path} {reload_flag} --host {host} --port {port}"

    console.print(f"[green]→[/green] Server: [bold]http://{host}:{port}[/bold]")
    console.print(f"[green]→[/green] App: [bold]{app_path}[/bold]")
    console.print(
        f"[green]→[/green] Auto-reload: [bold]{'enabled' if reload else 'disabled'}[/bold]\n"
    )

    try:
        subprocess.run(command, shell=True)
    except KeyboardInterrupt:
        console.print("\n[yellow]Server stopped[/yellow]")


@app.command()
def test(
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Verbose output"),
    coverage: bool = typer.Option(
        True, "--coverage/--no-coverage", help="Generate coverage report"
    ),
    path: Optional[str] = typer.Option(None, "--path", "-p", help="Specific test path"),
    watch: bool = typer.Option(False, "--watch", "-w", help="Watch mode with pytest-watch"),
):
    """
    🧪 Run tests with pytest.

    Example:
        microframe test
        microframe test --verbose --no-coverage
        microframe test --path tests/test_routing.py
        microframe test --watch
    """
    console.print(
        Panel.fit(
            "🧪 Running Tests",
            border_style="green",
        )
    )

    if watch:
        command = "poetry run ptw"
        console.print("[yellow]→[/yellow] Running in watch mode (Ctrl+C to stop)")
        try:
            subprocess.run(command, shell=True)
        except KeyboardInterrupt:
            console.print("\n[yellow]Watch mode stopped[/yellow]")
        return

    cmd_parts = ["poetry run pytest"]

    if verbose:
        cmd_parts.append("--verbose")

    if coverage:
        cmd_parts.extend(
            ["--cov", "--cov-branch", "--cov=microframe", "--cov-report=xml", "--cov-report=html"]
        )

    if path:
        cmd_parts.append(path)

    command = " ".join(cmd_parts)

    exit_code, _, _ = run_command(
        command,
        "Running pytest...",
        show_spinner=False,
    )

    if exit_code == 0:
        console.print("\n[green]✓[/green] Tests passed!")
        if coverage:
            console.print("[cyan]→[/cyan] Coverage report: htmlcov/index.html")
    else:
        console.print("\n[red]✗[/red] Tests failed!")
        sys.exit(exit_code)


@app.command()
def lint_fix(
    skip_autoflake: bool = typer.Option(False, "--skip-autoflake", help="Skip autoflake step"),
):
    """
    🔧 Automatically fix code style issues (black, isort, autopep8, autoflake).

    This command runs multiple formatters in sequence:
    1. autopep8 - Fix PEP8 issues
    2. isort - Sort imports
    3. black - Format code
    4. autoflake - Remove unused variables (conservative)

    Example:
        microframe lint-fix
        microframe lint-fix --skip-autoflake
    """
    console.print(
        Panel.fit(
            "🔧 Fixing Code Style",
            border_style="blue",
        )
    )

    steps = [
        (
            "poetry run autopep8 --in-place --recursive --exclude=alembic,static,__pycache__ .",
            "Running autopep8...",
        ),
        (
            "poetry run isort . --skip=alembic --skip=static --skip=__pycache__",
            "Sorting imports with isort...",
        ),
        ('poetry run black . --exclude="(alembic|static|__pycache__)"', "Formatting with black..."),
    ]

    if not skip_autoflake:
        steps.append(
            (
                "poetry run autoflake --in-place --recursive --remove-unused-variables --ignore-init-module-imports --exclude=alembic,static,__pycache__ .",
                "Removing unused variables with autoflake...",
            )
        )

    for command, description in steps:
        exit_code, _, _ = run_command(command, description)
        if exit_code != 0:
            console.print(f"[red]✗[/red] {description.split('...')[0]} failed!")
            sys.exit(exit_code)

    console.print("\n[green]✓[/green] Code style fixed successfully!")


@app.command()
def lint_check(
    tool: Optional[str] = typer.Option(
        None, "--tool", "-t", help="Specific tool: black, flake8, mypy"
    ),
):
    """
    🔍 Check code style without making changes.

    Example:
        microframe lint-check
        microframe lint-check --tool black
    """
    console.print(
        Panel.fit(
            "🔍 Checking Code Style",
            border_style="yellow",
        )
    )

    tools = {
        "black": ("poetry run black --check .", "Checking with black..."),
        "flake8": ("poetry run flake8 microframe tests", "Checking with flake8..."),
        "mypy": ("poetry run mypy microframe", "Type checking with mypy..."),
    }

    if tool:
        if tool not in tools:
            console.print(f"[red]✗[/red] Unknown tool: {tool}")
            console.print(f"Available tools: {', '.join(tools.keys())}")
            sys.exit(1)
        tools_to_run = {tool: tools[tool]}
    else:
        tools_to_run = tools

    failed = []

    for tool_name, (command, description) in tools_to_run.items():
        exit_code, _, _ = run_command(command, description, show_spinner=False)
        if exit_code != 0:
            failed.append(tool_name)

    if failed:
        console.print(f"\n[red]✗[/red] Failed checks: {', '.join(failed)}")
        console.print("[yellow]→[/yellow] Run [cyan]microframe lint-fix[/cyan] to auto-fix issues")
        sys.exit(1)
    else:
        console.print("\n[green]✓[/green] All checks passed!")


@app.command()
def clean(
    all: bool = typer.Option(False, "--all", help="Clean everything including venv and dist"),
):
    """
    🧹 Clean up generated files (__pycache__, *.pyc, *.pyo, .pytest_cache).

    Example:
        microframe clean
        microframe clean --all
    """
    console.print(
        Panel.fit(
            "🧹 Cleaning Project",
            border_style="red",
        )
    )

    commands = [
        (
            'find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true',
            "Removing __pycache__ directories...",
        ),
        (
            'find . -type f \\( -name "*.pyc" -o -name "*.pyo" \\) -exec rm -f {} + 2>/dev/null || true',
            "Removing .pyc and .pyo files...",
        ),
        (
            'find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true',
            "Removing pytest cache...",
        ),
        (
            'find . -type f \\( -name "*.backup" \\) -exec rm -f {} + 2>/dev/null || true',
            "Removing backup files...",
        ),
    ]

    for command, description in commands:
        run_command(command, description)

    if all:
        console.print("[yellow]→[/yellow] Cleaning additional files...")
        additional = [
            ("rm -rf .venv venv", "Removing virtual environments..."),
            ("rm -rf dist build *.egg-info", "Removing build artifacts..."),
            ("rm -rf .mypy_cache .coverage htmlcov", "Removing cache and coverage..."),
        ]
        for command, description in additional:
            run_command(command, description)

    console.print("\n[green]✓[/green] Project cleaned successfully!")


@app.command()
def build(
    skip_tests: bool = typer.Option(False, "--skip-tests", help="Skip test execution"),
    production: bool = typer.Option(False, "--production", help="Build for production"),
):
    """
    🏗️ Build the project (clean, install, lint-fix, test).

    Example:
        microframe build
        microframe build --skip-tests
        microframe build --production
    """
    console.print(
        Panel.fit(
            "🏗️ Building Project",
            border_style="magenta",
        )
    )

    # Clean
    console.print("\n[cyan]Step 1:[/cyan] Cleaning...")
    subprocess.run("microframe clean", shell=True)

    # Install
    console.print("\n[cyan]Step 2:[/cyan] Installing dependencies...")
    exit_code, _, _ = run_command("poetry install", "Installing with poetry...")
    if exit_code != 0:
        console.print("[red]✗[/red] Installation failed!")
        sys.exit(exit_code)

    # Lint fix
    console.print("\n[cyan]Step 3:[/cyan] Fixing code style...")
    subprocess.run("microframe lint-fix", shell=True)

    # Tests
    if not skip_tests:
        console.print("\n[cyan]Step 4:[/cyan] Running tests...")
        subprocess.run("microframe test", shell=True)

    # Production build
    if production:
        console.print("\n[cyan]Step 5:[/cyan] Building package...")
        exit_code, _, _ = run_command("poetry build --no-cache", "Building with poetry...")
        if exit_code != 0:
            console.print("[red]✗[/red] Build failed!")
            sys.exit(exit_code)

    console.print("\n[green]✓[/green] Build completed successfully!")


@app.command()
def new(
    name: str = typer.Argument(..., help="Project name"),
    path: Optional[Path] = typer.Option(None, "--path", "-p", help="Project path"),
    template: str = typer.Option("basic", "--template", "-t", help="Template: basic, api, full"),
    no_git: bool = typer.Option(False, "--no-git", help="Skip git initialization"),
):
    """
    🎨 Create a new MicroFrame project from template.

    Templates:
      - basic: Minimal setup with single route
      - api: REST API template with auth
      - full: Complete template with auth, database, and WebSocket

    Example:
        microframe new my-api
        microframe new my-api --template api
        microframe new my-api --path /path/to/projects
    """
    console.print(
        Panel.fit(
            f"🎨 Creating New Project: {name}",
            border_style="cyan",
        )
    )

    # Determine project path
    project_path = path / name if path else Path.cwd() / name

    if project_path.exists():
        console.print(f"[red]✗[/red] Directory already exists: {project_path}")
        sys.exit(1)

    console.print(f"[green]→[/green] Creating project at: {project_path}")
    console.print(f"[green]→[/green] Template: {template}\n")

    try:
        # Create project structure
        project_path.mkdir(parents=True, exist_ok=True)

        # Basic structure
        (project_path / "app").mkdir(exist_ok=True)
        (project_path / "app" / "__init__.py").write_text("")
        (project_path / "tests").mkdir(exist_ok=True)
        (project_path / "tests" / "__init__.py").write_text("")

        # Create main.py based on template
        if template == "basic":
            main_content = '''
            """
            MicroFrame Application - Basic Template
            """
            from microframe import Application, AppConfig

            # Configuration
            config = AppConfig(
                title="{name}",
                version="1.0.0",
                debug=True,
            )

            # Create application
            app = Application(configuration=config)


            @app.get("/")
            async def index():
                """Root endpoint."""
                return {{"message": "Hello from MicroFrame!", "app": "{name}"}}


            @app.get("/health")
            async def health():
                """Health check endpoint."""
                return {{"status": "healthy"}}


            if __name__ == "__main__":
                import uvicorn
                uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
            '''
        elif template == "api":
            main_content = '''
"""
MicroFrame Application - REST API Template
"""
from microframe import Application, AppConfig, Router
from microframe import AuthConfig, AuthManager, create_auth_router
from typing import Optional, Dict, Any

# Configuration
config = AppConfig(
    title="{name} API",
    version="1.0.0",
    debug=True,
    docs_url="/docs",
    redoc_url="/redoc",
)

auth_config = AuthConfig(
    secret_key="your-secret-key-change-in-production",
    access_token_expire_minutes=15,
    refresh_token_expire_days=7,
)

# Create application
app = Application(configuration=config)


# Custom AuthManager implementation
class InMemoryAuthManager(AuthManager):
    """Simple in-memory auth manager for development."""
    
    users = {{
        "admin@example.com": {{
            "id": "1",
            "email": "admin@example.com",
            "password": "admin123",  # In production, use hashed passwords
            "name": "Admin User",
        }}
    }}
    
    async def authenticate(self, email: str, password: str) -> Optional[Dict[str, Any]]:
        user = self.users.get(email)
        if user and user["password"] == password:
            return {{"id": user["id"], "email": user["email"], "name": user["name"]}}
        return None
    
    async def get_user_by_id(self, user_id: str) -> Optional[Dict[str, Any]]:
        for user in self.users.values():
            if user["id"] == user_id:
                return {{"id": user["id"], "email": user["email"], "name": user["name"]}}
        return None
    
    async def get_user_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        user = self.users.get(email)
        if user:
            return {{"id": user["id"], "email": user["email"], "name": user["name"]}}
        return None


# Setup auth
app.state.auth_config = auth_config
app.state.auth_manager = InMemoryAuthManager()

# Create routers
api_router = Router(prefix="/api/v1", tags=["API"])
auth_router = create_auth_router()


@api_router.get("/")
async def api_root():
    """API root endpoint."""
    return {{"message": "Welcome to {name} API", "version": "1.0.0"}}


@app.get("/")
async def index():
    """Root endpoint."""
    return {{
        "app": "{name}",
        "docs": "/docs",
        "api": "/api/v1",
        "auth": "/auth"
    }}


# Include routers
app.include_router(api_router)
app.include_router(auth_router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
'''
        else:  # full template
            main_content = '''"""
MicroFrame Application - Full Template
"""
from microframe import Application, AppConfig, Router
from microframe import AuthConfig, AuthManager, create_auth_router
from typing import Optional, Dict, Any

# Configuration
config = AppConfig(
    title="{name}",
    version="1.0.0",
    debug=True,
    docs_url="/docs",
    redoc_url="/redoc",
)

auth_config = AuthConfig(
    secret_key="your-secret-key-change-in-production",
)

# Create application
app = Application(configuration=config)

# TODO: Implement your AuthManager
# TODO: Setup database connection
# TODO: Add WebSocket endpoints if needed


@app.get("/")
async def index():
    """Root endpoint."""
    return {{
        "app": "{name}",
        "docs": "/docs",
    }}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
'''

        main_content = main_content.format(name=name)
        (project_path / "main.py").write_text(main_content)

        # Create requirements.txt
        requirements = """
microframe>=2.0.0
uvicorn[standard]>=0.29.0
python-dotenv>=1.0.0
"""
        (project_path / "requirements.txt").write_text(requirements)

        # Create .env.example
        env_example = """# Environment Configuration
SECRET_KEY=your-secret-key-here-change-in-production
DEBUG=true
HOST=0.0.0.0
PORT=8000
"""
        (project_path / ".env.example").write_text(env_example)

        # Create .gitignore
        gitignore = """__pycache__/
*.py[cod]
*$py.class
*.so
.env
.venv
venv/
*.log
.pytest_cache/
.coverage
htmlcov/
dist/
build/
*.egg-info/
.mypy_cache/
.ruff_cache/
"""
        (project_path / ".gitignore").write_text(gitignore)

        # Create README.md
        readme = f"""# {name}

A MicroFrame application.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure environment:
```bash
cp .env.example .env
# Edit .env with your configuration
```

3. Run development server:
```bash
python main.py
```

Or with microframe CLI:
```bash
microframe run-dev
```

## API Documentation

- Interactive docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Project Structure

```
{name}/
├── app/              # Application modules
├── tests/            # Test files
├── main.py           # Application entry point
├── requirements.txt  # Dependencies
└── .env.example      # Environment template
```

## Development

```bash
# Run tests
microframe test

# Fix code style
microframe lint-fix

# Check code style
microframe lint-check

# Clean project
microframe clean
```
"""
        (project_path / "README.md").write_text(readme)

        # Initialize git
        if not no_git:
            console.print("[cyan]→[/cyan] Initializing git repository...")
            subprocess.run("git init", cwd=project_path, shell=True, capture_output=True)
            subprocess.run("git add .", cwd=project_path, shell=True, capture_output=True)
            subprocess.run(
                'git commit -m "Initial commit"',
                cwd=project_path,
                shell=True,
                capture_output=True,
            )

        console.print("[green]✓[/green] Project structure created!")

        # Show summary
        tree = Tree(f"[bold cyan]{name}/[/bold cyan]", guide_style="dim")
        tree.add("[cyan]app/[/cyan] - Application modules")
        tree.add("[cyan]tests/[/cyan] - Test files")
        tree.add("[white]main.py[/white] - Application entry point")
        tree.add("[white]requirements.txt[/white] - Dependencies")
        tree.add("[white].env.example[/white] - Environment template")
        tree.add("[white].gitignore[/white] - Git ignore rules")
        tree.add("[white]README.md[/white] - Documentation")

        console.print(tree)

        # Next steps
        console.print(f"\n[bold green]✓ Project created successfully![/bold green]")
        console.print(f"\n[bold]Next steps:[/bold]")
        console.print(f"  [cyan]cd {name}[/cyan]")
        console.print("  [cyan]pip install -r requirements.txt[/cyan]")
        console.print("  [cyan]cp .env.example .env[/cyan]")
        console.print("  [cyan]python main.py[/cyan]")
        console.print("\n[dim]Or use: [cyan]microframe run-dev[/cyan][/dim]")

    except Exception as e:
        console.print(f"[red]✗[/red] Error creating project: {e}")
        print(e)
        # Clean up on error
        if project_path.exists():
            shutil.rmtree(project_path)
        sys.exit(1)


@app.command()
def shell():
    """
    🐚 Open an interactive Python shell with the app loaded.

    Example:
        microframe shell
    """
    console.print(
        Panel.fit(
            "🐚 Starting Interactive Shell",
            border_style="cyan",
        )
    )

    try:
        # Try to import the app
        console.print("[cyan]→[/cyan] Loading application...")
        subprocess.run(
            "poetry run python -c 'from main import app; import code; code.interact(local=locals())'",
            shell=True,
        )
    except KeyboardInterrupt:
        console.print("\n[yellow]Shell closed[/yellow]")


@app.command()
def routes():
    """
    🗺️  Display all registered routes in the application.

    Example:
        microframe routes
    """
    console.print(
        Panel.fit(
            "🗺️ Application Routes",
            border_style="cyan",
        )
    )

    try:
        # Import the app and display routes
        code = """
from main import app
from rich.console import Console
from rich.table import Table

console = Console()
table = Table(title="Routes", border_style="green")
table.add_column("Path", style="cyan")
table.add_column("Methods", style="yellow")
table.add_column("Name", style="white")

for route in app.routes:
    methods = ", ".join(route.methods) if hasattr(route, 'methods') else "N/A"
    name = route.name if hasattr(route, 'name') else "N/A"
    table.add_row(route.path, methods, name)

console.print(table)
"""
        subprocess.run(f"poetry run python -c '{code}'", shell=True)
    except Exception as e:
        console.print(f"[red]✗[/red] Error loading routes: {e}")
        console.print("[yellow]→[/yellow] Make sure your application is properly configured")


@app.command()
def docs():
    """
    📚 Open API documentation in browser.

    Example:
        microframe docs
    """
    import webbrowser

    console.print(
        Panel.fit(
            "📚 Opening API Documentation",
            border_style="cyan",
        )
    )

    url = "http://localhost:8000/docs"
    console.print(f"[cyan]→[/cyan] Opening {url}")

    try:
        webbrowser.open(url)
        console.print("[green]✓[/green] Browser opened!")
    except Exception as e:
        console.print(f"[red]✗[/red] Could not open browser: {e}")
        console.print(f"[yellow]→[/yellow] Please visit: {url}")


@app.command()
def check_deps():
    """
    📦 Check for outdated dependencies.

    Example:
        microframe check-deps
    """
    console.print(
        Panel.fit(
            "📦 Checking Dependencies",
            border_style="blue",
        )
    )

    exit_code, stdout, _ = run_command(
        "poetry show --outdated",
        "Checking for outdated packages...",
        capture_output=True,
        show_spinner=False,
    )

    if exit_code == 0 and stdout:
        console.print(stdout)
        console.print("\n[yellow]→[/yellow] Run [cyan]poetry update[/cyan] to update packages")
    else:
        console.print("[green]✓[/green] All dependencies are up to date!")


@app.command()
def db_migrate(
    message: str = typer.Argument(..., help="Migration message"),
    autogenerate: bool = typer.Option(True, "--auto/--no-auto", help="Auto-generate migration"),
):
    """
    🗄️  Create a new database migration.

    Example:
        microframe db-migrate "Add user table"
        microframe db-migrate "Update schema" --no-auto
    """
    console.print(
        Panel.fit(
            "🗄️ Creating Database Migration",
            border_style="green",
        )
    )

    auto_flag = "--autogenerate" if autogenerate else ""
    command = f'poetry run alembic revision {auto_flag} -m "{message}"'

    exit_code, _, _ = run_command(command, "Creating migration...")

    if exit_code == 0:
        console.print("[green]✓[/green] Migration created!")
    else:
        console.print("[red]✗[/red] Migration failed!")
        sys.exit(exit_code)


@app.command()
def db_upgrade(
    revision: str = typer.Option("head", "--revision", "-r", help="Target revision"),
):
    """
    🗄️  Apply database migrations.

    Example:
        microframe db-upgrade
        microframe db-upgrade --revision +1
    """
    console.print(
        Panel.fit(
            "🗄️ Applying Database Migrations",
            border_style="green",
        )
    )

    command = f"poetry run alembic upgrade {revision}"

    exit_code, _, _ = run_command(command, "Applying migrations...")

    if exit_code == 0:
        console.print("[green]✓[/green] Migrations applied!")
    else:
        console.print("[red]✗[/red] Migration failed!")
        sys.exit(exit_code)


@app.command()
def db_downgrade(
    revision: str = typer.Option("-1", "--revision", "-r", help="Target revision"),
):
    """
    🗄️  Rollback database migrations.

    Example:
        microframe db-downgrade
        microframe db-downgrade --revision base
    """
    console.print(
        Panel.fit(
            "🗄️ Rolling Back Database Migrations",
            border_style="yellow",
        )
    )

    command = f"poetry run alembic downgrade {revision}"

    exit_code, _, _ = run_command(command, "Rolling back migrations...")

    if exit_code == 0:
        console.print("[green]✓[/green] Rollback complete!")
    else:
        console.print("[red]✗[/red] Rollback failed!")
        sys.exit(exit_code)


@app.command()
def info():
    """
    📊 Display project information and available commands.
    """
    console.print(
        Panel.fit(
            "[bold cyan]MicroFrame CLI[/bold cyan]\n" "ASGI Microframework Development Tools",
            border_style="cyan",
        )
    )

    # Project info
    info_table = Table(show_header=False, border_style="blue")
    info_table.add_column("Key", style="cyan")
    info_table.add_column("Value", style="white")

    info_table.add_row("Version", "2.0.0")
    info_table.add_row("Python", "^3.13")
    info_table.add_row("Framework", "Starlette + Pydantic")

    console.print(info_table)

    # Commands grouped by category
    console.print("\n[bold]📦 Project Management:[/bold]")
    for cmd, desc in [
        ("new", "Create new project from template"),
        ("info", "Show project information"),
    ]:
        console.print(f"  [cyan]{cmd:20}[/cyan] {desc}")

    console.print("\n[bold]🚀 Development:[/bold]")
    for cmd, desc in [
        ("run-dev", "Launch development server"),
        ("shell", "Open interactive Python shell"),
        ("routes", "Display all registered routes"),
        ("docs", "Open API documentation"),
    ]:
        console.print(f"  [cyan]{cmd:20}[/cyan] {desc}")

    console.print("\n[bold]🧪 Testing & Quality:[/bold]")
    for cmd, desc in [
        ("test", "Run tests with pytest"),
        ("lint-fix", "Fix code style issues"),
        ("lint-check", "Check code style"),
    ]:
        console.print(f"  [cyan]{cmd:20}[/cyan] {desc}")

    console.print("\n[bold]🗄️  Database:[/bold]")
    for cmd, desc in [
        ("db-migrate", "Create database migration"),
        ("db-upgrade", "Apply migrations"),
        ("db-downgrade", "Rollback migrations"),
    ]:
        console.print(f"  [cyan]{cmd:20}[/cyan] {desc}")

    console.print("\n[bold]🛠️  Utilities:[/bold]")
    for cmd, desc in [
        ("clean", "Clean generated files"),
        ("build", "Build the project"),
        ("check-deps", "Check outdated dependencies"),
    ]:
        console.print(f"  [cyan]{cmd:20}[/cyan] {desc}")

    console.print("\n[dim]Use --help with any command for more details[/dim]")


def main():
    """Entry point for the CLI."""
    app()


if __name__ == "__main__":
    main()
