from sqlmodel import Session, select, func
from app.models.product import Product, ProductCreate, ProductUpdate
from datetime import datetime

def get_product(db: Session, product_id: int, user_id: int) -> Product:
    return db.exec(select(Product).where(Product.id == product_id, Product.user_id == user_id)).first()

def get_products(db: Session, user_id: int, skip: int = 0, limit: int = 100, search: str = None):
    """
    Get products for a user with pagination.
    Returns tuple of (products, total_count, all_count)
    """
    query = select(Product).where(Product.user_id == user_id)
    
    if search:
        search_pattern = f"%{search}%"
        query = query.where(
            (Product.name.ilike(search_pattern)) | 
            (Product.description.ilike(search_pattern))
        )
    
    # Get total count with filters
    total_count = db.exec(select(func.count()).select_from(query.subquery())).one()
    
    # Get all count (unfiltered)
    all_count = db.exec(select(func.count()).where(Product.user_id == user_id)).one()
    
    # Get paginated products
    products = db.exec(query.offset(skip).limit(limit)).all()
    
    return products, total_count, all_count

def create_product(db: Session, product: ProductCreate, user_id: int) -> Product:
    db_product = Product(
        **product.model_dump(),
        user_id=user_id
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def update_product(db: Session, product_id: int, product_update: ProductUpdate, user_id: int) -> Product:
    db_product = get_product(db, product_id, user_id)
    if not db_product:
        return None

    update_data = product_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_product, field, value)

    db_product.updated_at = datetime.utcnow()
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def delete_product(db: Session, product_id: int, user_id: int) -> bool:
    db_product = get_product(db, product_id, user_id)
    if not db_product:
        return False

    db.delete(db_product)
    db.commit()
    return True
