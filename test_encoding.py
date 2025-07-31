#!/usr/bin/env python3
"""
Тест кодування UTF-8
"""
import requests
import json

def test_encoding():
    """Тестує кодування UTF-8"""
    print("🔤 Тестування кодування UTF-8...")
    
    # Тест 1: Створення контакту з кириличними символами
    contact_data = {
        "first_name": "Іван",
        "last_name": "Петренко",
        "email": "ivan@example.com",
        "phone": "+380501234567",
        "birth_date": "1990-01-15",
        "additional_data": "Тестовий контакт з кириличними символами"
    }
    
    try:
        response = requests.post(
            "http://localhost:8000/contacts/",
            json=contact_data,
            headers={"Content-Type": "application/json; charset=utf-8"}
        )
        print(f"✅ Статус створення: {response.status_code}")
        
        if response.status_code == 200:
            created_contact = response.json()
            print("📄 Створений контакт:")
            print(json.dumps(created_contact, indent=2, ensure_ascii=False))
            
            # Тест 2: Отримання всіх контактів
            response = requests.get("http://localhost:8000/contacts/")
            print(f"\n✅ Статус отримання: {response.status_code}")
            
            if response.status_code == 200:
                contacts = response.json()
                print("📄 Всі контакти:")
                print(json.dumps(contacts, indent=2, ensure_ascii=False))
                
                # Перевірка кодування
                for contact in contacts:
                    if contact.get("first_name") == "Іван":
                        print("✅ Кириличні символи відображаються правильно!")
                        break
                else:
                    print("❌ Проблема з кодуванням кириличних символів")
            else:
                print(f"❌ Помилка отримання контактів: {response.text}")
        else:
            print(f"❌ Помилка створення контакту: {response.text}")
            
    except Exception as e:
        print(f"❌ Помилка: {e}")

if __name__ == "__main__":
    test_encoding() 