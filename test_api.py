import requests
import json

BASE_URL = "http://localhost:8000"

def test_create_contact():
    contact_data = {
        "first_name": "Іван",
        "last_name": "Петренко",
        "email": "ivan@example.com",
        "phone": "+380501234567",
        "birth_date": "1990-05-15",
        "additional_data": "Дружній та відповідальний"
    }
    
    response = requests.post(f"{BASE_URL}/contacts/", json=contact_data)
    print(f"Створення контакту: {response.status_code}")
    if response.status_code == 200:
        print(f"Створено контакт: {response.json()}")
    return response.json() if response.status_code == 200 else None

def test_get_contacts():
    response = requests.get(f"{BASE_URL}/contacts/")
    print(f"Отримання контактів: {response.status_code}")
    if response.status_code == 200:
        contacts = response.json()
        print(f"Знайдено {len(contacts)} контактів")
        for contact in contacts:
            print(f"- {contact['first_name']} {contact['last_name']} ({contact['email']})")
    return response.json() if response.status_code == 200 else []

def test_search_contacts():
    query = "Іван"
    response = requests.get(f"{BASE_URL}/contacts/search/?query={query}")
    print(f"Пошук контактів за '{query}': {response.status_code}")
    if response.status_code == 200:
        contacts = response.json()
        print(f"Знайдено {len(contacts)} контактів")
        for contact in contacts:
            print(f"- {contact['first_name']} {contact['last_name']} ({contact['email']})")
    return response.json() if response.status_code == 200 else []

def test_get_upcoming_birthdays():
    response = requests.get(f"{BASE_URL}/contacts/birthdays/upcoming/")
    print(f"Дні народження на найближчі 7 днів: {response.status_code}")
    if response.status_code == 200:
        contacts = response.json()
        print(f"Знайдено {len(contacts)} контактів з днями народження")
        for contact in contacts:
            print(f"- {contact['first_name']} {contact['last_name']} ({contact['birth_date']})")
    return response.json() if response.status_code == 200 else []

def test_update_contact(contact_id):
    update_data = {
        "phone": "+380509876543",
        "additional_data": "Оновлена інформація"
    }
    
    response = requests.put(f"{BASE_URL}/contacts/{contact_id}", json=update_data)
    print(f"Оновлення контакту {contact_id}: {response.status_code}")
    if response.status_code == 200:
        print(f"Оновлено контакт: {response.json()}")
    return response.json() if response.status_code == 200 else None

def test_delete_contact(contact_id):
    response = requests.delete(f"{BASE_URL}/contacts/{contact_id}")
    print(f"Видалення контакту {contact_id}: {response.status_code}")
    if response.status_code == 200:
        print("Контакт успішно видалено")
    return response.status_code == 200

if __name__ == "__main__":
    print("=== Тестування Contacts API ===\n")
    
    print("1. Створення контакту")
    contact = test_create_contact()
    print()
    
    print("2. Отримання всіх контактів")
    contacts = test_get_contacts()
    print()
    
    print("3. Пошук контактів")
    search_results = test_search_contacts()
    print()
    
    print("4. Дні народження")
    birthdays = test_get_upcoming_birthdays()
    print()
    
    if contact:
        print("5. Оновлення контакту")
        updated_contact = test_update_contact(contact['id'])
        print()
        
        print("6. Видалення контакту")
        test_delete_contact(contact['id'])
        print()
    
    print("=== Тестування завершено ===")