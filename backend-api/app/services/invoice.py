from sqlmodel import Session, select
from app.models.invoice import Invoice, InvoiceCreate, InvoiceUpdate, InvoiceItem
from datetime import datetime

def get_invoice(db: Session, invoice_id: int, user_id: int) -> Invoice:
    return db.exec(select(Invoice).where(Invoice.id == invoice_id, Invoice.user_id == user_id)).first()

def get_invoices(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.exec(select(Invoice).where(Invoice.user_id == user_id).offset(skip).limit(limit)).all()

def create_invoice(db: Session, invoice: InvoiceCreate, user_id: int) -> Invoice:
    # Calculate total amount
    total_amount = sum(item.quantity * item.unit_price for item in invoice.items)
    
    db_invoice = Invoice(
        client_id=invoice.client_id,
        user_id=user_id,
        status=invoice.status,
        due_date=invoice.due_date,
        currency=invoice.currency,
        is_recurring=invoice.is_recurring,
        recurring_interval=invoice.recurring_interval,
        total_amount=total_amount
    )
    db.add(db_invoice)
    db.commit()
    db.refresh(db_invoice)
    
    for item in invoice.items:
        db_item = InvoiceItem(
            invoice_id=db_invoice.id,
            product_id=item.product_id,
            quantity=item.quantity,
            unit_price=item.unit_price
        )
        db.add(db_item)
    
    db.commit()
    db.refresh(db_invoice)
    return db_invoice

def update_invoice(db: Session, invoice_id: int, invoice_update: InvoiceUpdate, user_id: int) -> Invoice:
    db_invoice = get_invoice(db, invoice_id, user_id)
    if not db_invoice:
        return None

    update_data = invoice_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_invoice, field, value)

    db_invoice.updated_at = datetime.utcnow()
    db.add(db_invoice)
    db.commit()
    db.refresh(db_invoice)
    return db_invoice

def delete_invoice(db: Session, invoice_id: int, user_id: int) -> bool:
    db_invoice = get_invoice(db, invoice_id, user_id)
    if not db_invoice:
        return False
        
    # Delete items first (cascade should handle this usually, but explicit is safe)
    for item in db_invoice.items:
        db.delete(item)

    db.delete(db_invoice)
    db.commit()
    return True
