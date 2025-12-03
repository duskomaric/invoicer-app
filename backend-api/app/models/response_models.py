from typing import Generic, TypeVar, Optional, Dict, Any
from pydantic import BaseModel

# Generic type for data
T = TypeVar('T')


class Meta(BaseModel):
    """Metadata for paginated responses"""
    total: int  # Total records matching filters
    page: int  # Current page number (1-indexed)
    limit: int  # Items per page
    filters: Optional[Dict[str, Any]] = None  # Optional filter statistics (model-specific)


class PaginatedResponse(BaseModel, Generic[T]):
    """Generic paginated response wrapper"""
    data: list[T]
    meta: Meta

    class Config:
        # Allow arbitrary types for generic support
        arbitrary_types_allowed = True
