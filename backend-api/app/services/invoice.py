from sqlmodel import Session, select, func
from app.models.invoice import Invoice, InvoiceCreate, InvoiceUpdate, InvoiceItem
from app.models.client import Client
from datetime import datetime
from sqlalchemy.orm import selectinload

def get_invoice(db: Session, invoice_id: int, user_id: int) -> Invoice:
    return db.exec(
        select(Invoice)
        .where(Invoice.id == invoice_id, Invoice.user_id == user_id)
        .options(selectinload(Invoice.client))
        .options(selectinload(Invoice.items))
    ).first()

def get_invoices(db: Session, user_id: int, skip: int = 0, limit: int = 100, status: str = None, search: str = None):
    """
    Get invoices for a user with pagination.
    Returns tuple of (invoices, total_count, all_count, draft_count, sent_count, paid_count, cancelled_count)
    """
    # Base query for counts (all user invoices)
    base_query = select(Invoice).where(Invoice.user_id == user_id)
    
    # Get total count with filters (if any)
    # For the list, we apply status filter
    list_query = base_query
    if status and status != "all":
        list_query = list_query.where(Invoice.status == status)
        
    if search:
        # Simple search by ID for now, as joining with Client requires more changes
        # Check if search is numeric
        if search.isdigit():
            list_query = list_query.where(Invoice.id == int(search))
        
    # Get total count for the current filtered list
    total_count = db.exec(select(func.count()).select_from(list_query.subquery())).one()
    
    # Get counts for filter statistics (per status) - these should be based on ALL invoices
    all_count = db.exec(select(func.count()).select_from(base_query.subquery())).one()
    
    draft_count = db.exec(
        select(func.count()).where(Invoice.user_id == user_id, Invoice.status == "draft")
    ).one()
    
    sent_count = db.exec(
        select(func.count()).where(Invoice.user_id == user_id, Invoice.status == "sent")
    ).one()
    
    paid_count = db.exec(
        select(func.count()).where(Invoice.user_id == user_id, Invoice.status == "paid")
    ).one()
    
    cancelled_count = db.exec(
        select(func.count()).where(Invoice.user_id == user_id, Invoice.status == "cancelled")
    ).one()
    
    # Get paginated invoices
    invoices = db.exec(
        list_query
        .offset(skip)
        .limit(limit)
        .options(selectinload(Invoice.client))
        .options(selectinload(Invoice.items))
    ).all()
    
    return invoices, total_count, all_count, draft_count, sent_count, paid_count, cancelled_count

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
    
    # Handle items update separately
    items_data = update_data.pop("items", None)
    
    for field, value in update_data.items():
        setattr(db_invoice, field, value)

    if items_data is not None:
        # Delete existing items
        for item in db_invoice.items:
            db.delete(item)
        
        # Create new items
        new_items = []
        for item_data in items_data:
            db_item = InvoiceItem(
                invoice_id=db_invoice.id,
                product_id=item_data["product_id"],
                quantity=item_data["quantity"],
                unit_price=item_data["unit_price"]
            )
            db.add(db_item)
            new_items.append(db_item)
            
        # Recalculate total amount
        total_amount = sum(item.quantity * item.unit_price for item in new_items)
        db_invoice.total_amount = total_amount

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
