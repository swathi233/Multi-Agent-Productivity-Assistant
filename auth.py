from db import SessionLocal
from models import User
import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register(username, password):
    db = SessionLocal()

    existing_user = db.query(User).filter_by(username=username).first()
    if existing_user:
        db.close()
        return None  # username already exists

    user = User(username=username, password=hash_password(password))
    db.add(user)
    db.commit()
    db.refresh(user)
    db.close()
    return user

def login(username, password):
    db = SessionLocal()
    user = db.query(User).filter_by(
        username=username,
        password=hash_password(password)
    ).first()
    db.close()
    return user