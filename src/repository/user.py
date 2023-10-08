from datetime import datetime

from sqlalchemy import or_
from sqlalchemy.orm import Session

from src.database.models import User
from src.schemas import UserModel


async def get_users(db: Session):
    user = db.query(User).all()
    return user


async def birthdays_per_weak(db: Session):
    users = db.query(User).all()
    today = datetime.now()
    result = list()
    for user in users:
        birthday = user.birthday.replace(year=today.year)
        diff = birthday - today
        if 8 > diff.days >= 0:
            result.append(user)
    return result


async def get_user(user_id: int, db: Session):
    user = db.query(User).filter_by(id=user_id).first()
    return user


async def search_user(value: str, db: Session):
    user = db.query(User).filter(
        or_(User.firstname == str(value), User.lastname == str(value), User.email == str(value))).all()
    return user


async def create_user(body: UserModel, db: Session):
    user = User(firstname=body.firstname, lastname=body.lastname, email=body.email, phone=body.phone,
                birthday=body.birthday, description=body.description)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


async def update_user(body: UserModel, user_id: int, db: Session):
    user = db.query(User).filter_by(id=user_id).first()
    if user:
        user.firstname = body.firstname
        user.lastname = body.lastname
        user.email = body.email
        user.phone = body.phone
        user.birthday = body.birthday
        user.description = body.description
        db.commit()
    return user


async def remove_user(user_id: int, db: Session):
    user = db.query(User).filter_by(id=user_id).first()
    if user:
        db.delete(user)
        db.commit()
    return user
