"""
Tests for Validation with Pydantic
"""

import pytest
from httpx import AsyncClient
from pydantic import BaseModel, Field, ValidationError

from microframe import Application


class TestValidation:
    """Test request validation with Pydantic"""

    @pytest.mark.asyncio
    async def test_valid_request_body(self):
        """Test valid JSON body validation"""
        app = Application()

        class Item(BaseModel):
            name: str
            price: float

        @app.post("/items")
        async def create_item(item: Item):
            return {"name": item.name, "price": item.price}

        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.post("/items", json={"name": "Book", "price": 9.99})
            assert response.status_code == 200
            data = response.json()
            assert data["name"] == "Book"
            assert data["price"] == 9.99

    @pytest.mark.asyncio
    async def test_invalid_request_body(self):
        """Test invalid JSON body returns 422"""
        app = Application()

        class Item(BaseModel):
            name: str
            price: float

        @app.post("/items")
        async def create_item(request, item: Item):

            return {"name": item.name, "price": item.price}

        async with AsyncClient(app=app, base_url="http://test") as client:
            # Missing required field
            response = await client.post("/items", json={"name": "Book"})
            assert response.status_code == 422

            # Wrong type
            response = await client.post("/items", json={"name": "Book", "price": "invalid"})
            assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_validation_with_constraints(self):
        """Test validation with field constraints"""
        app = Application()

        class User(BaseModel):
            username: str = Field(..., min_length=3, max_length=20)
            age: int = Field(..., ge=0, le=150)
            email: str

        @app.post("/users")
        async def create_user(user: User):
            return user.model_dump()

        async with AsyncClient(app=app, base_url="http://test") as client:
            # Valid user
            response = await client.post(
                "/users",
                json={"username": "john_doe", "age": 25, "email": "john@example.com"},
            )
            assert response.status_code == 200

            # Username too short
            response = await client.post(
                "/users", json={"username": "ab", "age": 25, "email": "john@example.com"}
            )
            assert response.status_code == 422

            # Age out of range
            response = await client.post(
                "/users", json={"username": "john", "age": 200, "email": "john@example.com"}
            )
            assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_nested_model_validation(self):
        """Test nested Pydantic models"""
        app = Application()

        class Address(BaseModel):
            street: str
            city: str
            zipcode: str

        class User(BaseModel):
            name: str
            address: Address

        @app.post("/users")
        async def create_user(user: User):
            return user.model_dump()

        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.post(
                "/users",
                json={
                    "name": "John",
                    "address": {"street": "123 Main St", "city": "NYC", "zipcode": "10001"},
                },
            )
            assert response.status_code == 200
            data = response.json()
            assert data["name"] == "John"
            assert data["address"]["city"] == "NYC"

    @pytest.mark.asyncio
    async def test_optional_fields(self):
        """Test optional fields in validation"""
        app = Application()

        class Item(BaseModel):
            name: str
            description: str | None = None
            price: float = 0.0

        @app.post("/items")
        async def create_item(item: Item):
            return item.model_dump()

        async with AsyncClient(app=app, base_url="http://test") as client:
            # Only required field
            response = await client.post("/items", json={"name": "Book"})
            assert response.status_code == 200
            data = response.json()
            assert data["name"] == "Book"
            assert data["description"] is None
            assert data["price"] == 0.0

            # All fields
            response = await client.post(
                "/items", json={"name": "Book", "description": "A good book", "price": 19.99}
            )
            assert response.status_code == 200
            data = response.json()
            assert data["description"] == "A good book"

    @pytest.mark.asyncio
    async def test_list_validation(self):
        """Test validation of list fields"""
        app = Application()

        class ItemList(BaseModel):
            items: list[str]
            quantities: list[int]

        @app.post("/batch")
        async def create_batch(batch: ItemList):
            return batch.model_dump()

        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.post(
                "/batch",
                json={"items": ["item1", "item2"], "quantities": [10, 20]},
            )
            assert response.status_code == 200
            data = response.json()
            assert len(data["items"]) == 2
            assert len(data["quantities"]) == 2
