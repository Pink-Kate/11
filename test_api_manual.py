#!/usr/bin/env python3
"""
Ручне тестування API
"""
import requests
import json
from datetime import date

BASE_URL = "http://localhost:8000"

def test_api():
    """Тестує основні функції API"""
    print("🧪 Тестування Contacts API...")
    print(f"📍 Базовий URL: {BASE_URL}")
    
    # Тест 1: Отримання всіх контактів
    print("\n1️⃣ Тест отримання всіх контактів...")
    try:
        response = requests.get(f"{BASE_URL}/contacts/")
        print(f"✅ Статус: {response.status_code}")
        print(f"📄 Відповідь: {response.json()}")
    except Exception as e:
        print(f"❌ Помилка: {e}")
    
    # Тест 2: Створення контакту
    print("\n2️⃣ Тест створення контакту...")
    contact_data = {
        "first_name": "Марія",
        "last_name": "Коваленко",
        "email": "maria@example.com",
        "phone": "+380671234567",
        "birth_date": "1985-03-20",
        "additional_data": "Колега з роботи"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/contacts/",
            json=contact_data,
            headers={"Content-Type": "application/json"}
        )
        print(f"✅ Статус: {response.status_code}")
        created_contact = response.json()
        print(f"📄 Створений контакт: {json.dumps(created_contact, indent=2, ensure_ascii=False)}")
        contact_id = created_contact.get("id")
    except Exception as e:
        print(f"❌ Помилка: {e}")
        return
    
    # Тест 3: Отримання конкретного контакту
    print(f"\n3️⃣ Тест отримання контакту ID {contact_id}...")
    try:
        response = requests.get(f"{BASE_URL}/contacts/{contact_id}")
        print(f"✅ Статус: {response.status_code}")
        print(f"📄 Контакт: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    except Exception as e:
        print(f"❌ Помилка: {e}")
    
    # Тест 4: Пошук контактів
    print("\n4️⃣ Тест пошуку контактів...")
    try:
        response = requests.get(f"{BASE_URL}/contacts/search/?query=Марія")
        print(f"✅ Статус: {response.status_code}")
        print(f"📄 Результати пошуку: {response.json()}")
    except Exception as e:
        print(f"❌ Помилка: {e}")
    
    # Тест 5: Оновлення контакту
    print(f"\n5️⃣ Тест оновлення контакту ID {contact_id}...")
    update_data = {
        "phone": "+380631234567",
        "additional_data": "Оновлена інформація"
    }
    
    try:
        response = requests.put(
            f"{BASE_URL}/contacts/{contact_id}",
            json=update_data,
            headers={"Content-Type": "application/json"}
        )
        print(f"✅ Статус: {response.status_code}")
        print(f"📄 Оновлений контакт: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    except Exception as e:
        print(f"❌ Помилка: {e}")
    
    # Тест 6: Майбутні дні народження
    print("\n6️⃣ Тест майбутніх днів народження...")
    try:
        response = requests.get(f"{BASE_URL}/contacts/birthdays/upcoming/?days=30")
        print(f"✅ Статус: {response.status_code}")
        print(f"📄 Майбутні дні народження: {response.json()}")
    except Exception as e:
        print(f"❌ Помилка: {e}")
    
    # Тест 7: Видалення контакту
    print(f"\n7️⃣ Тест видалення контакту ID {contact_id}...")
    try:
        response = requests.delete(f"{BASE_URL}/contacts/{contact_id}")
        print(f"✅ Статус: {response.status_code}")
        print(f"📄 Відповідь: {response.json()}")
    except Exception as e:
        print(f"❌ Помилка: {e}")
    
    # Тест 8: Перевірка видалення
    print(f"\n8️⃣ Перевірка видалення контакту ID {contact_id}...")
    try:
        response = requests.get(f"{BASE_URL}/contacts/{contact_id}")
        print(f"✅ Статус: {response.status_code}")
        if response.status_code == 404:
            print("✅ Контакт успішно видалено")
        else:
            print(f"❌ Контакт все ще існує: {response.json()}")
    except Exception as e:
        print(f"❌ Помилка: {e}")
    
    print("\n🎉 Тестування завершено!")

if __name__ == "__main__":
    test_api() 