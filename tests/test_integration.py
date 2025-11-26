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
        app.include_router(v1_router, prefix="/api/v1")

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
    async def test_authentication_workflow(self):
        """Test complete authentication flow with token-based auth"""
        from authx import AuthConfig, create_access_token, decode_token

        authx_ = AuthConfig(
            secret_key="votre-cle-secrete-min-32-caracteres",
        )

        app = Application()

        # Mock user database
        users_db = {
            "admin": {"password": "admin123", "role": "admin"},
            "user": {"password": "user123", "role": "user"},
        }

        # Mock token storage
        tokens = {}

        class LoginRequest(BaseModel):
            username: str
            password: str

        class TokenResponse(BaseModel):
            access_token: str
            token_type: str = "bearer"

        def verify_token(request):
            """Dependency to verify authentication token"""
            auth_header = request.headers.get("authorization", "")
            if not auth_header.startswith("Bearer "):
                from microframe.exceptions.exception import UnauthorizedException

                raise UnauthorizedException("Invalid authentication")
            return decode_token(auth_header[7:], authx_, "access")

        @app.post("/auth/login")
        async def login(credentials: LoginRequest):
            """Login endpoint"""
            user = users_db.get(credentials.username)
            if not user or user["password"] != credentials.password:
                from microframe.exceptions.exception import UnauthorizedException

                raise UnauthorizedException("Invalid credentials")

            # Generate simple token (in real app, use JWT)
            token = create_access_token(credentials.username, authx_)

            return {"access_token": token, "token_type": "bearer"}

        @app.get("/auth/me")
        async def get_current_user(user=Depends(verify_token)):
            """Get current authenticated user"""
            return {"user": user}

        @app.get("/admin/dashboard")
        async def admin_dashboard(user=Depends(verify_token)):
            """Admin-only endpoint"""
            if user["sub"] != "admin":
                from microframe.exceptions.exception import ForbiddenException

                raise ForbiddenException("Admin access required")
            return {"dashboard": "admin data", "user": user["sub"]}

        async with AsyncClient(app=app, base_url="http://test") as client:
            # Try accessing protected endpoint without auth (should fail)
            response = await client.get("/auth/me")
            assert response.status_code == 401

            # Login with wrong credentials (should fail)
            response = await client.post(
                "/auth/login", json={"username": "admin", "password": "wrong"}
            )
            assert response.status_code == 401

            # Login with correct credentials
            response = await client.post(
                "/auth/login", json={"username": "admin", "password": "admin123"}
            )
            assert response.status_code == 200
            token_data = response.json()
            assert "access_token" in token_data
            token = token_data["access_token"]

            # Access protected endpoint with token
            response = await client.get("/auth/me", headers={"Authorization": f"Bearer {token}"})
            assert response.status_code == 200
            user_data = response.json()
            assert user_data["user"]["username"] == "admin"
            assert user_data["user"]["role"] == "admin"

            # Access admin endpoint as admin
            response = await client.get(
                "/admin/dashboard", headers={"Authorization": f"Bearer {token}"}
            )
            assert response.status_code == 200

            # Login as regular user
            response = await client.post(
                "/auth/login", json={"username": "user", "password": "user123"}
            )
            assert response.status_code == 200
            user_token = response.json()["access_token"]

            # Try to access admin endpoint as regular user (should fail)
            response = await client.get(
                "/admin/dashboard", headers={"Authorization": f"Bearer {user_token}"}
            )
            assert response.status_code == 403

    @pytest.mark.asyncio
    async def test_query_parameters_and_filtering(self):
        """Test query parameters for filtering and pagination"""
        app = Application()

        # Mock products database
        products = [
            {"id": 1, "name": "Laptop", "category": "electronics", "price": 999.99},
            {"id": 2, "name": "Mouse", "category": "electronics", "price": 29.99},
            {"id": 3, "name": "Desk", "category": "furniture", "price": 299.99},
            {"id": 4, "name": "Chair", "category": "furniture", "price": 199.99},
            {"id": 5, "name": "Monitor", "category": "electronics", "price": 399.99},
        ]

        @app.get("/products")
        async def list_products(request):
            """List products with filtering and pagination"""
            # Get query parameters
            category = request.query_params.get("category")
            min_price = request.query_params.get("min_price", type=float)
            max_price = request.query_params.get("max_price", type=float)
            page = int(request.query_params.get("page", "1"))
            limit = int(request.query_params.get("limit", "10"))

            # Filter products
            filtered = products.copy()

            if category:
                filtered = [p for p in filtered if p["category"] == category]

            if min_price:
                filtered = [p for p in filtered if p["price"] >= float(min_price)]

            if max_price:
                filtered = [p for p in filtered if p["price"] <= float(max_price)]

            # Paginate
            start = (page - 1) * limit
            end = start + limit
            paginated = filtered[start:end]

            return {
                "products": paginated,
                "total": len(filtered),
                "page": page,
                "limit": limit,
            }

        async with AsyncClient(app=app, base_url="http://test") as client:
            # Get all products
            response = await client.get("/products")
            assert response.status_code == 200
            data = response.json()
            assert len(data["products"]) == 5
            assert data["total"] == 5

            # Filter by category
            response = await client.get("/products?category=electronics")
            assert response.status_code == 200
            data = response.json()
            assert len(data["products"]) == 3
            assert all(p["category"] == "electronics" for p in data["products"])

            # Filter by price range
            response = await client.get("/products?min_price=100&max_price=500")
            assert response.status_code == 200
            data = response.json()
            assert len(data["products"]) == 3

            # Pagination
            response = await client.get("/products?page=1&limit=2")
            assert response.status_code == 200
            data = response.json()
            assert len(data["products"]) == 2
            assert data["page"] == 1

            # Combined filters
            response = await client.get("/products?category=electronics&min_price=100&limit=2")
            assert response.status_code == 200
            data = response.json()
            assert len(data["products"]) == 2
            assert all(p["category"] == "electronics" for p in data["products"])

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
    async def test_complex_multi_step_workflow(self):
        """Test a complex multi-step business workflow"""
        app = Application()

        # Simulated database
        users = {}
        orders = {}
        next_order_id = 1

        class UserRegister(BaseModel):
            username: str
            email: str
            password: str

        class OrderCreate(BaseModel):
            product_id: int
            quantity: int

        class OrderUpdate(BaseModel):
            status: str  # pending, processing, shipped, delivered

        @app.post("/users/register")
        async def register_user(user: UserRegister):
            """Step 1: Register a new user"""
            if user.username in users:
                from microframe.exceptions.exception import BadRequestException

                raise BadRequestException("Username already exists")

            users[user.username] = {"email": user.email, "password": user.password, "orders": []}
            return {"username": user.username, "email": user.email}

        @app.post("/users/{username}/orders")
        async def create_order(username: str, order: OrderCreate):
            """Step 2: Create order for user"""
            if username not in users:
                from microframe.exceptions.exception import NotFoundException

                raise NotFoundException("User not found")

            nonlocal next_order_id
            order_id = next_order_id
            next_order_id += 1

            order_data = {
                "id": order_id,
                "username": username,
                "product_id": order.product_id,
                "quantity": order.quantity,
                "status": "pending",
                "total": order.quantity * 100,  # Mock price
            }

            orders[order_id] = order_data
            users[username]["orders"].append(order_id)

            return order_data

        @app.get("/users/{username}/orders")
        async def get_user_orders(username: str):
            """Step 3: Get all orders for user"""
            if username not in users:
                from microframe.exceptions.exception import NotFoundException

                raise NotFoundException("User not found")

            user_order_ids = users[username]["orders"]
            user_orders = [orders[oid] for oid in user_order_ids if oid in orders]

            return {"orders": user_orders}

        @app.patch("/orders/{order_id}")
        async def update_order_status(order_id: int, update: OrderUpdate):
            """Step 4: Update order status"""
            if order_id not in orders:
                from microframe.exceptions.exception import NotFoundException

                raise NotFoundException("Order not found")

            valid_statuses = ["pending", "processing", "shipped", "delivered", "cancelled"]
            if update.status not in valid_statuses:
                from microframe.exceptions.exception import BadRequestException

                raise BadRequestException(f"Invalid status. Must be one of {valid_statuses}")

            orders[order_id]["status"] = update.status
            return orders[order_id]

        @app.get("/orders/{order_id}")
        async def get_order(order_id: int):
            """Get order details"""
            if order_id not in orders:
                from microframe.exceptions.exception import NotFoundException

                raise NotFoundException("Order not found")
            return orders[order_id]

        async with AsyncClient(app=app, base_url="http://test") as client:
            # Complete workflow test

            # Step 1: Register user
            response = await client.post(
                "/users/register",
                json={"username": "alice", "email": "alice@example.com", "password": "secret123"},
            )
            assert response.status_code == 200
            assert response.json()["username"] == "alice"

            # Step 2: Create first order
            response = await client.post(
                "/users/alice/orders", json={"product_id": 101, "quantity": 2}
            )
            assert response.status_code == 200
            order1 = response.json()
            assert order1["status"] == "pending"
            assert order1["quantity"] == 2
            order1_id = order1["id"]

            # Step 3: Create second order
            response = await client.post(
                "/users/alice/orders", json={"product_id": 102, "quantity": 5}
            )
            assert response.status_code == 200
            order2_id = response.json()["id"]

            # Step 4: Get all user orders
            response = await client.get("/users/alice/orders")
            assert response.status_code == 200
            user_orders = response.json()["orders"]
            assert len(user_orders) == 2

            # Step 5: Update order status to processing
            response = await client.patch(f"/orders/{order1_id}", json={"status": "processing"})
            assert response.status_code == 200
            assert response.json()["status"] == "processing"

            # Step 6: Update to shipped
            response = await client.patch(f"/orders/{order1_id}", json={"status": "shipped"})
            assert response.status_code == 200

            # Step 7: Update to delivered
            response = await client.patch(f"/orders/{order1_id}", json={"status": "delivered"})
            assert response.status_code == 200

            # Step 8: Verify final order status
            response = await client.get(f"/orders/{order1_id}")
            assert response.status_code == 200
            assert response.json()["status"] == "delivered"

            # Test error: Try invalid status
            response = await client.patch(f"/orders/{order1_id}", json={"status": "invalid-status"})
            assert response.status_code == 400

            # Test error: Try to register duplicate user
            response = await client.post(
                "/users/register",
                json={"username": "alice", "email": "alice2@example.com", "password": "secret456"},
            )
            assert response.status_code == 400

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
    async def test_batch_operations(self):
        """Test batch operations and bulk processing"""
        app = Application()

        items_db = {}
        next_id = 1

        class Item(BaseModel):
            name: str
            value: int

        class BulkCreateRequest(BaseModel):
            items: list[Item]

        @app.post("/items/bulk")
        async def bulk_create(request: BulkCreateRequest):
            """Create multiple items at once"""
            nonlocal next_id
            created = []

            for item in request.items:
                item_data = {"id": next_id, "name": item.name, "value": item.value}
                items_db[next_id] = item_data
                created.append(item_data)
                next_id += 1

            return {"created": len(created), "items": created}

        @app.delete("/items/bulk")
        async def bulk_delete(request):
            """Delete multiple items by IDs"""
            body = await request.json()
            ids = body.get("ids", [])
            deleted = []

            for item_id in ids:
                if item_id in items_db:
                    deleted.append(items_db.pop(item_id))

            return {"deleted": len(deleted), "items": deleted}

        @app.patch("/items/bulk")
        async def bulk_update(request):
            """Update multiple items"""
            body = await request.json()
            updates = body.get("updates", [])
            updated = []

            for update in updates:
                item_id = update.get("id")
                if item_id in items_db:
                    items_db[item_id].update(update.get("changes", {}))
                    updated.append(items_db[item_id])

            return {"updated": len(updated), "items": updated}

        async with AsyncClient(app=app, base_url="http://test") as client:
            # Bulk create
            response = await client.post(
                "/items/bulk",
                json={
                    "items": [
                        {"name": "Item 1", "value": 100},
                        {"name": "Item 2", "value": 200},
                        {"name": "Item 3", "value": 300},
                    ]
                },
            )
            assert response.status_code == 200
            result = response.json()
            assert result["created"] == 3
            assert len(result["items"]) == 3

            # Bulk update
            response = await client.patch(
                "/items/bulk",
                json={
                    "updates": [
                        {"id": 1, "changes": {"value": 150}},
                        {"id": 2, "changes": {"value": 250}},
                    ]
                },
            )
            assert response.status_code == 200
            assert response.json()["updated"] == 2

            # Bulk delete
            response = await client.delete("/items/bulk", params={"ids": [1, 3]})
            assert response.status_code == 200
            assert response.json()["deleted"] == 2

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

    @pytest.mark.asyncio
    async def test_dependency_scopes_and_caching(self):
        """Test dependency injection scopes and caching behavior"""
        app = Application()

        # Counter to track dependency calls
        call_counts = {"uncached": 0, "cached": 0}

        def uncached_dependency():
            """Called on every request"""
            call_counts["uncached"] += 1
            return {"count": call_counts["uncached"], "cached": False}

        def cached_dependency():
            """Cached dependency"""
            call_counts["cached"] += 1
            return {"count": call_counts["cached"], "cached": True}

        @app.get("/uncached")
        async def test_uncached(dep=Depends(uncached_dependency)):
            return {"dependency": dep}

        @app.get("/cached")
        async def test_cached(dep=Depends(cached_dependency, use_cache=True)):
            return {"dependency": dep}

        @app.get("/multiple-deps")
        async def test_multiple(
            dep1=Depends(uncached_dependency),
            dep2=Depends(uncached_dependency),
        ):
            """Same uncached dependency used twice"""
            return {"dep1": dep1, "dep2": dep2}

        async with AsyncClient(app=app, base_url="http://test") as client:
            # Reset counters
            call_counts["uncached"] = 0
            call_counts["cached"] = 0

            # Call uncached endpoint multiple times
            for i in range(3):
                response = await client.get("/uncached")
                assert response.status_code == 200
                data = response.json()
                assert data["dependency"]["count"] == i + 1
                assert data["dependency"]["cached"] is False

            # Multiple uncached dependencies in single request
            response = await client.get("/multiple-deps")
            assert response.status_code == 200
            data = response.json()
            # Each dependency call increments the counter
            assert data["dep1"]["count"] != data["dep2"]["count"]
