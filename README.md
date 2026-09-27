# 📊 Asynchronous Reports System

A simple asynchronous report generation system built with **Django REST Framework, Celery, and Redis**.

The API creates a report and sends the long-running processing task to **Celery**, so the HTTP request does not have to wait for the report to finish.

---

## 🚀 Quick Start

### 1. Create virtual environment

```bash
python -m venv venv
venv\Scripts\activate
```

### 2. Install dependencies

```bash
pip install django djangorestframework celery redis
```

### 3. Run migrations

```bash
python manage.py migrate
```

### 4. Start Redis

```bash
docker run -d --name redis -p 6379:6379 redis:latest
```

### 5. Run the application

You need **2 terminals**:

**Terminal 1 — Django**

```bash
python manage.py runserver
```

**Terminal 2 — Celery**

```bash
celery -A config worker -l info
```

---

## 🔄 How It Works

When a report is created:

```text
Client
  │
  │ POST /api/reports/
  ▼
Django API
  │
  │ Send task
  ▼
Redis
  │
  │ Queue
  ▼
Celery Worker
  │
  │ Generate report
  ▼
Database
```

The API responds immediately instead of keeping the request open while the report is being generated.

The report can then be monitored using the status endpoint.

---

## 📡 API

| Method | Endpoint                 | Description             |
| ------ | ------------------------ | ----------------------- |
| POST   | `/api/reports/`          | Create a report         |
| GET    | `/api/reports/`          | List reports            |
| GET    | `/api/reports/1/`        | Get a report            |
| GET    | `/api/reports/1/status/` | Check processing status |
| PUT    | `/api/reports/1/`        | Update a report         |
| DELETE | `/api/reports/1/`        | Delete a report         |

### Example

Create a report:

```http
POST /api/reports/
```

The API creates the report with:

```text
pending
```

Celery processes it:

```text
pending → processing → completed
```

If something goes wrong:

```text
pending → processing → failed
```

---

## 📊 Report States

* `pending` — Waiting to be processed.
* `processing` — Celery worker is generating the report.
* `completed` — Report finished successfully.
* `failed` — Report processing failed.

---

## 🧠 Why Celery + Redis?

**Celery** handles background tasks that should not block the API request.

**Redis** acts as the message broker between Django and the Celery worker.

This pattern is useful for operations such as:

* Report generation
* Sending emails
* Data processing
* File generation
* Scheduled jobs

---

## 🛠️ Tech Stack

* Django
* Django REST Framework
* Celery
* Redis
* SQLite
* Docker
* Python
