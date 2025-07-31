import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # Використовуємо SQLite для розробки, PostgreSQL для production
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./contacts_dev.db")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-here")

settings = Settings()