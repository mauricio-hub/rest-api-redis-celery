# 📊 Asynchronous Reports System

A simple project that implements an asynchronous report generation system with **Django REST Framework**, **Celery**, and **Redis**.

---

## 🎯 What is this?

A system where:
- The user **creates a report** (fast)
- The system puts it in a **queue** (Redis)
- A **worker** (Celery) processes it in the background (non-blocking)
- The user sees the progress in real time

---

## 🏗️ Key Concepts

### **Job**
A task that needs to be processed. In our case: "generate a report"

```json
{
  "id": 1,
  "title": "Sales Report",
  "status": "pending",
  "result": null
}
```

### **Queue**
Place where tasks are stored waiting to be processed. We use **Redis**.