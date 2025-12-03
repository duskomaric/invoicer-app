from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import Optional
from app.core.database import get_session
from app.models.user import User, UserCreate, UserUpdate, UserResponse, UserFiltersMeta
from app.models.response_models import PaginatedResponse, Meta
from app.api.deps import get_current_user
from app.services.user import (
    get_user, get_users, create_user, update_user, delete_user,
    get_user_by_email
)
import re

router = APIRouter()

# Basic email validation regex
def validate_email(email: str) -> bool:
    return bool(re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$').match(email))

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_new_user(
    user: UserCreate, 
    db: Session = Depends(get_session),
) -> UserResponse:
    # Validate email format
    if not validate_email(user.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid email format"
        )

    # Check if email already exists
    db_user = get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    return create_user(db=db, user=user)


@router.get("/", response_model=PaginatedResponse[UserResponse])
def read_users(
    skip: int = 0, 
    limit: int = 100,
    search: Optional[str] = None,
    is_active: Optional[bool] = None,
    db: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
) -> PaginatedResponse[UserResponse]:
    """
    Get all users with optional search and filter parameters.
    Returns paginated response with metadata.
    
    Query Parameters:
        - skip: Number of records to skip (default: 0)
        - limit: Maximum records to return (default: 100)
        - search: Search string to filter by email or full_name
        - is_active: Filter by active status (true/false)
    """
    users, total_count, all_count, active_count, inactive_count = get_users(
        db, 
        skip=skip, 
        limit=limit,
        search=search,
        is_active=is_active
    )
    
    # Calculate page number (1-indexed)
    page = (skip // limit) + 1 if limit > 0 else 1
    
    # Create user-specific filters
    user_filters = UserFiltersMeta(
        all_count=all_count,
        active_count=active_count,
        inactive_count=inactive_count
    )
    
    return PaginatedResponse(
        data=users,
        meta=Meta(
            total=total_count,
            page=page,
            limit=limit,
            filters=user_filters.model_dump()  # Convert to dict
        )
    )


@router.get("/{user_id}", response_model=UserResponse)
def read_user(
    user_id: int, 
    db: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
) -> UserResponse:
    db_user = get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return db_user


@router.put("/{user_id}", response_model=UserResponse)
def update_existing_user(
    user_id: int, 
    user: UserUpdate, 
    db: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
) -> UserResponse:
    db_user = update_user(db, user_id=user_id, user_update=user)
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return db_user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_existing_user(
    user_id: int, 
    db: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
) -> None:
    success = delete_user(db, user_id=user_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return None