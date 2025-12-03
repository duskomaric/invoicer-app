from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import Optional
from app.core.database import get_session
from app.models.client import Client, ClientCreate, ClientUpdate, ClientResponse, ClientFiltersMeta
from app.models.user import User
from app.models.response_models import PaginatedResponse, Meta
from app.api.deps import get_current_user
from app.services.client import (
    get_client, get_clients, create_client, update_client, delete_client
)

router = APIRouter()

@router.post("/", response_model=ClientResponse, status_code=status.HTTP_201_CREATED)
def create_new_client(
    client: ClientCreate,
    db: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
) -> ClientResponse:
    return create_client(db=db, client=client, user_id=current_user.id)

@router.get("/", response_model=PaginatedResponse[ClientResponse])
def read_clients(
    skip: int = 0,
    limit: int = 100,
    search: Optional[str] = None,
    db: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
) -> PaginatedResponse[ClientResponse]:
    """
    Get all clients for the current user with pagination.
    """
    clients, total_count, all_count = get_clients(
        db=db,
        user_id=current_user.id,
        skip=skip,
        limit=limit,
        search=search
    )

    # Calculate page number (1-indexed)
    page = (skip // limit) + 1 if limit > 0 else 1

    # Create client-specific filters
    client_filters = ClientFiltersMeta(all_count=all_count)

    return PaginatedResponse(
        data=clients,
        meta=Meta(
            total=total_count,
            page=page,
            limit=limit,
            filters=client_filters.model_dump()
        )
    )

@router.get("/{client_id}", response_model=ClientResponse)
def read_client(
    client_id: int,
    db: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
) -> ClientResponse:
    client = get_client(db, client_id=client_id, user_id=current_user.id)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    return client

@router.put("/{client_id}", response_model=ClientResponse)
def update_existing_client(
    client_id: int,
    client_update: ClientUpdate,
    db: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
) -> ClientResponse:
    client = update_client(db, client_id=client_id, client_update=client_update, user_id=current_user.id)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    return client

@router.delete("/{client_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_existing_client(
    client_id: int,
    db: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
) -> None:
    success = delete_client(db, client_id=client_id, user_id=current_user.id)
    if not success:
        raise HTTPException(status_code=404, detail="Client not found")
    return None
