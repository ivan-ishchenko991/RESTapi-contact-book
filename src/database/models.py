from sqlalchemy import Column, Integer, String, DateTime, func, ForeignKey, Boolean
from sqlalchemy.orm import declarative_base, relationship

from src.database.connect import engine

Base = declarative_base()


class Contact(Base):
    __tablename__ = "contacts"
    id = Column(Integer, primary_key=True, index=True)
    firstname = Column(String, index=True)
    lastname = Column(String, index=True)
    email = Column(String, index=True)
    phone = Column(String, index=True)
    birthday = Column(DateTime, index=True)
    description = Column(String, index=True)
    user_id = Column('user_id', ForeignKey('users.id', ondelete='CASCADE'), default=None)
    user = relationship('User', backref="contacts")


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(50))
    email = Column(String(250), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    created_at = Column('crated_at', DateTime, default=func.now())
    avatar = Column(String(255), nullable=True)
    refresh_token = Column(String(255), nullable=True)
    confirmed_email = Column(Boolean, default=False)


# Base.metadata.create_all(bind=engine)
