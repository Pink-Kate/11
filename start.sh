#!/bin/bash

echo "🚀 Запуск Contacts API з PostgreSQL..."

# Перевірка чи встановлений Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker не встановлений. Будь ласка, встановіть Docker спочатку."
    exit 1
fi

# Перевірка чи встановлений Docker Compose
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose не встановлений. Будь ласка, встановіть Docker Compose спочатку."
    exit 1
fi

echo "📦 Збірка та запуск контейнерів..."
docker-compose up --build -d

echo "⏳ Очікування готовності бази даних..."
sleep 10

echo "✅ Додаток запущений!"
echo ""
echo "🌐 Доступні URL:"
echo "   - API документація: http://localhost:8000/docs"
echo "   - ReDoc документація: http://localhost:8000/redoc"
echo "   - Веб-інтерфейс: http://localhost:8000/web"
echo ""
echo "📊 База даних PostgreSQL доступна на localhost:5432"
echo "   - База даних: contacts_db"
echo "   - Користувач: contacts_user"
echo "   - Пароль: contacts_password"
echo ""
echo "🛑 Для зупинки використовуйте: docker-compose down" 