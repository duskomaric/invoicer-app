import requests
import json

BASE_URL = "http://localhost:8000/api/v1"

def test_flow():
    # 1. Register User (if not exists)
    user_data = {
        "email": "test@example.com",
        "username": "testuser",
        "full_name": "Test User",
        "password": "password123"
    }
    
    # Try to login first to see if user exists
    login_data = {
        "username": user_data["email"],
        "password": user_data["password"]
    }
    
    response = requests.post(f"{BASE_URL}/auth/login", data=login_data)
    
    if response.status_code != 200:
        print("User not found or credentials wrong, creating user...")
        response = requests.post(f"{BASE_URL}/users/", json=user_data)
        if response.status_code == 201:
            print("User created successfully")
        elif response.status_code == 400 and "already registered" in response.text:
             print("User already exists")
        else:
            print(f"Failed to create user: {response.text}")
            return

        # Login again
        response = requests.post(f"{BASE_URL}/auth/login", data=login_data)
    
    if response.status_code != 200:
        print(f"Login failed: {response.text}")
        return

    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    print("Login successful, token obtained")

    # 2. Create Client
    client_data = {
        "name": "Test Client",
        "email": "client@test.com",
        "address": "123 Test St"
    }
    response = requests.post(f"{BASE_URL}/clients/", json=client_data, headers=headers)
    if response.status_code == 201:
        client = response.json()
        print(f"Client created: {client['id']}")
    else:
        print(f"Failed to create client: {response.text}")
        return

    # 3. Create Product
    product_data = {
        "name": "Test Product",
        "description": "A test product",
        "price": 100.0,
        "currency": "USD"
    }
    response = requests.post(f"{BASE_URL}/products/", json=product_data, headers=headers)
    if response.status_code == 201:
        product = response.json()
        print(f"Product created: {product['id']}")
    else:
        print(f"Failed to create product: {response.text}")
        return

    # 4. Create Invoice
    invoice_data = {
        "client_id": client["id"],
        "due_date": "2024-12-31T00:00:00",
        "status": "draft",
        "currency": "USD",
        "items": [
            {
                "product_id": product["id"],
                "quantity": 2,
                "unit_price": 100.0
            }
        ]
    }
    response = requests.post(f"{BASE_URL}/invoices/", json=invoice_data, headers=headers)
    if response.status_code == 201:
        invoice = response.json()
        print(f"Invoice created: {invoice['id']}")
        print(f"Total Amount: {invoice['total_amount']}")
    else:
        print(f"Failed to create invoice: {response.text}")
        return

    print("Verification flow completed successfully!")

if __name__ == "__main__":
    test_flow()
