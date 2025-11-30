from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from app.core.database import get_session
from app.models.invoice import InvoiceCreate, InvoiceUpdate, InvoiceResponse
from app.models.user import User
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

@router.get("/", response_model=list[InvoiceResponse])
def read_invoices(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
) -> list[InvoiceResponse]:
    return get_invoices(db, user_id=current_user.id, skip=skip, limit=limit)

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
