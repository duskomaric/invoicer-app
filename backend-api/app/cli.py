import sys
import os

# Add the app directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import click
from sqlmodel import Session
from app.core.database import engine
from app.services.user import create_user as create_user_db, get_user_by_email, get_users
from app.models.user import UserCreate
from app.core.seeder import seed_users, seed_clients


# === USER COMMANDS ===
def _create_user(email, full_name, password):
    """Internal function to create user"""
    with Session(engine) as session:
        if get_user_by_email(session, email):
            click.echo(f"❌ User with email {email} already exists!")
            return False

        user_data = UserCreate(
            email=email,
            full_name=full_name,
            password=password
        )

        user = create_user_db(session, user_data)
        click.echo(f"✅ User created successfully!")
        click.echo(f"   ID: {user.id}")
        click.echo(f"   Email: {user.email}")
        return True


def _list_users():
    """Internal function to list users"""
    with Session(engine) as session:
        users = get_users(session)
        if not users:
            click.echo("No users found.")
            return

        click.echo("Users:")
        for user in users:
            click.echo(f"  ID: {user.id}, Email: {user.email}")


# === DATABASE COMMANDS ===
def _migrate():
    """Internal function to run migrations"""
    import os
    os.system("alembic upgrade head")
    click.echo("✅ Migrations completed!")


def _make_migration(message):
    """Internal function to create migration"""
    import os
    os.system(f'alembic revision --autogenerate -m "{message}"')
    click.echo("✅ Migration created!")


# === CLI COMMANDS ===
@click.group()
def cli():
    """FastAPI CLI Management"""
    pass


@cli.command()
@click.option('--email', prompt=True, help='User email')
@click.option('--full-name', prompt=True, help='Full name')
@click.option('--password', prompt=True, hide_input=True, confirmation_prompt=True, help='Password')
def create_user(email, full_name, password):
    """Create a new user"""
    _create_user(email, full_name, password)


@cli.command()
def list_users():
    """List all users"""
    _list_users()


@cli.command()
def migrate():
    """Run database migrations"""
    _migrate()


@cli.command()
@click.argument('message')
def make_migration(message):
    """Create a new migration"""
    _make_migration(message)


@cli.command()
def seed():
    """Seed the database with test data"""
    with Session(engine) as session:
        user_count = seed_users(session)
        click.echo(f"✅ Users seeded! Created {user_count} new users.")
        
        client_count = seed_clients(session)
        click.echo(f"✅ Clients seeded! Created {client_count} new clients.")
        
        click.echo(f"✅ Seeding completed! Total: {user_count} users, {client_count} clients.")


if __name__ == '__main__':
    cli()