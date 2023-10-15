from datetime import datetime

from sqlalchemy import or_, and_
from sqlalchemy.orm import Session

from src.database.models import Contact, User
from src.schemas import ContactModel


async def get_contacts(user: User, db: Session):
    contact = db.query(Contact).filter(Contact.user_id == user.id).all()
    return contact


async def birthdays_per_weak(user: User, db: Session):
    contacts = db.query(Contact).filter(Contact.user_id == user.id).all()
    today = datetime.now()
    result = list()
    for contact in contacts:
        birthday = contact.birthday.replace(year=today.year)
        diff = birthday - today
        if 8 > diff.days >= 0:
            result.append(contact)
    return result


async def get_contact(contact_id: int, user: User, db: Session):
    contact = db.query(Contact).filter(and_(Contact.id == contact_id, Contact.user_id == user.id)).first()
    return contact


async def search_contact(value: str, user: User, db: Session):
    contact = db.query(Contact).filter(
        and_(Contact.user_id == user.id,
             or_(Contact.firstname == str(value), Contact.lastname == str(value), Contact.email == str(value)))
    ).all()
    return contact


async def create_contact(body: ContactModel, user: User, db: Session):
    contact = Contact(firstname=body.firstname, lastname=body.lastname, email=body.email, phone=body.phone,
                      birthday=body.birthday, description=body.description, user_id=user.id)
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


async def update_contact(body: ContactModel, contact_id: int, user: User, db: Session):
    contact = db.query(Contact).filter_by(id=contact_id).first()
    if contact:
        contact.firstname = body.firstname
        contact.lastname = body.lastname
        contact.email = body.email
        contact.phone = body.phone
        contact.birthday = body.birthday
        contact.description = body.description
        db.commit()
    return contact


async def remove_contact(contact_id: int, user: User, db: Session):
    contact = db.query(Contact).filter(and_(Contact.id == contact_id, Contact.user_id == user.id)).first()
    if contact:
        db.delete(contact)
        db.commit()
    return contact
