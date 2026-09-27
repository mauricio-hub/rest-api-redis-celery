# 📊 Asynchronous Reports System

Django REST Framework with Celery and Redis for background task processing.

---

## 🚀 Quick Start

### Setup
```bash
python -m venv venv
venv\Scripts\activate
pip install django djangorestframework celery redis
python manage.py migrate
docker run -d --name redis -p 6379:6379 redis:latest
```

### Run (2 terminals)
```bash
# Terminal 1
python manage.py runserver

# Terminal 2
celery -A config worker -l info
```

---

## 📡 API

```bash
POST   /api/reports/          # Create
GET    /api/reports/          # List
GET    /api/reports/1/        # Get one
GET    /api/reports/1/status/ # Check status
PUT    /api/reports/1/        # Update
DELETE /api/reports/1/        # Delete
```

---

## 📊 States

`pending` → `processing` → `completed` | `failed`

---

## 🛠️ Tech

Django • DRF • Celery • Redis • SQLite