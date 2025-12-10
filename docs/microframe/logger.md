# Advanced Logging System

Documentation for `microframe/utils/logger.py` - Comprehensive logging utilities.

## Overview

The `microframe/utils/logger.py` module provides a powerful and highly configurable logging system designed to offer detailed insights into the behavior and performance of your MicroFrame applications. It extends Python's standard `logging` module with advanced features like JSON formatting, log rotation, thread-local context, and specialized logging methods for various application aspects.

### Key Features

-   **Flexible Configuration**: Easily customize log level, format (JSON or plain text), and output destinations (console, file).
-   **Log Rotation**: Supports both size-based and time-based log file rotation.
-   **Structured Logging**: JSON formatting for easy parsing by log management systems.
-   **Sensitive Data Masking**: Automatically masks specified sensitive fields in JSON logs.
-   **Thread-Local Context**: Add contextual information (e.g., `request_id`, `user_id`) to all logs within a specific execution flow.
-   **Specialized Log Methods**: `CustomLogger` provides methods for logging HTTP requests, SQL queries, security events, and performance metrics.
-   **Execution Decorator**: Automatically logs function entry, exit, and duration, including error details.

## `LogConfig` Class

This class centralizes all logging-related settings.

```python
class LogConfig:
    def __init__(self):
        self.log_level = logging.INFO
        self.log_dir = Path("logs")
        self.log_format = "json"  # "json" or "text"
        self.enable_console = True
        self.enable_file = True
        self.max_file_size = 10 * 1024 * 1024  # 10MB
        self.backup_count = 5
        self.enable_rotation = True
        self.rotation_interval = "midnight"  # "H", "D", "W0"-"W6"
        self.enable_request_logging = True
        self.log_sql_queries = False
        self.sensitive_fields = ["password", "token", "secret", "api_key"]
```

You can customize these settings by passing a `LogConfig` instance to `setup_logging`.

## Logging Context

### `LogContext` (Thread-Local)

The `LogContext` class manages thread-local data, allowing you to attach contextual information (like a request ID, user ID, or session data) to all log messages generated within a specific thread's execution path.

```python
from microframe.utils.logger import log_context

# Set a value in the context
log_context.set("request_id", "xyz123")
logger.info("This log will include request_id")

# Get a value from the context
request_id = log_context.get("request_id")
```

### `logging_context(**kwargs)` (Context Manager)

This context manager provides a convenient way to temporarily add or override values in the logging context.

```python
from microframe.utils.logger import logging_context

with logging_context(user_id=123, transaction_id="tx_456"):
    logger.info("User action initiated")
    # All logs within this block will have user_id and transaction_id
    # When the block exits, the context is restored to its previous state.
```

## Custom Formatters

The module includes specialized formatters to control the output appearance of logs.

### `JSONFormatter`

Formats log records as JSON objects, making them ideal for machine parsing and integration with log aggregation systems (e.g., ELK stack, Splunk). It also includes sensitive data masking.

```json
{
  "timestamp": "2025-12-06T12:34:56.789000",
  "level": "INFO",
  "logger": "my_app",
  "message": "User logged in",
  "module": "auth_service",
  "function": "login_user",
  "line": 42,
  "context": {
    "user_id": 123,
    "request_id": "xyz123"
  },
  "extra_field_1": "value",
  "sensitive_data": "***MASKED***",
  "exception": { /* ... if an exception occurred */ }
}
```

### `ColoredFormatter`

Provides colored output for console logs, enhancing readability during development.

## `CustomLogger` Class

This extended `logging.Logger` class adds several convenient methods for logging specific types of events.

### `log_with_context(level: int, msg: str, **kwargs)`

Logs a message with additional key-value pairs that are directly added to the log record's `extra_fields` (useful for JSON output).

### `debug_dict(data: Dict, message: str = "")` / `info_dict(data: Dict, message: str = "")`

Logs a dictionary in a readable format (indented JSON string) at debug or info level.

### `request(method: str, path: str, status: int, duration: float, **kwargs)`

Logs details about an incoming HTTP request, including method, path, status code, and duration.

```python
logger.request("GET", "/api/users", 200, 0.05, user_agent="Mozilla/5.0")
```

### `query(sql: str, params: Optional[tuple] = None, duration: Optional[float] = None)`

Logs SQL queries (if `log_config.log_sql_queries` is `True`), along with parameters and execution duration.

```python
logger.query("SELECT * FROM users WHERE id = %s", (1,), 0.002)
```

### `security(event: str, **kwargs)`

Logs a security-related event, such as a failed login attempt or access to a restricted resource.

```python
logger.security("FailedLoginAttempt", username="bad_user", ip_address="192.168.1.1")
```

### `performance(operation: str, duration: float, **kwargs)`

Logs performance metrics for specific operations, useful for profiling and optimization.

```python
logger.performance("DatabaseFetch", 0.12, records_count=1000)
```

## `setup_logging(app_name: str = "microframework", config: Optional[LogConfig] = None) -> CustomLogger`

This function initializes the entire logging system based on the provided `LogConfig`. It creates log directories, sets up handlers (console, file), applies formatters, and returns the configured `CustomLogger` instance.

```python
from microframe.utils.logger import setup_logging, LogConfig, logging

# Basic setup
logger = setup_logging(app_name="my_micro_app")
logger.info("Logging system initialized!")

# Custom configuration
my_log_config = LogConfig()
my_log_config.log_level = logging.DEBUG
my_log_config.enable_file = False # Disable file logging
my_log_config.sensitive_fields.append("credit_card_number") # Add sensitive field

custom_logger = setup_logging(app_name="my_custom_app", config=my_log_config)
custom_logger.debug("Debug message, only to console")
```

## `log_execution(logger: Optional[logging.Logger] = None)` (Decorator)

A decorator to automatically log the execution flow of functions, including their start, completion, and any exceptions. It also records the execution duration.

```python
import asyncio
from microframe.utils.logger import log_execution, setup_logging

# Get a configured logger
my_logger = setup_logging(app_name="my_app_func_logger")

@log_execution(logger=my_logger) # Specify the logger to use
def synchronous_task(a: int, b: int):
    """A synchronous function."""
    return a + b

@log_execution(logger=my_logger)
async def asynchronous_task():
    """An asynchronous function."""
    await asyncio.sleep(0.01)
    return "Done"

# Example usage
result_sync = synchronous_task(10, 20) # Logs "Executing synchronous_task" and "Completed synchronous_task"
result_async = await asynchronous_task() # Logs "Executing asynchronous_task" and "Completed asynchronous_task"

@log_execution() # Uses default logger for the module
def failing_task():
    """A task that will raise an error."""
    raise ValueError("Something went wrong!")

try:
    failing_task() # Logs "Failed failing_task" with exception info
except ValueError:
    pass
```

---

## Best Practices

1.  **Centralize Configuration**: Use `LogConfig` and `setup_logging` to configure your logger once at application startup.
2.  **Structured Logging (JSON)**: For production environments, prefer JSON format (`log_format = "json"`) for easier parsing and analysis by log management tools.
3.  **Use Context**: Employ `logging_context` or `LogContext` directly to enrich your logs with relevant data for better debugging.
4.  **Specialized Methods**: Utilize `logger.request()`, `logger.query()`, `logger.security()`, and `logger.performance()` for specific event types.
5.  **Sensitive Data Masking**: Configure `log_config.sensitive_fields` to prevent sensitive information from appearing in your logs.
6.  **Decorate Critical Functions**: Use `@log_execution` on important functions to automatically track their performance and catch errors.
7.  **Do Not Propagate**: Ensure `logger.propagate = False` to prevent logs from being duplicated by parent loggers.

---

## 📖 Navigation

**Documentation Modules Core** :
- [Index Modules](README.md)
- [Application](application.md)
- [Config](config.md)
- [Router](router.md)
- [Dependencies](dependencies.md)
- [Validation](validation.md)
- [Middleware](middleware.md)
- [Exceptions](exceptions.md)
- [Templates](templates.md)
- [UI Components](ui.md)
- [Configurations](configurations.md)

---

**[↑ Index Principal](../README.md)** | **[📚 Guides Pratiques](../guides/getting-started.md)**