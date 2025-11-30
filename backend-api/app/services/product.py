from sqlmodel import Session, select
from app.models.product import Product, ProductCreate, ProductUpdate
from datetime import datetime

def get_product(db: Session, product_id: int, user_id: int) -> Product:
    return db.exec(select(Product).where(Product.id == product_id, Product.user_id == user_id)).first()

def get_products(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.exec(select(Product).where(Product.user_id == user_id).offset(skip).limit(limit)).all()

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
