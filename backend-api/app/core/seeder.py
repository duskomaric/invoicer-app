from sqlmodel import Session
from app.models.user import UserCreate
from app.services.user import create_user, get_user_by_email

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

    # Add 20 more users with numbered emails and usernames
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
