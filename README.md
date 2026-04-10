# GitHub Users API

A complete backend application that scrapes GitHub users and exposes CRUD operations via FastAPI.

## Project Overview
This project:
- Fetches 1000 GitHub users via GitHub REST API (100 pages × 10 users)
- Stores data in SQLite database using SQLAlchemy ORM
- Exposes full CRUD operations through a FastAPI REST API
- Includes pagination, filtering, validation, logging, and error handling

## Project Structure
## 📁 Project Structure

```
web_scraper_fastapi/
│
├── app/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── crud.py
│   ├── scraper.py
│   └── config.py
│
├── data/
│   ├── users.json
│   └── users.db
│
├── .env
├── .gitignore
├── pyproject.toml
├── requirements.txt
└── README.md
```



## Tech Stack
- **Python 3.11**
- **FastAPI** — REST API framework
- **SQLAlchemy** — ORM for database interaction
- **SQLite** — Lightweight database
- **Pydantic** — Data validation
- **Requests** — HTTP calls to GitHub API
- **Poetry** — Package management
- **python-dotenv** — Environment variable loading

## Setup Instructions

### Requirements
- Python 3.10+
- Git

### 1. Clone the repository
```bash
git clone https://github.com/jayasreejetti/web-scraper-fastapi.git
cd web-scraper-fastapi
```

### 2. Create virtual environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### 3. Install dependencies

Using pip:
```bash
pip install -r requirements.txt
```

Using Poetry:
```bash
pip install poetry
poetry install
```

### 4. Environment Configuration
Create a `.env` file in root folder:

GITHUB_TOKEN=your_github_token_here
DATABASE_URL=sqlite:///./data/users.db
Get GitHub token from:
`GitHub → Settings → Developer Settings → Personal Access Tokens → Tokens Classic`

## Running the Project

### Step 1: Run the scraper
```bash
python app/scraper.py
```
This will:
- Fetch 1000 users from GitHub API
- Save to `data/users.json`
- Insert into `data/users.db`

### Step 2: Start the FastAPI server
```bash
uvicorn app.main:app --reload
```

### Step 3: Access API docs

http://127.0.0.1:8000/docs

## Database Setup
SQLite database is automatically created at `data/users.db` when server starts. Tables are created automatically via SQLAlchemy.

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Health check |
| GET | `/items` | Get all users (with pagination) |
| GET | `/items/filter?login=abc` | Filter users by login |
| GET | `/items/{id}` | Get single user by ID |
| POST | `/items` | Create new user |
| PUT | `/items/{id}` | Update existing user |
| DELETE | `/items/{id}` | Delete user |

## API Examples

### Get all users
```bash
curl http://127.0.0.1:8000/items
```

### Get all users with pagination
```bash
curl http://127.0.0.1:8000/items?limit=10&offset=0
```

### Get user by ID
```bash
curl http://127.0.0.1:8000/items/1
```

### Filter users by login
```bash
curl http://127.0.0.1:8000/items/filter?login=john
```

### Create new user
```bash
curl -X POST http://127.0.0.1:8000/items \
  -H "Content-Type: application/json" \
  -d '{"login": "testuser", "url": "https://github.com/testuser"}'
```

### Update user
```bash
curl -X PUT http://127.0.0.1:8000/items/1 \
  -H "Content-Type: application/json" \
  -d '{"login": "updated_user"}'
```

### Delete user
```bash
curl -X DELETE http://127.0.0.1:8000/items/1
```

## HTTP Status Codes

| Code | Meaning |
|------|---------|
| 200 | Success |
| 201 | Created |
| 400 | Bad Request |
| 404 | Not Found |
| 500 | Internal Server Error |

## Features
- ✅ Modular project structure
- ✅ Pagination support
- ✅ Duplicate prevention
- ✅ Rate limit handling
- ✅ Retry logic for failed requests
- ✅ Request logging
- ✅ Input validation via Pydantic
- ✅ Auto-generated Swagger docs
