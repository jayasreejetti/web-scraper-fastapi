from sqlalchemy.orm import Session
from app.models import User
from app.schemas import UserCreate, UserUpdate
import logging

logger = logging.getLogger(__name__)

def get_all_users(db: Session, limit: int = 100, offset: int = 0):
    return db.query(User).offset(offset).limit(limit).all()

def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def filter_users(db: Session, login: str = None):
    query = db.query(User)
    if login:
        query = query.filter(User.login.contains(login))
    return query.all()

def create_user(db: Session, user: UserCreate):
    existing = db.query(User).filter(User.login == user.login).first()
    if existing:
        return None
    new_user = User(
        id=user.id,
        login=user.login,
        url=user.url
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def update_user(db: Session, user_id: int, user_data: UserUpdate):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return None
    if user_data.login:
        user.login = user_data.login
    if user_data.url:
        user.url = user_data.url
    db.commit()
    db.refresh(user)
    return user

def delete_user(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return None
    db.delete(user)
    db.commit()
    return user