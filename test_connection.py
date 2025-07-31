#!/usr/bin/env python3
"""
Скрипт для тестування підключення до PostgreSQL
"""
import sys
from sqlalchemy import text
from database import engine
from config import settings

def test_connection():
    """Тестує підключення до PostgreSQL"""
    print("🔍 Тестування підключення до PostgreSQL...")
    print(f"📡 DATABASE_URL: {settings.DATABASE_URL}")
    
    try:
        # Тестуємо підключення
        with engine.connect() as connection:
            result = connection.execute(text("SELECT version()"))
            version = result.fetchone()[0]
            print(f"✅ Підключення успішне!")
            print(f"📊 Версія PostgreSQL: {version}")
            
            # Тестуємо створення таблиці
            print("\n🔧 Тестування створення таблиць...")
            from models import Base
            Base.metadata.create_all(bind=engine)
            print("✅ Таблиці створені успішно!")
            
            return True
            
    except Exception as e:
        print(f"❌ Помилка підключення: {e}")
        print("\n🔧 Перевірте:")
        print("1. PostgreSQL сервер запущений")
        print("2. DATABASE_URL правильно налаштований")
        print("3. Користувач має права доступу")
        print("4. База даних існує")
        return False

if __name__ == "__main__":
    success = test_connection()
    sys.exit(0 if success else 1) 