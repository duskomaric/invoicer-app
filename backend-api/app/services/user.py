from sqlmodel import Session, select, func
from app.models.user import User
from typing import Optional
from app.models.user import UserCreate, UserUpdate
from passlib.context import CryptContext
from datetime import datetime

pwd_context = CryptContext(
    schemes=["pbkdf2_sha256"],
    deprecated="auto",
    pbkdf2_sha256__default_rounds=30000
)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_user(db: Session, user_id: int) -> User:
    return db.exec(select(User).where(User.id == user_id)).first()


def get_user_by_email(db: Session, email: str) -> User:
    return db.exec(select(User).where(User.email == email)).first()


def get_users(
    db: Session, 
    skip: int = 0, 
    limit: int = 100,
    search: Optional[str] = None,
    is_active: Optional[bool] = None
):
    """
    Get users with optional search and filter parameters.
    Returns tuple of (users, total_count, all_count, active_count, inactive_count)
    
    Args:
        db: Database session
        skip: Number of records to skip (pagination)
        limit: Maximum number of records to return
        search: Optional search string to filter by email or full_name
        is_active: Optional filter by active status
        
    Returns:
        users: List of filtered users
        total_count: Total matching current filters (for pagination)
        all_count: Total users (unfiltered, for "All" filter button)
        active_count: Total active users (unfiltered, for filter buttons)
        inactive_count: Total inactive users (unfiltered, for filter buttons)
    """
    # Build base query for filtered results
    query = select(User)
    
    # Apply search filter
    if search:
        search_pattern = f"%{search}%"
        query = query.where(
            (User.email.ilike(search_pattern)) | 
            (User.full_name.ilike(search_pattern))
        )
    
    # Apply status filter
    if is_active is not None:
        query = query.where(User.is_active == is_active)
    
    # Get total count with current filters applied (for pagination)
    total_count = db.exec(select(func.count()).select_from(query.subquery())).one()
    
    # Get counts for filter statistics (UNFILTERED - show all users)
    all_count = db.exec(select(func.count(User.id))).one()
    
    active_count = db.exec(
        select(func.count()).where(User.is_active == True)
    ).one()
    
    inactive_count = db.exec(
        select(func.count()).where(User.is_active == False)
    ).one()
    
    # Apply pagination and get users
    paginated_query = query.offset(skip).limit(limit)
    users = db.exec(paginated_query).all()
    
    return users, total_count, all_count, active_count, inactive_count


def create_user(db: Session, user: UserCreate) -> User:
    hashed_password = get_password_hash(user.password)
    db_user = User(
        email=user.email,
        full_name=user.full_name,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, user_id: int, user_update: UserUpdate) -> User:
    db_user = get_user(db, user_id)
    if not db_user:
        return None

    update_data = user_update.model_dump(exclude_unset=True)

    if "password" in update_data:
        update_data["hashed_password"] = get_password_hash(update_data.pop("password"))

    for field, value in update_data.items():
        setattr(db_user, field, value)

    db_user.updated_at = datetime.utcnow()
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int) -> bool:
    db_user = get_user(db, user_id)
    if not db_user:
        return False

    db.delete(db_user)
    db.commit()
    return True