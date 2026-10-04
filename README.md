# Phonebook API

REST API телефонного справочника на FastAPI + PostgreSQL.

## Эндпоинты
- `GET /api/contacts` — список всех контактов
- `POST /api/contacts` — создать контакт
- `DELETE /api/contacts` — удалить все контакты
- `GET /api/contacts/{id}` — получить контакт
- `PUT /api/contacts/{id}` — обновить контакт
- `DELETE /api/contacts/{id}` — удалить контакт

## Локальный запуск
```bash
pip install -r requirements.txt
python main.py