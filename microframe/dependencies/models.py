"""
Dependency models
"""
from typing import Callable


class Depends:
    """
    Dependency marker for dependency injection
    
    Example:
        def get_db():
            return Database()
        
        @app.get("/users")
        async def get_users(db = Depends(get_db)):
            return db.query_all()
    """
    
    def __init__(
        self,
        dependency: Callable,
        *,
        use_cache: bool = True
    ):
        self.dependency = dependency
        self.use_cache = use_cache
        self._cache_key = f"depends_{id(dependency)}"
    
    def __repr__(self):
        return f"Depends({self.dependency.__name__})"
