from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from datetime import datetime
from pydantic import ConfigDict, EmailStr, BaseModel


class ClientFiltersMeta(BaseModel):
    """Client-specific filter statistics"""
    all_count: int


class Client(SQLModel, table=True):
    __tablename__ = "clients"

    id: int = Field(default=None, primary_key=True)
    name: str = Field(index=True, max_length=100)
    email: str = Field(index=True, max_length=255)
    address: Optional[str] = Field(default=None, max_length=255)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    user_id: int = Field(foreign_key="users.id")
    
    # Relationships
    invoices: list["Invoice"] = Relationship(back_populates="client")

class ClientCreate(SQLModel):
    name: str
    email: str
    address: Optional[str] = None

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Acme Corp",
                "email": "contact@acme.com",
                "address": "123 Main St"
            }
        }
    )

class ClientUpdate(SQLModel):
    name: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Acme Corporation",
                "email": "newcontact@acme.com"
            }
        }
    )

class ClientResponse(SQLModel):
    id: int
    name: str
    email: str
    address: Optional[str]
    created_at: datetime
    updated_at: datetime
    user_id: int
