from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from app.core.database import get_session
from app.models.product import ProductCreate, ProductUpdate, ProductResponse
from app.models.user import User
from app.api.deps import get_current_user
from app.services.product import (
    get_product, get_products, create_product, update_product, delete_product
)

router = APIRouter()

@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def create_new_product(
    product: ProductCreate,
    db: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
) -> ProductResponse:
    return create_product(db=db, product=product, user_id=current_user.id)

@router.get("/", response_model=list[ProductResponse])
def read_products(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
) -> list[ProductResponse]:
    return get_products(db, user_id=current_user.id, skip=skip, limit=limit)

@router.get("/{product_id}", response_model=ProductResponse)
def read_product(
    product_id: int,
    db: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
) -> ProductResponse:
    product = get_product(db, product_id=product_id, user_id=current_user.id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.put("/{product_id}", response_model=ProductResponse)
def update_existing_product(
    product_id: int,
    product_update: ProductUpdate,
    db: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
) -> ProductResponse:
    product = update_product(db, product_id=product_id, product_update=product_update, user_id=current_user.id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_existing_product(
    product_id: int,
    db: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
) -> None:
    success = delete_product(db, product_id=product_id, user_id=current_user.id)
    if not success:
        raise HTTPException(status_code=404, detail="Product not found")
    return None
