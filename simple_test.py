#!/usr/bin/env python3
"""
Простий тест API
"""
import requests
import json

def simple_test():
    """Простий тест API"""
    print("🧪 Простий тест API...")
    
    # Тест 1: Отримання всіх контактів
    try:
        response = requests.get("http://localhost:8000/contacts/")
        print(f"✅ Статус: {response.status_code}")
        print(f"📄 Заголовки: {dict(response.headers)}")
        
        if response.status_code == 200:
            contacts = response.json()
            print(f"📄 Контакти: {json.dumps(contacts, indent=2, ensure_ascii=False)}")
        else:
            print(f"❌ Помилка: {response.text}")
            
    except Exception as e:
        print(f"❌ Помилка: {e}")

if __name__ == "__main__":
    simple_test() 