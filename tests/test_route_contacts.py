from unittest.mock import MagicMock, patch

import pytest
from fastapi import Depends
from fastapi_limiter.depends import RateLimiter

from src.database.models import User
from src.services.auth import auth_service


@pytest.fixture()
def access_token(client, user, session, monkeypatch):
    mock_send_email = MagicMock()
    monkeypatch.setattr("src.routes.auth.send_email", mock_send_email)
    response = client.post(
        "/api/auth/signup",
        json=user,
    )
    current_user: User = session.query(User).filter(User.email == user.get('email')).first()
    current_user.confirmed_email = True
    session.commit()
    response = client.post(
        "/api/auth/login",
        data={"username": user.get('email'), "password": user.get('password')},
    )
    assert response.status_code == 200, response.text
    data = response.json()
    return data["access_token"]


def test_create_contact(client, access_token, monkeypatch):
    with patch.object(auth_service, 'r') as r_mock:
        r_mock.get.return_value = None
        response = client.post(
            "/api/contact",
            json={
                "firstname": "Petro",
                "lastname": "Galitskiy",
                "email": "test_contact@gmail.com",
                "phone": "+380666666666",
                "birthday": "2000-10-30",
                "description": "Developer"
            },
            headers={"Authorization": f"Bearer {access_token}"}
        )
        assert response.status_code == 201, response.text
        data = response.json()
        assert data["email"] == "test_contact@gmail.com"
        assert "id" in data


def test_get_contacts(client, access_token):
    with patch.object(auth_service, 'r') as r_mock:
        r_mock.get.return_value = None
        response = client.get(
            "/api/contact/all",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        assert response.status_code == 200, response.text
        data = response.json()
        print(data)
        assert data[0]["email"] == "test_contact@gmail.com"
        assert "id" in data[0]


def test_get_contact(client, access_token):
    with patch.object(auth_service, 'r') as r_mock:
        r_mock.get.return_value = None
        response = client.get(
            "/api/contact/1",
            headers={"Authorization": f"Bearer {access_token}"}
        )
        assert response.status_code == 200, response.text
        data = response.json()
        assert data["email"] == "test_contact@gmail.com"
        assert "id" in data


def test_get_contact_not_found(client, access_token):
    with patch.object(auth_service, 'r') as r_mock:
        r_mock.get.return_value = None
        response = client.get(
            "/api/contact/2",
            headers={"Authorization": f"Bearer {access_token}"}
        )
        assert response.status_code == 404, response.text
        data = response.json()
        assert data["detail"] == "Not Found"


def test_birthdays(client, access_token):
    with patch.object(auth_service, 'r') as r_mock:
        r_mock.get.return_value = None
        response = client.get(
            "/api/contact/birthdays",
            headers={"Authorization": f"Bearer {access_token}"}
        )
        assert response.status_code == 200, response.text
        data = response.json()
        assert data[0]["email"] == "test_contact@gmail.com"
        assert "id" in data[0]


def test_search_contact(client, access_token):
    with patch.object(auth_service, 'r') as r_mock:
        r_mock.get.return_value = None
        response = client.get(
            "/api/contact/search/?value=Petro",
            headers={"Authorization": f"Bearer {access_token}"}
        )
        assert response.status_code == 200, response.text
        data = response.json()
        assert data[0]["email"] == "test_contact@gmail.com"
        assert "id" in data[0]


def test_search_contact_not_found(client, access_token):
    with patch.object(auth_service, 'r') as r_mock:
        r_mock.get.return_value = None
        response = client.get(
            "/api/contact/search/?value=Vasya",
            headers={"Authorization": f"Bearer {access_token}"}
        )
        data = response.json()
        assert data == []


def test_update_contact(client, access_token):
    with patch.object(auth_service, 'r') as r_mock:
        r_mock.get.return_value = None
        response = client.put(
            "/api/contact/1",
            json={
                "firstname": "Petro",
                "lastname": "Galitskiy",
                "email": "test_contact@gmail.com",
                "phone": "+380999999999",
                "birthday": "2000-10-30",
                "description": "tester"
            },
            headers={"Authorization": f"Bearer {access_token}"}
        )
        assert response.status_code == 200, response.text
        data = response.json()
        assert data["phone"] == "+380999999999"
        assert "id" in data


def test_update_contact_not_found(client, access_token):
    with patch.object(auth_service, 'r') as r_mock:
        r_mock.get.return_value = None
        response = client.get(
            "/api/contact/2",
            headers={"Authorization": f"Bearer {access_token}"}
        )
        assert response.status_code == 404, response.text
        data = response.json()
        assert data["detail"] == "Not Found"


def test_remove_contact(client, access_token):
    with patch.object(auth_service, 'r') as r_mock:
        r_mock.get.return_value = None
        response = client.delete(
            "/api/contact/1",
            headers={"Authorization": f"Bearer {access_token}"}
        )
        assert response.status_code == 204, response.text


def test_remove_contact_not_found(client, access_token):
    with patch.object(auth_service, 'r') as r_mock:
        r_mock.get.return_value = None
        response = client.delete(
            "/api/contact/1",
            headers={"Authorization": f"Bearer {access_token}"}
        )
        assert response.status_code == 404, response.text
        data = response.json()
        assert data["detail"] == "Not Found"


def test_get_contacts_not_found(client, access_token):
    with patch.object(auth_service, 'r') as r_mock:
        r_mock.get.return_value = None
        response = client.get(
            "/api/contact/all",
            headers={"Authorization": f"Bearer {access_token}"}
        )
        data = response.json()
        assert data == []


def test_birthdays_not_found(client, access_token):
    with patch.object(auth_service, 'r') as r_mock:
        r_mock.get.return_value = None
        response = client.get(
            "/api/contact/birthdays",
            headers={"Authorization": f"Bearer {access_token}"}
        )
        data = response.json()
        assert data == []
