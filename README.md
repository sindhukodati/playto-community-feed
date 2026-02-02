# Playto Community Feed

A backend prototype for a community feed system built as part of the **Playto Engineering Challenge**.

This project demonstrates efficient handling of:
- Threaded (nested) comments
- Likes with concurrency safety
- Karma-based gamification
- Dynamic leaderboard (last 24 hours only)
- Optimized database queries (no N+1 problem)

---

## 🚀 Tech Stack

- **Backend:** Django, Django REST Framework
- **Database:** SQLite
- **Language:** Python 3.11
- **Auth:** Django built-in User model

---

## ✨ Features

- Create and list posts
- Like posts and comments (no double-like allowed)
- Nested comments (Reddit-style threads)
- Karma system:
  - Post like → +5 karma
  - Comment like → +1 karma
- Leaderboard showing **Top 5 users in last 24 hours**
- Optimized queries using `select_related`, `prefetch_related`, and aggregation

---


## 📂 Project Structure

```text
playto-community-feed/
│
├── playto_backend/
│   ├── core/
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   └── services/
│   │       └── leaderboard.py
│   │
│   ├── playto_backend/
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   │
│   └── manage.py
│
├── requirements.txt
└── README.md
```
---

## ⚙️ Setup Instructions (Local)

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```
Server will start at:
```bash
http://127.0.0.1:8000/

```
## 🔗 API Endpoints

| Endpoint | Method | Description |
|--------|--------|-------------|
| `/api/` | GET | API health check |
| `/api/posts/` | GET, POST | Create & list posts |
| `/api/feed/` | GET | Feed with like counts |
| `/api/leaderboard/` | GET | Top 5 users (last 24h) |

---

## 🧠 Key Engineering Decisions

- **Nested comments:** Implemented using a self-referencing foreign key on the `Comment` model  
- **No N+1 queries:** Batched fetching and in-memory tree construction  
- **Concurrency safety:** Database-level unique constraints prevent double likes  
- **Leaderboard:** Calculated dynamically from karma transaction history (no cached totals)

---

## 👩‍💻 Author

**Sindhu Kodati**
