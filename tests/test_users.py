import pytest
from fastapi import status
from jose import jwt

from app import schemas
from app.config import settings


def test_create_user(client):
    email = "new_user@gmail.com"
    res = client.post(
        "/user/",
        json={
            "email": email,
            "password": "securepassword123"
        }
    )
    
    assert res.status_code == status.HTTP_201_CREATED
    new_user = schemas.UserOut(**res.json())
    assert new_user.email == email


def test_login(client, test_user):

    res = client.post(
        "/login",
        data={
            "username": test_user["email"],
            "password": test_user["password"]
        }
    )

    token_data = schemas.Token(**res.json())
    
    payload = jwt.decode(
        token_data.access_token, settings.secret_key, settings.algorithm)
    idt = payload.get("user_id")
    
    assert idt == test_user["id"]
    assert token_data.token_type == "bearer"
    assert res.status_code == status.HTTP_200_OK


@pytest.mark.parametrize(["email", "password", "status_code"],[
    ("wrong_email@gmail.com", "password123", status.HTTP_403_FORBIDDEN),
    ("test_user@gmail.com", "wrong_password", status.HTTP_403_FORBIDDEN),
    (None, "wrong_password", status.HTTP_422_UNPROCESSABLE_CONTENT),
    ("wrong_email@gmail.com", None, status.HTTP_422_UNPROCESSABLE_CONTENT)
])
def test_incorrect_login(test_user, client, email, password, status_code):
    res = client.post(
        "/login",
        data={
            "username": email,
            "password": password
        }
    )
    
    assert res.status_code == status_code
