import unittest
from unittest.mock import MagicMock

from sqlalchemy.orm import Session

from src.database.models import User
from src.schemas import UserModel
from src.repository.users import (
    get_user_by_email,
    create_user,
    update_token,
    confirmed_email,
    update_avatar,
)


class TestUsers(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.session = MagicMock(spec=Session)
        self.user = User(id=1)

    async def test_get_user_by_email(self):
        user = User()
        self.session.query().filter().first.return_value = user
        result = await get_user_by_email(email="deadpool@example.com", db=self.session)
        self.assertEqual(result, user)

    async def test_get_user_by_email_not_found(self):
        self.session.query().filter().first.return_value = None
        result = await get_user_by_email(email="deadpool@example.com", db=self.session)
        self.assertIsNone(result)

    async def test_create_user(self):  #error!!!
        # mock_gravatar = MagicMock()
        # monkeypatch.setattr("src.repository.users.Gravatar", mock_gravatar)
        user = UserModel(
            username="deadpool",
            email="deadpool@example.com",
            password="123456789"
        )
        self.session.commit.return_value = None
        result = await create_user(body=user, db=self.session)
        self.assertEqual(result.username, user.username)
        self.assertEqual(result.email, user.email)
        self.assertEqual(result.password, user.password)
        self.assertTrue(hasattr(result, "id"))

    async def test_update_token(self):
        user = User()
        test_token = "fhbvoqur0g8q738qvyb38vb834bv"
        self.session.query().filter().first.return_value = user
        self.session.commit.return_value = None
        await update_token(user=user, token=test_token, db=self.session)
        new_user = self.session.query().filter().first.return_value
        self.assertEqual(new_user.refresh_token, test_token)

    async def test_confirmed_email(self):
        user = User()
        self.session.query().filter().first.return_value = user
        self.session.commit.return_value = None
        await confirmed_email(email=user.email, db=self.session)
        new_user = self.session.query().filter().first.return_value
        self.assertTrue(new_user.confirmed_email)

    async def test_update_avatar(self):
        user = User()
        test_url = "test/avatar/v1/picture.jpg"
        self.session.query().filter().first.return_value = user
        self.session.commit.return_value = None
        result = await update_avatar(email=user.email, url=test_url, db=self.session)
        new_user = self.session.query().filter().first.return_value
        self.assertEqual(result.avatar, test_url)


if __name__ == '__main__':
    unittest.main()
