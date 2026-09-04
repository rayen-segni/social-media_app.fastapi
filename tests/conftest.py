import pytest
from fastapi.testclient import TestClient

from app import models, utils, oauth2
from app.main import app
from app.database import get_db, Base

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config import settings


test_db_name = settings.database_name_test or f"{settings.database_name}_test"

TESTING_SQLALCHEMY_DATABASE_URL = (
    f"postgresql://{settings.database_username}:{settings.database_password}"
    f"@{settings.database_hostname}:{settings.database_port}/"
    f"{test_db_name}"
)

engine = create_engine(
    TESTING_SQLALCHEMY_DATABASE_URL
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="session", autouse=True)
def setup_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def session():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.rollback()
        db.query(models.Vote).delete()
        db.query(models.Post).delete()
        db.query(models.User).delete()
        db.commit()
        db.close()


# 2. Client fixture (plugs the session into FastAPI and CLEANS UP)
@pytest.fixture
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    # Apply the override
    app.dependency_overrides[get_db] = override_get_db

    yield TestClient(app)  # Test runs here

    app.dependency_overrides.clear()


@pytest.fixture
def test_user(session) -> dict:
    user_data = {
        "email": "test_user@gmail.com",
        "password": "password123"
    }
    hashed_password = utils.hash(user_data["password"])
    new_user = models.User(email=user_data["email"], password=hashed_password)

    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    return {
        "id": new_user.id,
        "email": new_user.email,
        "password": user_data["password"]
    }


@pytest.fixture
def test_user2(session) -> dict:
    user_data = {
        "email": "test_user2@gmail.com",
        "password": "password123"
    }
    hashed_password = utils.hash(user_data["password"])
    new_user = models.User(email=user_data["email"], password=hashed_password)

    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    return {
        "id": new_user.id,
        "email": new_user.email,
        "password": user_data["password"]
    }


@pytest.fixture
def token(test_user: dict) -> str:
    return oauth2.create_access_token({"user_id": test_user["id"]})


@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    
    return client


@pytest.fixture
def test_posts(test_user, test_user2, session):
    posts_data = [
        {"title": "1st title", "content": "1st content", "owner_id": test_user["id"]},
        {"title": "2nd title", "content": "2nd content", "owner_id": test_user["id"]},
        {"title": "3rd title", "content": "3rd content", "owner_id": test_user["id"]},
        {"title": "4th title", "content": "4th content", "owner_id": test_user2["id"]},
    ]

    posts = [models.Post(**post) for post in posts_data]
    session.add_all(posts)
    session.commit()

    return session.query(models.Post).all()


