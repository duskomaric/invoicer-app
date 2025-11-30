# 🐍 FastAPI Docker Project

Complete **FastAPI** project with **Docker**, **SQLModel**, **Alembic migrations**, and **PostgreSQL**.

---

## 🚀 Quick Start

```bash
# Clone & setup
git clone <your-repo>
cd fastapi-docker-project

# Start services
docker-compose up -d

# Run migrations
docker-compose exec app alembic upgrade head
```
```bash
# Create user
docker-compose exec app python app/cli.py create-user --email admin@example.com --username admin --full-name "Admin User" --password admin123
docker-compose exec app python app/cli.py create-user
docker-compose exec app python app/cli.py list-users
```

##🐳 Docker Commands
```bash
# Start services in background
docker-compose up -d

# Stop services
docker-compose down

# View running containers
docker-compose ps

# View logs
docker-compose logs -f app

# Access container shell
docker-compose exec app bash

# Restart service
docker-compose restart app

# Rebuild Container
docker-compose build --no-cache
docker-compose up -d

# 🗄️ Database Management
# Migrations
# Create new migration
docker-compose exec app alembic revision --autogenerate -m "description"

# Run migrations
docker-compose exec app alembic upgrade head

# Check migration status
docker-compose exec app alembic current

# Migrate Fresh
# Reset and re-run migrations
docker-compose exec app alembic downgrade base
docker-compose exec app alembic upgrade head

# Complete database reset
docker-compose down -v
docker-compose up -d
docker-compose exec app alembic upgrade head


```

bash
```
🔄 Development Workflow

Start services:

docker-compose up -d


Code changes auto-reload via volume mount.

Model changes:

docker-compose exec app alembic revision --autogenerate -m "add_field"
docker-compose exec app alembic upgrade head


New dependencies:

# Add to requirements.txt
docker-compose build --no-cache
```


Access:
API: http://localhost:8000

Docs: http://localhost:8000/docs

Health: http://localhost:8000/health
