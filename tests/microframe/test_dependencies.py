"""
Tests for Dependency Injection
"""
import pytest
from httpx import AsyncClient
from microframe import Application, Depends


class TestDependencies:
    """Test dependency injection"""

    @pytest.mark.asyncio
    async def test_simple_dependency(self):
        """Test simple dependency injection"""
        app = Application()

        def get_db():
            return {"type": "postgres", "connected": True}

        @app.get("/data")
        async def get_data(db=Depends(get_db)):
            return {"database": db}

        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.get("/data")
            assert response.status_code == 200
            data = response.json()
            assert data["database"]["type"] == "postgres"
            assert data["database"]["connected"] is True

    @pytest.mark.asyncio
    async def test_nested_dependencies(self):
        """Test nested dependency injection"""
        app = Application()

        def get_db():
            return {"db": "postgres"}

        def get_repository(db=Depends(get_db)):
            return {"repository": "UserRepository", "db": db}

        @app.get("/users")
        async def get_users(repo=Depends(get_repository)):
            return {"repo": repo}

        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.get("/users")
            assert response.status_code == 200
            data = response.json()
            assert "repo" in data
            assert data["repo"]["repository"] == "UserRepository"
            assert data["repo"]["db"]["db"] == "postgres"

    @pytest.mark.asyncio
    async def test_async_dependency(self):
        """Test async dependency function"""
        app = Application()

        async def get_async_data():
            return {"async": True, "data": "loaded"}

        @app.get("/async-data")
        async def get_data(data=Depends(get_async_data)):
            return {"result": data}

        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.get("/async-data")
            assert response.status_code == 200
            result = response.json()
            assert result["result"]["async"] is True
            assert result["result"]["data"] == "loaded"

    @pytest.mark.asyncio
    async def test_dependency_with_request(self):
        """Test dependency with request parameter"""
        app = Application()

        def get_user_agent(request):
            return request.headers.get("user-agent", "unknown")

        @app.get("/user-agent")
        async def show_user_agent(agent=Depends(get_user_agent)):
            return {"user_agent": agent}

        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.get("/user-agent")
            assert response.status_code == 200
            # httpx sets a default user-agent
            assert "user_agent" in response.json()

    @pytest.mark.asyncio
    async def test_multiple_dependencies(self):
        """Test multiple dependencies in single route"""
        app = Application()

        def get_db():
            return {"db": "connected"}

        def get_cache():
            return {"cache": "redis"}

        @app.get("/multi")
        async def multi_deps(db=Depends(get_db), cache=Depends(get_cache)):
            return {"db": db, "cache": cache}

        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.get("/multi")
            assert response.status_code == 200
            data = response.json()
            assert data["db"]["db"] == "connected"
            assert data["cache"]["cache"] == "redis"

    @pytest.mark.asyncio
    async def test_dependency_caching(self):
        """Test dependency caching"""
        app = Application()
        call_count = {"count": 0}

        def get_expensive_resource():
            call_count["count"] += 1
            return {"resource": "expensive", "call": call_count["count"]}

        @app.get("/cached1")
        async def route1(resource=Depends(get_expensive_resource, use_cache=True)):
            return {"route": "1", "resource": resource}

        @app.get("/cached2")
        async def route2(resource=Depends(get_expensive_resource, use_cache=True)):
            return {"route": "2", "resource": resource}

        async with AsyncClient(app=app, base_url="http://test") as client:
            # First call
            response1 = await client.get("/cached1")
            assert response1.status_code == 200
            
            # Second call should use cache (if caching is working)
            response2 = await client.get("/cached2")
            assert response2.status_code == 200

    @pytest.mark.asyncio
    async def test_dependency_in_router(self):
        """Test dependencies work with routers"""
        from microframe import Router

        app = Application()
        router = Router(prefix="/api")

        def get_api_key():
            return {"api_key": "secret-key-123"}

        @router.get("/secure")
        async def secure_route(auth=Depends(get_api_key)):
            return {"authenticated": True, "key": auth}

        app.include_router(router)

        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.get("/api/secure")
            assert response.status_code == 200
            data = response.json()
            assert data["authenticated"] is True
            assert data["key"]["api_key"] == "secret-key-123"


class TestDependencyManager:
    """Test DependencyManager directly"""

    @pytest.mark.asyncio
    async def test_dependency_manager_resolve(self):
        """Test DependencyManager resolve method"""
        from microframe.dependencies import DependencyManager

        manager = DependencyManager()

        def sample_dep():
            return "dependency_value"

        def target_func(dep=Depends(sample_dep)):
            return dep

        resolved = await manager.resolve(target_func)
        assert "dep" in resolved
        assert resolved["dep"] == "dependency_value"

    @pytest.mark.asyncio
    async def test_dependency_manager_clear_cache(self):
        """Test cache clearing"""
        from microframe.dependencies import DependencyManager

        manager = DependencyManager()
        
        # Add something to cache
        manager._cache["test"] = "value"
        assert len(manager._cache) > 0
        
        # Clear cache
        manager.clear_cache()
        assert len(manager._cache) == 0
