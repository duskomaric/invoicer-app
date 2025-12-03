import requests
import random
from datetime import datetime, timedelta

BASE_URL = "http://localhost:8000/api/v1"

def seed_data():
    print("🌱 Starting database seed...")
    
    # 1. Register/Login User
    user_data = {
        "email": "test@example.com",
        "username": "testuser",
        "full_name": "Test User",
        "password": "password123"
    }
    
    # Try to login first
    login_data = {
        "username": user_data["email"],
        "password": user_data["password"]
    }
    
    response = requests.post(f"{BASE_URL}/auth/login", data=login_data)
    
    if response.status_code != 200:
        print("Creating test user...")
        response = requests.post(f"{BASE_URL}/users/", json=user_data)
        if response.status_code not in [200, 201]:
            if "already registered" not in response.text:
                print(f"Failed to create user: {response.text}")
                return
        
        # Login again
        response = requests.post(f"{BASE_URL}/auth/login", data=login_data)
    
    if response.status_code != 200:
        print(f"Login failed: {response.text}")
        return

    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    print("✅ User authenticated")

    # 2. Create Clients (50)
    print("Creating 50 clients...")
    client_ids = []
    for i in range(50):
        client_data = {
            "name": f"Client {i+1} - {random.choice(['Inc', 'LLC', 'Corp', 'Ltd'])}",
            "email": f"client{i+1}@example.com",
            "address": f"{random.randint(1, 999)} Business Rd, City {i+1}"
        }
        res = requests.post(f"{BASE_URL}/clients/", json=client_data, headers=headers)
        if res.status_code == 201:
            client_ids.append(res.json()["id"])
    print(f"✅ Created {len(client_ids)} clients")

    # 3. Create Products (50)
    print("Creating 50 products...")
    product_ids = []
    services = ["Consulting", "Development", "Design", "Audit", "Training", "Support"]
    for i in range(50):
        product_data = {
            "name": f"{random.choice(services)} Service {i+1}",
            "description": f"Professional services for project {i+1}",
            "price": float(random.randint(50, 500)),
            "currency": "USD"
        }
        res = requests.post(f"{BASE_URL}/products/", json=product_data, headers=headers)
        if res.status_code == 201:
            product_ids.append(res.json()["id"])
        else:
            print(f"Failed to create product: {res.status_code} {res.text}")
    print(f"✅ Created {len(product_ids)} products")

    # 4. Create Invoices (50)
    print("Creating 50 invoices...")
    statuses = ["draft", "sent", "paid", "cancelled"]
    invoice_count = 0
    
    if client_ids and product_ids:
        for i in range(50):
            # Random date within last year
            days_ago = random.randint(0, 365)
            due_date = (datetime.now() + timedelta(days=30)).isoformat()
            
            invoice_data = {
                "client_id": random.choice(client_ids),
                "due_date": due_date,
                "status": random.choice(statuses),
                "currency": "USD",
                "items": [
                    {
                        "product_id": random.choice(product_ids),
                        "quantity": random.randint(1, 10),
                        "unit_price": float(random.randint(50, 500))
                    }
                ]
            }
            res = requests.post(f"{BASE_URL}/invoices/", json=invoice_data, headers=headers)
            if res.status_code == 201:
                invoice_count += 1
            else:
                print(f"Failed to create invoice: {res.status_code} {res.text}")
    
    print(f"✅ Created {invoice_count} invoices")
    print("🎉 Seeding completed successfully!")

if __name__ == "__main__":
    seed_data()
