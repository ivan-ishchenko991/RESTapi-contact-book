from typing import List

from fastapi import APIRouter, Depends, HTTPException, status, Path, Query
from fastapi_limiter.depends import RateLimiter
from sqlalchemy.orm import Session

from src.database.connect import get_db
from src.database.models import User
from src.schemas import ContactModel, ResponseContact
from src.repository import contacts as repository_contacts
from src.services.auth import auth_service

router = APIRouter(prefix='/contact', tags=['contacts'])


@router.get("/all", response_model=List[ResponseContact])
async def get_contacts(db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    """
    The get_contacts function returns a list of contacts for the current user.

    :param db: Session: Get the database session
    :param current_user: User: Get the current user from the database
    :return: A list of users
    :doc-author: Trelent
    """
    users = await repository_contacts.get_contacts(current_user, db)
    if users is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return users


@router.get("/birthdays", response_model=List[ResponseContact])
            # dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def birthdays(db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    """
    The birthdays function returns a list of users with birthdays in the current week.
        The function is called by sending a GET request to /birthdays.


    :param db: Session: Get the database session
    :param current_user: User: Get the current user from the database
    :return: A list of users with their birthdays in the next week
    :doc-author: Trelent
    """
    users = await repository_contacts.birthdays_per_weak(current_user, db)
    if users is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return users


@router.get("/{contact_id}", response_model=ResponseContact)
async def get_contact(contact_id: int = Path(ge=1), db: Session = Depends(get_db),
                      current_user: User = Depends(auth_service.get_current_user)):
    """
    The get_contact function returns a single contact from the database.
        The function takes an integer as its only argument, which is the ID of the contact to be returned.
        If no such contact exists in the database, then a 404 error is raised.

    :param contact_id: int: Get the contact id from the url
    :param db: Session: Access the database
    :param current_user: User: Get the current user
    :return: A contact object
    :doc-author: Trelent
    """
    user = await repository_contacts.get_contact(contact_id, current_user, db)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return user


@router.get("/search/", response_model=List[ResponseContact])
async def search_contact(value: str = Query(..., description='Searching contact'), db: Session = Depends(get_db),
                         current_user: User = Depends(auth_service.get_current_user)):
    """
    The search_contact function is used to search for a contact in the database.
        The function takes in a string value and returns the user object if found.

    :param value: str: Search for a contact in the database
    :param description: Describe the parameter in the swagger documentation
    :param db: Session: Get the database session
    :param current_user: User: Get the current user
    :return: A list of contacts
    :doc-author: Trelent
    """
    user = await repository_contacts.search_contact(value, current_user, db)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return user


@router.post("/", response_model=ResponseContact, status_code=status.HTTP_201_CREATED)
             # dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def create_contact(body: ContactModel, db: Session = Depends(get_db),
                         current_user: User = Depends(auth_service.get_current_user)):
    """
    The create_contact function creates a new contact in the database.

    :param body: ContactModel: Pass in the contact information to be added
    :param db: Session: Pass the database session to the repository layer
    :param current_user: User: Get the current user
    :return: A contactmodel object
    :doc-author: Trelent
    """
    user = await repository_contacts.create_contact(body, current_user, db)
    return user


@router.put("/{contact_id}", response_model=ResponseContact)
async def update_contact(body: ContactModel, contact_id: int = Path(ge=1), db: Session = Depends(get_db),
                         current_user: User = Depends(auth_service.get_current_user)):
    """
    The update_contact function updates a contact in the database.
        The function takes an id and a body as input, which is then used to update the contact.
        If no user with that id exists, it returns 404 Not Found.

    :param body: ContactModel: Get the data from the request body
    :param contact_id: int: Get the contact id from the url
    :param db: Session: Pass the database connection to the function
    :param current_user: User: Get the user_id from the token
    :return: The user object
    :doc-author: Trelent
    """
    user = await repository_contacts.update_contact(body, contact_id, current_user, db)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return user


@router.delete("/{contact_id}", status_code=status.HTTP_204_NO_CONTENT)
               # dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def remove_contact(contact_id: int = Path(ge=1), db: Session = Depends(get_db),
                         current_user: User = Depends(auth_service.get_current_user)):
    """
    The remove_contact function removes a contact from the database.
        The function takes in an integer representing the id of the contact to be removed,
        and returns a User object with all of its contacts.

    :param contact_id: int: Specify the contact to be removed
    :param db: Session: Get the database session
    :param current_user: User: Get the current user from the database
    :return: A user object
    :doc-author: Trelent
    """
    user = await repository_contacts.remove_contact(contact_id, current_user, db)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return user
