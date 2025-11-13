"""
Example application using the new modular architecture
"""

from pydantic import BaseModel, Field

from microframe import Application, Depends, Router
from microframe.middleware import CORSMiddleware, SecurityMiddleware

# =====================================================
# Models
# =====================================================


class User(BaseModel):
    """User model"""

    name: str = Field(..., min_length=2, max_length=50)
    email: str
    age: int = Field(..., ge=0, le=150)


class Item(BaseModel):
    """Item model"""

    title: str
    description: str = None
    price: float = Field(..., gt=0)


# =====================================================
# Dependencies
# =====================================================


def get_database():
    """Simulate database connection"""
    return {"type": "postgres", "connected": True}


def get_current_user():
    """Get current authenticated user"""
    return User(name="John Doe", email="john@example.com", age=30)


# =====================================================
# Routers
# =====================================================

# Users router
users_router = Router(prefix="/users", tags=["Users"])


@users_router.get("/")
async def list_users(db=Depends(get_database)):
    """List all users"""
    return {"users": [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}], "database": db}


@users_router.get("/{user_id}")
async def get_user(user_id: str):
    """Get user by ID"""
    return {"user_id": user_id, "name": "Alice"}


@users_router.post("/")
async def create_user(user: User):
    """Create a new user"""
    return {"message": "User created", "user": user}


# Items router
items_router = Router(prefix="/items", tags=["Items"])


@items_router.get("/")
async def list_items():
    """List all items"""
    return {
        "items": [
            {"id": 1, "title": "Item 1", "price": 10.99},
            {"id": 2, "title": "Item 2", "price": 20.99},
        ]
    }


@items_router.post("/")
async def create_item(item: Item):
    """Create a new item"""
    return {"message": "Item created", "item": item}


# Admin router (nested)
admin_router = Router(prefix="/admin", tags=["Admin"])


@admin_router.get("/stats")
async def get_stats(current_user=Depends(get_current_user)):
    """Get admin statistics"""
    return {"total_users": 100, "total_items": 250, "admin": current_user}


# =====================================================
# Application
# =====================================================

app = Application(
    title="Example API",
    version="2.0.0",
    description="Example application using the new modular architecture",
    debug=True,
)

# Add middlewares
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

app.add_middleware(SecurityMiddleware, rate_limit_requests=100, rate_limit_window=60)

# Include routers
api_router = Router(prefix="/api/v1", tags=["API v1"])
api_router.include_router(users_router)
api_router.include_router(items_router)
api_router.include_router(admin_router)

app.include_router(api_router)

# Direct routes


@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "Welcome to the API", "version": "2.0.0", "docs": "/docs"}


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


# =====================================================
# Run application
# =====================================================

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
