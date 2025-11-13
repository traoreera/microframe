"""
Routing models and data structures
"""

from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional


@dataclass
class RouteInfo:
    """
    Information about a route

    Attributes:
        path: URL path pattern
        func: Handler function
        methods: HTTP methods (GET, POST, etc.)
        tags: Tags for documentation
        summary: Short description
        description: Long description
        response_model: Expected response model
        status_code: Default status code
        deprecated: Whether route is deprecated
        include_in_schema: Include in OpenAPI docs
    """

    path: str
    func: Callable
    methods: List[str]
    tags: List[str] = field(default_factory=list)
    summary: Optional[str] = None
    description: Optional[str] = None
    response_model: Optional[Any] = None
    status_code: int = 200
    deprecated: bool = False
    include_in_schema: bool = True
    dependencies: List[Any] = field(default_factory=list)

    def __post_init__(self):
        """Post initialization processing"""
        if self.summary is None:
            self.summary = self.func.__name__.replace("_", " ").title()

        if self.description is None and self.func.__doc__:
            self.description = self.func.__doc__.strip()

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "path": self.path,
            "methods": self.methods,
            "tags": self.tags,
            "summary": self.summary,
            "description": self.description,
            "status_code": self.status_code,
            "deprecated": self.deprecated,
        }
