from sqlmodel import Session, select, func
from app.models.client import Client, ClientCreate, ClientUpdate
from datetime import datetime

def get_client(db: Session, client_id: int, user_id: int) -> Client:
    return db.exec(select(Client).where(Client.id == client_id, Client.user_id == user_id)).first()

def get_clients(db: Session, user_id: int, skip: int = 0, limit: int = 100, search: str = None):
    """
    Get clients for a user with pagination.
    Returns tuple of (clients, total_count, all_count)
    """
    query = select(Client).where(Client.user_id == user_id)
    
    if search:
        search_pattern = f"%{search}%"
        query = query.where(
            (Client.name.ilike(search_pattern)) | 
            (Client.email.ilike(search_pattern))
        )
    
    # Get total count with filters
    total_count = db.exec(select(func.count()).select_from(query.subquery())).one()
    
    # Get all count (unfiltered)
    all_count = db.exec(select(func.count()).where(Client.user_id == user_id)).one()
    
    # Get paginated clients
    clients = db.exec(query.offset(skip).limit(limit)).all()
    
    return clients, total_count, all_count

def create_client(db: Session, client: ClientCreate, user_id: int) -> Client:
    db_client = Client(
        **client.model_dump(),
        user_id=user_id
    )
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    return db_client

def update_client(db: Session, client_id: int, client_update: ClientUpdate, user_id: int) -> Client:
    db_client = get_client(db, client_id, user_id)
    if not db_client:
        return None

    update_data = client_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_client, field, value)

    db_client.updated_at = datetime.utcnow()
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    return db_client

def delete_client(db: Session, client_id: int, user_id: int) -> bool:
    db_client = get_client(db, client_id, user_id)
    if not db_client:
        return False

    db.delete(db_client)
    db.commit()
    return True
