from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from app.core.database import get_session
from app.models.client import ClientCreate, ClientUpdate, ClientResponse
from app.models.user import User
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

@router.get("/", response_model=list[ClientResponse])
def read_clients(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
) -> list[ClientResponse]:
    return get_clients(db, user_id=current_user.id, skip=skip, limit=limit)

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
