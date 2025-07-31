from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
import crud
import models
import schemas
from database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Contacts API",
    description="REST API для управління контактами",
    version="1.0.0",
    openapi_tags=[
        {
            "name": "contacts",
            "description": "Операції з контактами"
        },
        {
            "name": "search",
            "description": "Пошук контактів"
        },
        {
            "name": "birthdays",
            "description": "Дні народження"
        }
    ]
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Middleware для правильного кодування UTF-8
@app.middleware("http")
async def add_utf8_headers(request, call_next):
    response = await call_next(request)
    if "application/json" in response.headers.get("content-type", ""):
        response.headers["content-type"] = "application/json; charset=utf-8"
    return response

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", tags=["root"])
def read_root():
    return FileResponse("templates/index.html", media_type="text/html; charset=utf-8")

@app.get("/web", tags=["web"])
def web_interface():
    return FileResponse("templates/index.html", media_type="text/html; charset=utf-8")

@app.post("/contacts/", response_model=schemas.Contact, tags=["contacts"])
def create_contact(contact: schemas.ContactCreate, db: Session = Depends(get_db)):
    return crud.create_contact(db=db, contact=contact)

@app.get("/contacts/", response_model=List[schemas.Contact], tags=["contacts"])
def read_contacts(
    skip: int = Query(0, ge=0, description="Кількість записів для пропуску"),
    limit: int = Query(100, ge=1, le=1000, description="Максимальна кількість записів"),
    db: Session = Depends(get_db)
):
    contacts = crud.get_contacts(db, skip=skip, limit=limit)
    return contacts

@app.get("/contacts/{contact_id}", response_model=schemas.Contact, tags=["contacts"])
def read_contact(contact_id: int, db: Session = Depends(get_db)):
    contact = crud.get_contact(db, contact_id=contact_id)
    if contact is None:
        raise HTTPException(status_code=404, detail="Контакт не знайдено")
    return contact

@app.put("/contacts/{contact_id}", response_model=schemas.Contact, tags=["contacts"])
def update_contact(contact_id: int, contact: schemas.ContactUpdate, db: Session = Depends(get_db)):
    updated_contact = crud.update_contact(db, contact_id=contact_id, contact=contact)
    if updated_contact is None:
        raise HTTPException(status_code=404, detail="Контакт не знайдено")
    return updated_contact

@app.delete("/contacts/{contact_id}", tags=["contacts"])
def delete_contact(contact_id: int, db: Session = Depends(get_db)):
    success = crud.delete_contact(db, contact_id=contact_id)
    if not success:
        raise HTTPException(status_code=404, detail="Контакт не знайдено")
    return {"message": "Контакт успішно видалено"}

@app.get("/contacts/search/", response_model=List[schemas.Contact], tags=["search"])
def search_contacts(
    query: str = Query(..., description="Пошуковий запит для імені, прізвища або email"),
    db: Session = Depends(get_db)
):
    contacts = crud.search_contacts(db, query=query)
    return contacts

@app.get("/contacts/birthdays/upcoming/", response_model=List[schemas.Contact], tags=["birthdays"])
def get_upcoming_birthdays(
    days: int = Query(7, ge=1, le=365, description="Кількість днів для перегляду"),
    db: Session = Depends(get_db)
):
    contacts = crud.get_upcoming_birthdays(db, days=days)
    return contacts