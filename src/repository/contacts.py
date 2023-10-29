from datetime import datetime

from sqlalchemy import or_, and_
from sqlalchemy.orm import Session

from src.database.models import Contact, User
from src.schemas import ContactModel


async def get_contacts(user: User, db: Session):
    """
    The get_contacts function returns a list of contacts for the user.
        Args:
            user (User): The User object to get contacts from.
            db (Session): A database session to use when querying the database.

    :param user: User: Get the user id of the current logged in user
    :param db: Session: Pass the database session to the function
    :return: A list of contacts
    :doc-author: Trelent
    """
    contacts = db.query(Contact).filter(Contact.user_id == user.id).all()
    return contacts


async def birthdays_per_weak(user: User, db: Session):
    """
    The birthdays_per_weak function returns a list of contacts that have their birthday in the next 7 days.
        Args:
            user (User): The user whose contacts are being queried.
            db (Session): A database session to query from.

    :param user: User: Get the user id from the database
    :param db: Session: Pass the database session to the function
    :return: A list of contacts with their birthday in the next week
    :doc-author: Trelent
    """
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
    """
    The get_contact function takes in a contact_id and user, and returns the contact with that id.
        Args:
            contact_id (int): The id of the desired Contact object.
            user (User): The User object associated with this request.

    :param contact_id: int: Find the contact in the database
    :param user: User: Get the user_id from the database
    :param db: Session: Pass in the database session
    :return: A contact object
    :doc-author: Trelent
    """
    contact = db.query(Contact).filter(and_(Contact.id == contact_id, Contact.user_id == user.id)).first()
    return contact


async def search_contact(value: str, user: User, db: Session):
    """
    The search_contact function searches for a contact in the database.
        Args:
            value (str): The search term to look for.
            user (User): The user who is searching for the contact.

    :param value: str: Search for a contact by firstname, lastname or email
    :param user: User: Get the user id from the user object
    :param db: Session: Pass the database session to the function
    :return: A list of contacts
    :doc-author: Trelent
    """
    contact = db.query(Contact).filter(
        and_(Contact.user_id == user.id,
             or_(Contact.firstname == str(value), Contact.lastname == str(value), Contact.email == str(value)))
    ).all()
    return contact


async def create_contact(body: ContactModel, user: User, db: Session):
    """
    The create_contact function creates a new contact in the database.
        Args:
            body (ContactModel): The contact to create.
            user (User): The current user, who is creating the contact.

    :param body: ContactModel: Pass the contact data to the function
    :param user: User: Get the user id of the logged in user
    :param db: Session: Access the database
    :return: The contact object that was created
    :doc-author: Trelent
    """
    contact = Contact(firstname=body.firstname, lastname=body.lastname, email=body.email, phone=body.phone,
                      birthday=body.birthday, description=body.description, user_id=user.id)
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


async def update_contact(body: ContactModel, contact_id: int, user: User, db: Session):
    """
    The update_contact function updates a contact in the database.
        Args:
            body (ContactModel): The updated contact information.
            contact_id (int): The id of the contact to update.
            user (User): The current logged-in user, used for authorization purposes.

    :param body: ContactModel: Pass the contact information that is being updated
    :param contact_id: int: Identify which contact to update
    :param user: User: Check if the user is logged in
    :param db: Session: Access the database
    :return: The updated contact
    :doc-author: Trelent
    """
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
    """
    The remove_contact function removes a contact from the database. Args: contact_id (int): The id of the contact to
    be removed. user (User): The user who is removing the contact. This is used to ensure that only contacts
    belonging to this user are deleted, and not contacts belonging to other users with similar IDs.

    :param contact_id: int: Specify the contact to be removed
    :param user: User: Identify the user that is logged in
    :param db: Session: Pass the database session to the function
    :return: The contact that was deleted
    :doc-author: Trelent
    """
    contact = db.query(Contact).filter(and_(Contact.id == contact_id, Contact.user_id == user.id)).first()
    if contact:
        db.delete(contact)
        db.commit()
    return contact
