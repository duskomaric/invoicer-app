from sqlmodel import Session
from app.models.user import UserCreate
from app.models.client import ClientCreate
from app.services.user import create_user, get_user_by_email
from app.services.client import create_client

def seed_users(session: Session):
    """Seed the database with test users."""
    users = [
        {
            "email": "admin@example.com",
            "full_name": "Admin User",
            "password": "admin123",
            "is_active": True
        },
        {
            "email": "user@example.com",
            "full_name": "Regular User",
            "password": "user123",
            "is_active": True
        },
        {
            "email": "inactive@example.com",
            "full_name": "Inactive User",
            "password": "user123",
            "is_active": False
        },
    ]

    # Add 20 more users with numbered emails
    for i in range(1, 21):
        users.append({
            "email": f"user{i}@example.com",
            "full_name": f"Test User {i}",
            "password": f"user{i}pass",
            "is_active": i % 2 == 0  # alternate active/inactive
        })

    created_count = 0
    for user_data in users:
        if not get_user_by_email(session, user_data["email"]):
            user_create = UserCreate(
                email=user_data["email"],
                username=user_data["email"].split("@")[0],
                full_name=user_data["full_name"],
                password=user_data["password"]
            )
            user = create_user(session, user_create)

            # Update is_active if needed (create_user defaults to True)
            if not user_data["is_active"]:
                user.is_active = False
                session.add(user)
                session.commit()

            created_count += 1
            print(f"Created user: {user.email}")
        else:
            print(f"User already exists: {user_data['email']}")

    print(f"Total users created: {created_count}")
    return created_count


def seed_clients(session: Session):
    """Seed the database with test clients."""
    # Get the first user to assign clients to
    first_user = get_user_by_email(session, "admin@example.com")
    if not first_user:
        print("⚠️  No users found! Please run seed_users first.")
        return 0

    clients = [
        {
            "name": "Acme Corporation",
            "email": "contact@acme.com",
            "address": "123 Main Street, New York, NY 10001"
        },
        {
            "name": "TechStart Inc",
            "email": "hello@techstart.com",
            "address": "456 Tech Avenue, San Francisco, CA 94102"
        },
        {
            "name": "Global Services LLC",
            "email": "info@globalservices.com",
            "address": "789 Business Blvd, Chicago, IL 60601"
        },
    ]

    # Add 17 more clients with numbered names
    for i in range(1, 18):
        clients.append({
            "name": f"Client Company {i}",
            "email": f"client{i}@example.com",
            "address": f"{i * 100} Test Street, City, ST {10000 + i}" if i % 2 == 0 else None
        })

    created_count = 0
    for client_data in clients:
        client_create = ClientCreate(
            name=client_data["name"],
            email=client_data["email"],
            address=client_data.get("address")
        )
        client = create_client(session, client_create, user_id=first_user.id)
        created_count += 1
        print(f"Created client: {client.name}")

    print(f"Total clients created: {created_count}")
    return created_count
