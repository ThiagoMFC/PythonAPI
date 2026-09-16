from fastapi.testclient import TestClient
from app.main import app
from app import schemas

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import settings
from app.database import get_db, Base
import pytest



SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.DB_USER}:{settings.DB_USER_PWD}@{settings.DB_HOST}/{settings.DB_NAME}_test"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db


@pytest.fixture
def client():
    #drop test db before tests
    Base.metadata.drop_all(bind=engine)
    #create new test db
    Base.metadata.create_all(bind=engine)
    yield TestClient(app)

def test_create_user(client):
    res = client.post("/users/", json={
        "email": "email123@email.com",
        "password": "pass123"
    })

    assert res.status_code == 201

    data = schemas.UserResponse(**res.json())
    assert data.email == "email123@email.com"
    assert data.id is not None