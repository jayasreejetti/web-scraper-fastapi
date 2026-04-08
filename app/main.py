from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import engine, SessionLocal
from app.schemas import UserCreate, UserUpdate, UserResponse
from typing import Optional, List
import app.models as models
import app.crud as crud
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="GitHub Users API")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def home():
    return {"message": "GitHub Users API is working!"}

# GET all users
@app.get("/items", response_model=List[UserResponse])
def get_all_users(limit: int = 100, offset: int = 0, db: Session = Depends(get_db)):
    logger.info(f"Fetching all users")
    return crud.get_all_users(db, limit=limit, offset=offset)

# FILTER — must be before /items/{id}
@app.get("/items/filter", response_model=List[UserResponse])
def filter_users(login: Optional[str] = None, db: Session = Depends(get_db)):
    logger.info(f"Filtering by login={login}")
    return crud.filter_users(db, login=login)

# GET by ID
@app.get("/items/{id}", response_model=UserResponse)
def get_user(id: int, db: Session = Depends(get_db)):
    user = crud.get_user_by_id(db, id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# CREATE
@app.post("/items", response_model=UserResponse, status_code=201)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    new_user = crud.create_user(db, user)
    if not new_user:
        raise HTTPException(status_code=400, detail="User already exists")
    return new_user

# UPDATE
@app.put("/items/{id}", response_model=UserResponse)
def update_user(id: int, user: UserUpdate, db: Session = Depends(get_db)):
    updated = crud.update_user(db, id, user)
    if not updated:
        raise HTTPException(status_code=404, detail="User not found")
    return updated

# DELETE
@app.delete("/items/{id}")
def delete_user(id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_user(db, id)
    if not deleted:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": f"User {id} deleted successfully"}