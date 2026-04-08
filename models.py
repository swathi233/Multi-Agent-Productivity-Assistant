from sqlalchemy import Column, Integer, String, ForeignKey
from db import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    password = Column(String)

class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))

class Note(Base):
    __tablename__ = "notes"
    id = Column(Integer, primary_key=True)
    content = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))

class Birthday(Base):
    __tablename__ = "birthdays"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    date = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))

class Meeting(Base):
    __tablename__ = "meetings"
    id = Column(Integer, primary_key=True)
    email = Column(String)
    subject = Column(String)
    description = Column(String)
    date = Column(String)
    time = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))