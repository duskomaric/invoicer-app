import os
from typing import List
from dotenv import load_dotenv

load_dotenv()


class Settings:
    # FastAPI Application
    APP_TITLE: str = os.getenv("APP_TITLE")
    APP_DESCRIPTION: str = os.getenv("APP_DESCRIPTION")
    APP_VERSION: str = os.getenv("APP_VERSION")

    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL")

    # Application
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    DEBUG: bool = os.getenv("DEBUG").lower() == "true"

    # CORS
#     ALLOWED_HOSTS: List[str] = os.getenv("ALLOWED_HOSTS", "").split(",")
    ALLOWED_HOSTS: List[str] = ["http://localhost:3000", "http://127.0.0.1:3000", "http://localhost:5173", "http://localhost:5174"]

    # JWT
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30


settings = Settings()