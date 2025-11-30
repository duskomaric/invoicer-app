from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
from pydantic import ConfigDict

class Product(SQLModel, table=True):
    __tablename__ = "products"

    id: int = Field(default=None, primary_key=True)
    name: str = Field(index=True, max_length=100)
    description: Optional[str] = Field(default=None)
    price: float = Field(default=0.0)
    currency: str = Field(default="USD", max_length=3)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    user_id: int = Field(foreign_key="users.id")

class ProductCreate(SQLModel):
    name: str
    description: Optional[str] = None
    price: float
    currency: str = "USD"

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Consulting Service",
                "description": "Hourly consulting rate",
                "price": 150.00,
                "currency": "USD"
            }
        }
    )

class ProductUpdate(SQLModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    currency: Optional[str] = None

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "price": 175.00
            }
        }
    )

class ProductResponse(SQLModel):
    id: int
    name: str
    description: Optional[str]
    price: float
    currency: str
    created_at: datetime
    updated_at: datetime
    user_id: int
