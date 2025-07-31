from sqlalchemy.orm import Session
from sqlalchemy import or_, and_, extract
from datetime import date, timedelta
from typing import List, Optional
import models
import schemas

def create_contact(db: Session, contact: schemas.ContactCreate) -> models.Contact:
    db_contact = models.Contact(**contact.dict())
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact

def get_contacts(db: Session, skip: int = 0, limit: int = 100) -> List[models.Contact]:
    return db.query(models.Contact).offset(skip).limit(limit).all()

def get_contact(db: Session, contact_id: int) -> Optional[models.Contact]:
    return db.query(models.Contact).filter(models.Contact.id == contact_id).first()

def update_contact(db: Session, contact_id: int, contact: schemas.ContactUpdate) -> Optional[models.Contact]:
    db_contact = db.query(models.Contact).filter(models.Contact.id == contact_id).first()
    if db_contact:
        update_data = contact.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_contact, field, value)
        db.commit()
        db.refresh(db_contact)
    return db_contact

def delete_contact(db: Session, contact_id: int) -> bool:
    db_contact = db.query(models.Contact).filter(models.Contact.id == contact_id).first()
    if db_contact:
        db.delete(db_contact)
        db.commit()
        return True
    return False

def search_contacts(db: Session, query: str) -> List[models.Contact]:
    return db.query(models.Contact).filter(
        or_(
            models.Contact.first_name.ilike(f"%{query}%"),
            models.Contact.last_name.ilike(f"%{query}%"),
            models.Contact.email.ilike(f"%{query}%")
        )
    ).all()

def get_upcoming_birthdays(db: Session, days: int = 7) -> List[models.Contact]:
    today = date.today()
    end_date = today + timedelta(days=days)
    
    current_year_birthdays = db.query(models.Contact).filter(
        and_(
            extract('month', models.Contact.birth_date) >= today.month,
            extract('day', models.Contact.birth_date) >= today.day,
            extract('month', models.Contact.birth_date) <= end_date.month,
            extract('day', models.Contact.birth_date) <= end_date.day
        )
    ).all()
    
    next_year_birthdays = db.query(models.Contact).filter(
        and_(
            extract('month', models.Contact.birth_date) >= 1,
            extract('day', models.Contact.birth_date) >= 1,
            extract('month', models.Contact.birth_date) <= end_date.month,
            extract('day', models.Contact.birth_date) <= end_date.day
        )
    ).all()
    
    return current_year_birthdays + next_year_birthdays