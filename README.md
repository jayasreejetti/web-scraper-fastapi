# GitHub Users API

A FastAPI application that scrapes GitHub users and exposes CRUD operations.

## Project Overview
This project fetches 1000 GitHub users via the GitHub API, stores them in a SQLite database, and exposes them through a RESTful FastAPI application.

## Tech Stack
- Python 3.11
- FastAPI
- SQLAlchemy
- SQLite
- Requests
- Pydantic
- python-dotenv

## Setup Instructions

### 1. Clone the repository
```bash
git clone <your-repo-url>
cd web_scraper_fastapi
```

### 2. Create virtual environment
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Configuration
Create a `.env` file in root folder: