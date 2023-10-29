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


def test_read_users_me(client, access_token, monkeypatch):
    with patch.object(auth_service, 'r') as r_mock:
        r_mock.get.return_value = None
        response = client.get(
            "/api/users/me/",
            headers={"Authorization": f"Bearer {access_token}"}
        )
        assert response.status_code == 200, response.text
        data = response.json()
        assert data["email"] == "deadpool@example.com"
        assert "id" in data


# def test_update_avatar_user(client, access_token, monkeypatch):
#     mock_file = MagicMock()
#     monkeypatch.setattr("src.routes.users.File", mock_file)
#     mock_cloudinary = MagicMock()
#     monkeypatch.setattr("src.routes.users.cloudinary", mock_cloudinary)
#     with patch.object(auth_service, 'r') as r_mock:
#         r_mock.get.return_value = None
#         response = client.patch(
#             "/api/users/avatar",
#             json=,
#             headers={"Authorization": f"Bearer {access_token}"}
#         )
#         # assert response.status_code == 200, response.text
#         data = response.json()
#         print(data)
#         assert data["email"] == "deadpool@example.com"
#         assert "id" in data
