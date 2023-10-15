from typing import List

from fastapi import APIRouter, Depends, HTTPException, status, Path, Query
from sqlalchemy.orm import Session

from src.database.connect import get_db
from src.database.models import User
from src.schemas import ContactModel, ResponseContact
from src.repository import contacts as repository_contacts
from src.services.auth import auth_service

router = APIRouter(prefix='/contact', tags=['contacts'])


@router.get("/", response_model=List[ResponseContact])
async def get_contacts(db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    users = await repository_contacts.get_contacts(current_user, db)
    return users


@router.get("/birthdays", response_model=List[ResponseContact], )
async def birthdays(db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    users = await repository_contacts.birthdays_per_weak(current_user, db)
    if users is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return users


@router.get("/{contact_id}", response_model=ResponseContact)
async def get_contact(contact_id: int = Path(ge=1), db: Session = Depends(get_db),
                      current_user: User = Depends(auth_service.get_current_user)):
    user = await repository_contacts.get_contact(contact_id, current_user, db)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return user


@router.get("/search/", response_model=List[ResponseContact])
async def search_contact(value: str = Query(..., description='Searching contact'), db: Session = Depends(get_db),
                         current_user: User = Depends(auth_service.get_current_user)):
    user = await repository_contacts.search_contact(value, current_user, db)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return user


@router.post("/", response_model=ResponseContact, status_code=status.HTTP_201_CREATED)
async def create_contact(body: ContactModel, db: Session = Depends(get_db),
                         current_user: User = Depends(auth_service.get_current_user)):
    user = await repository_contacts.create_contact(body, current_user, db)
    return user


@router.put("/{contact_id}", response_model=ResponseContact)
async def update_contact(body: ContactModel, contact_id: int = Path(ge=1), db: Session = Depends(get_db),
                         current_user: User = Depends(auth_service.get_current_user)):
    user = await repository_contacts.update_contact(body, contact_id, current_user, db)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return user


@router.delete("/{contact_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_contact(contact_id: int = Path(ge=1), db: Session = Depends(get_db),
                         current_user: User = Depends(auth_service.get_current_user)):
    user = await repository_contacts.remove_contact(contact_id, current_user, db)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return user
