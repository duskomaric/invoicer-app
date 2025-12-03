from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import Optional
from app.core.database import get_session
from app.models.invoice import Invoice, InvoiceCreate, InvoiceUpdate, InvoiceResponse, InvoiceFiltersMeta
from app.models.user import User
from app.models.response_models import PaginatedResponse, Meta
from app.api.deps import get_current_user
from app.services.invoice import (
    get_invoice, get_invoices, create_invoice, update_invoice, delete_invoice
)

router = APIRouter()

@router.post("/", response_model=InvoiceResponse, status_code=status.HTTP_201_CREATED)
def create_new_invoice(
    invoice: InvoiceCreate,
    db: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
) -> InvoiceResponse:
    return create_invoice(db=db, invoice=invoice, user_id=current_user.id)

@router.get("/", response_model=PaginatedResponse[InvoiceResponse])
def list_invoices(
    skip: int = 0,
    limit: int = 10,
    status: Optional[str] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
) -> PaginatedResponse[InvoiceResponse]:
    """
    Get all invoices for the current user with pagination.
    """
    invoices, total_count, all_count, draft_count, sent_count, paid_count, cancelled_count = get_invoices(
        db,
        user_id=current_user.id,
        skip=skip,
        limit=limit,
        status=status,
        search=search
    )

    # Calculate page number (1-indexed)
    page = (skip // limit) + 1 if limit > 0 else 1

    # Create invoice-specific filters
    invoice_filters = InvoiceFiltersMeta(
        all_count=all_count,
        draft_count=draft_count,
        sent_count=sent_count,
        paid_count=paid_count,
        cancelled_count=cancelled_count
    )
    
    return PaginatedResponse(
        data=invoices,
        meta=Meta(
            total=total_count,
            page=page,
            limit=limit,
            filters=invoice_filters.model_dump()
        )
    )

@router.get("/{invoice_id}", response_model=InvoiceResponse)
def read_invoice(
    invoice_id: int,
    db: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
) -> InvoiceResponse:
    invoice = get_invoice(db, invoice_id=invoice_id, user_id=current_user.id)
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    return invoice

@router.put("/{invoice_id}", response_model=InvoiceResponse)
def update_existing_invoice(
    invoice_id: int,
    invoice_update: InvoiceUpdate,
    db: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
) -> InvoiceResponse:
    invoice = update_invoice(db, invoice_id=invoice_id, invoice_update=invoice_update, user_id=current_user.id)
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    return invoice

@router.delete("/{invoice_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_existing_invoice(
    invoice_id: int,
    db: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
) -> None:
    success = delete_invoice(db, invoice_id=invoice_id, user_id=current_user.id)
    if not success:
        raise HTTPException(status_code=404, detail="Invoice not found")
    return None
