import unittest
from unittest.mock import MagicMock

from sqlalchemy.orm import Session

from src.database.models import Contact, User
from src.schemas import ContactModel, ResponseContact
from src.repository.contacts import (
    get_contacts,
    get_contact,
    create_contact,
    remove_contact,
    update_contact,
)


class TestContacts(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.session = MagicMock(spec=Session)
        self.user = User(id=1)

    async def test_get_contacts(self):
        contacts = [Contact(), Contact(), Contact()]
        self.session.query().filter().all.return_value = contacts
        result = await get_contacts(user=self.user, db=self.session)
        self.assertEqual(result, contacts)

    async def test_get_contact_found(self):
        contact = Contact()
        self.session.query().filter().first.return_value = contact
        result = await get_contact(contact_id=1, user=self.user, db=self.session)
        self.assertEqual(result, contact)

    async def test_get_contact_not_found(self):
        self.session.query().filter().first.return_value = None
        result = await get_contact(contact_id=1, user=self.user, db=self.session)
        self.assertIsNone(result)

    async def test_create_contact(self):
        body = ContactModel(
            firstname="Oleg",
            lastname="Bikov",
            email='bikov@example.com',
            phone='+380994563456',
            birthday='2020-12-13',
            description='Python developer'
        )
        result = await create_contact(body=body, user=self.user, db=self.session)
        self.assertEqual(result.firstname, body.firstname)
        self.assertEqual(result.lastname, body.lastname)
        self.assertEqual(result.email, body.email)
        self.assertEqual(result.phone, body.phone)
        self.assertEqual(result.birthday, body.birthday)
        self.assertEqual(result.description, body.description)
        self.assertTrue(hasattr(result, "id"))

    async def test_remove_contact_found(self):
        contact = Contact()
        self.session.query().filter().first.return_value = contact
        result = await remove_contact(contact_id=1, user=self.user, db=self.session)
        self.assertEqual(result, contact)

    async def test_remove_contact_not_found(self):
        self.session.query().filter().first.return_value = None
        result = await remove_contact(contact_id=1, user=self.user, db=self.session)
        self.assertIsNone(result)

    async def test_update_contact_found(self):
        body = ContactModel(
            firstname="Oleg",
            lastname="Bikov",
            email='bikov@example.com',
            phone='+380994563456',
            birthday='2020-12-13',
            description='Python developer'
        )
        contact = Contact(
            firstname="Oleg",
            lastname="Bikov",
            email='oleg.lalala@example.com',
            phone='+380994563456',
            birthday='2020-12-13',
            description='Python developer, backend developer'
        )
        self.session.query().filter_by().first.return_value = contact
        self.session.commit.return_value = None
        result = await update_contact(body=body, contact_id=contact.id, user=self.user, db=self.session)
        self.assertEqual(result, contact)

    async def test_update_contact_not_found(self):
        body = ContactModel(
            firstname="Oleg",
            lastname="Bikov",
            email='bikov@example.com',
            phone='+380994563456',
            birthday='2020-12-13',
            description='Python developer'
        )
        self.session.query().filter_by().first.return_value = None
        self.session.commit.return_value = None
        result = await update_contact(body=body, contact_id=1, user=self.user, db=self.session)
        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()
