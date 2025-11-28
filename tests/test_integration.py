"""
Integration tests for complete application flows
"""

import pytest
from httpx import AsyncClient
from pydantic import BaseModel

from microframe import AppConfig, Application, Depends, Router
from microframe.exceptions.exception import (
    BadRequestException,
    ForbiddenException,
    NotFoundException,
    UnauthorizedException,
)
from microframe.middleware import CORSMiddleware


class TestIntegration:
    """End-to-end integration tests"""

    @pytest.mark.asyncio
    async def test_full_crud_api(self):
        """Test complete CRUD API flow"""
        from pydantic import BaseModel

        from microframe import AppConfig, Application

        app = Application()

        app = Application(AppConfig(title="Todo API", version="1.0.0"))

        # In-memory storage
        todos = {}
        next_id = 1

        class Get_Todo(BaseModel):
            id: int

        class Todo(BaseModel):
            title: str
            completed: bool = False

        class TodoResponse(BaseModel):
            id: int
            title: str
            completed: bool

        @app.get("/todos")
        async def list_todos():
            return todos

        @app.post("/todos")
        async def create_todo(todo: Todo):
            nonlocal next_id

            todo_dict = {"id": next_id, **todo.model_dump()}
            todos[next_id] = todo_dict
            next_id += 1
            return todo_dict

        @app.get("/todos/{todo_id}")
        async def get_todo(
            todo_id: int,
        ):
            for _, value in todos.items():
                for k, v in value.items():
                    if k == "id" and v == int(todo_id):
                        return value

            raise NotFoundException(f"Todo {todo_id} not found")

        @app.put("/todos/{todo_id}")
        async def update_todo(todo_id: int, todo: Todo):
            for _, value in todos.items():
                for k, v in value.items():
                    if k == "id" and v == int(todo_id):
                        todos[todo_id] = {"id": todo_id, **todo.model_dump()}
                        return todos[todo_id]

            raise NotFoundException(f"Todo {todo_id} not found")

        @app.delete("/todos/{todo_id}")
        async def delete_todo(todo_id: int):

            for key, value in todos.items():
                for k, v in value.items():
                    if k == "id" and v == int(todo_id):
                        del todos[key]
                        return {"message": "deleted"}
            raise NotFoundException(f"Todo {todo_id} not found")

        async with AsyncClient(app=app, base_url="http://test") as client:
            # CREATE
            response = await client.post(
                "/todos", json={"title": "Buy groceries", "completed": False}
            )
            assert response.status_code == 200
            todo1 = response.json()
            assert todo1["id"] == 1
            assert todo1["title"] == "Buy groceries"

            # CREATE another
            response = await client.post("/todos", json={"title": "Write code", "completed": True})
            assert response.status_code == 200
            todo2 = response.json()
            assert todo2["id"] == 2

            # LIST
            response = await client.get("/todos")
            assert response.status_code == 200
            data = response.json()
            assert len(data) == 2

            # GET
            response = await client.get("/todos/1")
            assert response.status_code == 200
            assert response.json()["title"] == "Buy groceries"

            # UPDATE
            response = await client.put(
                "/todos/1", json={"title": "Buy groceries", "completed": True}
            )
            assert response.status_code == 200
            assert response.json()["completed"] is True

            # DELETE
            response = await client.delete("/todos/1")
            assert response.status_code == 200

            # GET deleted (should 404)
            response = await client.get("/todos/1")
            assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_nested_routers_with_dependencies(self):
        """Test complex app with nested routers and dependencies"""
        app = Application()

        # Database dependency
        def get_db():
            return {"type": "postgres", "connected": True}

        # API v1 router
        v1_router = Router(prefix="/api/v1", tags=["v1"])

        # Users sub-router
        users_router = Router(prefix="/users", tags=["Users"])

        @users_router.get("/")
        async def list_users(db=Depends(get_db)):
            return {"users": [], "db": db["type"]}

        @users_router.get("/{user_id}")
        async def get_user(user_id: str, db=Depends(get_db)):
            return {"user_id": user_id, "db": db["type"]}

        # Posts sub-router
        posts_router = Router(prefix="/posts", tags=["Posts"])

        @posts_router.get("/")
        async def list_posts(db=Depends(get_db)):
            return {"posts": [], "db": db["type"]}

        # Include routers
        v1_router.include_router(users_router)
        v1_router.include_router(posts_router)
        app.include_router(v1_router)

        async with AsyncClient(app=app, base_url="http://test") as client:
            # Test users
            response = await client.get("/api/v1/users/")
            assert response.status_code == 200
            data = response.json()
            assert data["db"] == "postgres"

            response = await client.get("/api/v1/users/123")
            assert response.status_code == 200
            assert response.json()["user_id"] == "123"

            # Test posts
            response = await client.get("/api/v1/posts/")
            assert response.status_code == 200
            assert response.json()["db"] == "postgres"

    @pytest.mark.asyncio
    async def test_app_with_middleware_and_validation(self):
        """Test app with CORS middleware and validation"""
        app = Application()

        app.add_middleware(
            CORSMiddleware,
            allow_origins=["http://localhost:3000"],
            allow_methods=["GET", "POST"],
        )

        class UserCreate(BaseModel):
            username: str
            email: str
            age: int

        @app.post("/users")
        async def create_user(user: UserCreate):
            return user.model_dump()

        async with AsyncClient(app=app, base_url="http://test") as client:
            # Valid request
            response = await client.post(
                "/users",
                json={"username": "john", "email": "john@example.com", "age": 25},
                headers={"Origin": "http://localhost:3000"},
            )
            assert response.status_code == 200
            # CORS headers should be present
            assert "access-control-allow-origin" in response.headers

            # Invalid request (validation error)
            response = await client.post(
                "/users",
                json={"username": "john"},  # Missing required fields
            )
            assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_openapi_docs_generation(self):
        """Test that OpenAPI docs are generated"""
        app = Application(
            AppConfig(
                title="Test API",
                version="1.0.0",
                description="Test Description",
            )
        )

        @app.get("/items", tags=["Items"], summary="List items")
        async def list_items():
            """Get all items from the database"""
            return {"items": []}

        async with AsyncClient(app=app, base_url="http://test") as client:
            # OpenAPI schema
            response = await client.get("/openapi.json")
            assert response.status_code == 200
            schema = response.json()
            assert schema["info"]["title"] == "Test API"
            assert schema["info"]["version"] == "1.0.0"

            # Swagger UI
            response = await client.get("/docs")
            assert response.status_code == 200
            assert "swagger" in response.text.lower() or "html" in response.text.lower()

            # ReDoc UI
            response = await client.get("/redoc")
            assert response.status_code == 200
            assert "redoc" in response.text.lower() or "html" in response.text.lower()


class TestAdvancedIntegration:
    """Advanced integration tests for complex scenarios"""

    @pytest.mark.asyncio
    async def test_custom_headers_and_cookies(self):
        """Test custom headers and cookie handling"""
        app = Application()

        @app.get("/headers")
        async def read_headers(request):
            """Echo back custom headers"""
            custom_header = request.headers.get("x-custom-header", "not-found")
            user_agent = request.headers.get("user-agent", "unknown")

            return {
                "custom_header": custom_header,
                "user_agent": user_agent,
            }

        @app.post("/set-cookie")
        async def set_cookie():
            """Set a cookie in response"""
            from starlette.responses import JSONResponse

            response = JSONResponse({"message": "Cookie set"})
            response.set_cookie(key="session_id", value="abc123xyz", max_age=3600, httponly=True)
            return response

        @app.get("/read-cookie")
        async def read_cookie(request):
            """Read cookie from request"""
            session_id = request.cookies.get("session_id", "no-cookie")
            return {"session_id": session_id}

        async with AsyncClient(app=app, base_url="http://test") as client:
            # Test custom headers
            response = await client.get("/headers", headers={"X-Custom-Header": "test-value-123"})
            assert response.status_code == 200
            data = response.json()
            assert data["custom_header"] == "test-value-123"

            # Set cookie
            response = await client.post("/set-cookie")
            assert response.status_code == 200
            assert "session_id" in response.cookies

            # Read cookie
            response = await client.get("/read-cookie", cookies={"session_id": "test-session-456"})
            assert response.status_code == 200
            assert response.json()["session_id"] == "test-session-456"

    @pytest.mark.asyncio
    async def test_error_handling_integration(self):
        """Test comprehensive error handling across the application"""
        app = Application()

        @app.get("/error/404")
        async def not_found_error():
            from microframe.exceptions.exception import NotFoundException

            raise NotFoundException("Resource not found")

        @app.get("/error/401")
        async def unauthorized_error():
            from microframe.exceptions.exception import UnauthorizedException

            raise UnauthorizedException("Unauthorized access")

        @app.get("/error/403")
        async def forbidden_error():
            from microframe.exceptions.exception import ForbiddenException

            raise ForbiddenException("Forbidden")

        @app.get("/error/400")
        async def bad_request_error():
            from microframe.exceptions.exception import BadRequestException

            raise BadRequestException("Bad request")

        @app.get("/error/500")
        async def server_error():
            raise ValueError("Internal server error")

        @app.post("/validate")
        async def validate_data(data: BaseModel):
            return {"validated": True}

        async with AsyncClient(app=app, base_url="http://test") as client:
            # Test all error types
            response = await client.get("/error/404")
            assert response.status_code == 404

            response = await client.get("/error/401")
            assert response.status_code == 401

            response = await client.get("/error/403")
            assert response.status_code == 403

            response = await client.get("/error/400")
            assert response.status_code == 400

            response = await client.get("/error/500")
            assert response.status_code == 500

    @pytest.mark.asyncio
    async def test_content_types_and_responses(self):
        """Test different content types and response formats"""
        app = Application()

        @app.get("/json")
        async def get_json():
            return {"format": "json", "data": [1, 2, 3]}

        @app.get("/text")
        async def get_text():
            from starlette.responses import PlainTextResponse

            return PlainTextResponse("Plain text response")

        @app.get("/html")
        async def get_html():
            from starlette.responses import HTMLResponse

            return HTMLResponse("<h1>HTML Response</h1><p>Test content</p>")

        @app.post("/form")
        async def handle_form(request):
            """Handle form data"""
            form_data = await request.form()
            return {
                "received": dict(form_data),
                "content_type": request.headers.get("content-type"),
            }

        async with AsyncClient(app=app, base_url="http://test") as client:
            # JSON response
            response = await client.get("/json")
            assert response.status_code == 200
            assert response.headers["content-type"].startswith("application/json")
            assert response.json()["format"] == "json"

            # Plain text response
            response = await client.get("/text")
            assert response.status_code == 200
            assert "text/plain" in response.headers["content-type"]
            assert response.text == "Plain text response"

            # HTML response
            response = await client.get("/html")
            assert response.status_code == 200
            assert "text/html" in response.headers["content-type"]
            assert "<h1>" in response.text

            # Form data
            response = await client.post(
                "/form", data={"username": "john", "email": "john@example.com"}
            )
            assert response.status_code == 200
            data = response.json()
            assert data["received"]["username"] == "john"

    @pytest.mark.asyncio
    async def test_versioned_api_workflow(self):
        """Test API versioning with different router versions"""
        app = Application()

        # API v1
        v1_router = Router(prefix="/api/v1", tags=["v1"])

        @v1_router.get("/data")
        async def get_data_v1():
            return {"version": "1.0", "data": {"format": "old"}, "deprecated": True}

        # API v2
        v2_router = Router(prefix="/api/v2", tags=["v2"])

        @v2_router.get("/data")
        async def get_data_v2():
            return {
                "version": "2.0",
                "data": {
                    "format": "new",
                    "enhanced": True,
                    "features": ["pagination", "filtering"],
                },
                "deprecated": False,
            }

        class DataQuery(BaseModel):
            limit: int = 10
            offset: int = 0

        @v2_router.post("/data/query")
        async def query_data_v2(query: DataQuery):
            return {
                "version": "2.0",
                "results": list(range(query.offset, query.offset + query.limit)),
                "limit": query.limit,
                "offset": query.offset,
            }

        app.include_router(v1_router)
        app.include_router(v2_router)

        async with AsyncClient(app=app, base_url="http://test") as client:
            # Access v1 API
            response = await client.get("/api/v1/data")
            assert response.status_code == 200
            data = response.json()
            assert data["version"] == "1.0"
            assert data["deprecated"] is True

            # Access v2 API
            response = await client.get("/api/v2/data")
            assert response.status_code == 200
            data = response.json()
            assert data["version"] == "2.0"
            assert data["deprecated"] is False
            assert "enhanced" in data["data"]

            # Use v2 advanced features
            response = await client.post("/api/v2/data/query", json={"limit": 5, "offset": 10})
            assert response.status_code == 200
            data = response.json()
            assert len(data["results"]) == 5
            assert data["results"][0] == 10
