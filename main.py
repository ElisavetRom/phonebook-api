import os
from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

import models
import schemas
from database import engine, get_db

# Создаём таблицы при старте (если их нет)
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Phonebook API", version="1.0")

# Jinja2 для отдачи HTML
templates = Jinja2Templates(directory="templates")


# ---------- HTML-страница ----------
@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# ---------- CRUD ----------

@app.get("/api/contacts", response_model=list[schemas.ContactOut])
def get_contacts(db: Session = Depends(get_db)):
    """Получить список всех контактов."""
    return db.query(models.Contact).all()


@app.post("/api/contacts", response_model=schemas.ContactOut, status_code=201)
def create_contact(contact: schemas.ContactCreate, db: Session = Depends(get_db)):
    """Создать новый контакт."""
    db_contact = models.Contact(**contact.model_dump())
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact


@app.delete("/api/contacts", status_code=204)
def delete_all_contacts(db: Session = Depends(get_db)):
    """Удалить все контакты."""
    db.query(models.Contact).delete()
    db.commit()
    return None


@app.get("/api/contacts/{contact_id}", response_model=schemas.ContactOut)
def get_contact(contact_id: int, db: Session = Depends(get_db)):
    """Получить контакт по ID."""
    contact = db.query(models.Contact).filter(models.Contact.id == contact_id).first()
    if not contact:
        raise HTTPException(status_code=404, detail="Контакт не найден")
    return contact


@app.put("/api/contacts/{contact_id}", response_model=schemas.ContactOut)
def update_contact(contact_id: int, data: schemas.ContactUpdate, db: Session = Depends(get_db)):
    """Обновить контакт по ID."""
    contact = db.query(models.Contact).filter(models.Contact.id == contact_id).first()
    if not contact:
        raise HTTPException(status_code=404, detail="Контакт не найден")
    for key, value in data.model_dump().items():
        setattr(contact, key, value)
    db.commit()
    db.refresh(contact)
    return contact


@app.delete("/api/contacts/{contact_id}", status_code=204)
def delete_contact(contact_id: int, db: Session = Depends(get_db)):
    """Удалить контакт по ID."""
    contact = db.query(models.Contact).filter(models.Contact.id == contact_id).first()
    if not contact:
        raise HTTPException(status_code=404, detail="Контакт не найден")
    db.delete(contact)
    db.commit()
    return None


# ---------- Точка входа для локального запуска ----------
if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)