import sys
import os
from typing import Optional

# Add current directory to path
sys.path.append(os.getcwd())

from sqlmodel import Session, create_engine, select
from app.services.product import get_products
from app.services.invoice import get_invoices
from app.models.user import User
from dotenv import load_dotenv

load_dotenv()

# Use the database URL from .env or default
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/fastapi_db")
# Adjust host if running outside docker but db is in docker
# If running from host machine, might need localhost:5432
if "db:5432" in DATABASE_URL:
    DATABASE_URL = DATABASE_URL.replace("db:5432", "localhost:5432")

engine = create_engine(DATABASE_URL)

def test_services():
    print(f"Testing services with DB: {DATABASE_URL}")
    try:
        with Session(engine) as db:
            # Get a user to test with
            user = db.exec(select(User)).first()
            if not user:
                print("❌ No users found in DB. Run seed.py first.")
                return
            
            print(f"Testing with user: {user.email} (ID: {user.id})")

            # Test Products
            print("\n--- Testing Products ---")
            print("Calling get_products()...")
            products, total, all_c = get_products(db, user_id=user.id, skip=0, limit=10)
            print(f"✅ Success! Found {len(products)} products. Total: {total}")
            
            print("Calling get_products(search='test')...")
            products, total, all_c = get_products(db, user_id=user.id, search="test")
            print(f"✅ Success with search! Found {len(products)} products.")

            # Test Invoices
            print("\n--- Testing Invoices ---")
            print("Calling get_invoices()...")
            invoices, total, all_c, d, s, p, c = get_invoices(db, user_id=user.id, skip=0, limit=10)
            print(f"✅ Success! Found {len(invoices)} invoices. Total: {total}")

            print("Calling get_invoices(search='1')...")
            invoices, total, all_c, d, s, p, c = get_invoices(db, user_id=user.id, search="1")
            print(f"✅ Success with search! Found {len(invoices)} invoices.")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_services()
