from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base

from src.database.connect import engine

Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    firstname = Column(String, index=True)
    lastname = Column(String, index=True)
    email = Column(String, index=True)
    phone = Column(String, index=True)
    birthday = Column(DateTime, index=True)
    description = Column(String, index=True)


# Base.metadata.create_all(bind=engine)
