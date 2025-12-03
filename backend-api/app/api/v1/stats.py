from fastapi import APIRouter, Depends
from sqlmodel import Session, select, func
from app.core.database import get_session
from app.api.deps import get_current_user
from app.models.user import User
from app.models.client import Client
from app.models.product import Product
from app.models.invoice import Invoice, InvoiceFiltersMeta
from pydantic import BaseModel

router = APIRouter()

class DashboardStats(BaseModel):
    users_count: int
    clients_count: int
    products_count: int
    invoices_count: int
    invoices_status_counts: InvoiceFiltersMeta

@router.get("/", response_model=DashboardStats)
def get_dashboard_stats(
    db: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    # Users count (all users in system)
    users_count = db.exec(select(func.count(User.id))).one()

    # Clients count (scoped to user)
    clients_count = db.exec(select(func.count(Client.id)).where(Client.user_id == current_user.id)).one()

    # Products count (scoped to user)
    products_count = db.exec(select(func.count(Product.id)).where(Product.user_id == current_user.id)).one()

    # Invoices count (scoped to user)
    invoices_count = db.exec(select(func.count(Invoice.id)).where(Invoice.user_id == current_user.id)).one()

    # Invoice status counts
    draft_count = db.exec(select(func.count(Invoice.id)).where(Invoice.user_id == current_user.id, Invoice.status == "draft")).one()
    sent_count = db.exec(select(func.count(Invoice.id)).where(Invoice.user_id == current_user.id, Invoice.status == "sent")).one()
    paid_count = db.exec(select(func.count(Invoice.id)).where(Invoice.user_id == current_user.id, Invoice.status == "paid")).one()
    cancelled_count = db.exec(select(func.count(Invoice.id)).where(Invoice.user_id == current_user.id, Invoice.status == "cancelled")).one()

    invoice_filters = InvoiceFiltersMeta(
        all_count=invoices_count,
        draft_count=draft_count,
        sent_count=sent_count,
        paid_count=paid_count,
        cancelled_count=cancelled_count
    )

    return DashboardStats(
        users_count=users_count,
        clients_count=clients_count,
        products_count=products_count,
        invoices_count=invoices_count,
        invoices_status_counts=invoice_filters
    )
