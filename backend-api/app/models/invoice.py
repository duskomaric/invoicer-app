from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime
from pydantic import ConfigDict

class InvoiceItem(SQLModel, table=True):
    __tablename__ = "invoice_items"

    id: int = Field(default=None, primary_key=True)
    invoice_id: int = Field(foreign_key="invoices.id")
    product_id: int = Field(foreign_key="products.id")
    quantity: int = Field(default=1)
    unit_price: float = Field(default=0.0)
    
    # Relationships
    invoice: "Invoice" = Relationship(back_populates="items")

class Invoice(SQLModel, table=True):
    __tablename__ = "invoices"

    id: int = Field(default=None, primary_key=True)
    client_id: int = Field(foreign_key="clients.id")
    user_id: int = Field(foreign_key="users.id")
    status: str = Field(default="draft")  # draft, sent, paid, cancelled
    due_date: datetime
    total_amount: float = Field(default=0.0)
    currency: str = Field(default="USD", max_length=3)
    
    # Recurring fields
    is_recurring: bool = Field(default=False)
    recurring_interval: Optional[str] = Field(default=None) # monthly, yearly, etc.
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    items: List[InvoiceItem] = Relationship(back_populates="invoice")

class InvoiceItemCreate(SQLModel):
    product_id: int
    quantity: int
    unit_price: float

class InvoiceCreate(SQLModel):
    client_id: int
    due_date: datetime
    status: str = "draft"
    currency: str = "USD"
    is_recurring: bool = False
    recurring_interval: Optional[str] = None
    items: List[InvoiceItemCreate]

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "client_id": 1,
                "due_date": "2024-02-01T00:00:00",
                "items": [
                    {
                        "product_id": 1,
                        "quantity": 5,
                        "unit_price": 100.00
                    }
                ]
            }
        }
    )

class InvoiceUpdate(SQLModel):
    status: Optional[str] = None
    due_date: Optional[datetime] = None
    is_recurring: Optional[bool] = None
    recurring_interval: Optional[str] = None

class InvoiceResponse(SQLModel):
    id: int
    client_id: int
    user_id: int
    status: str
    due_date: datetime
    total_amount: float
    currency: str
    is_recurring: bool
    recurring_interval: Optional[str]
    created_at: datetime
    updated_at: datetime
    items: List[InvoiceItem]
