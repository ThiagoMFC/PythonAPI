#configuration file used to share fixtures, hooks, and plugins across multiple test files without needing to import them explicitly



from fastapi.testclient import TestClient
from app.main import app

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import settings
from app.database import get_db, Base
import pytest



SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.DB_USER}:{settings.DB_USER_PWD}@{settings.DB_HOST}/{settings.DB_NAME}_test"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#================================================================ DB / SESSION FIXTURES ============================================

@pytest.fixture()
def session():
    #drop test db before tests
    Base.metadata.drop_all(bind=engine)
    #create new test db
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture()
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db

    yield TestClient(app)


#======================================================== USER CREATION FIXTURE ======================================================
@pytest.fixture
def test_user(client):
    user_data = {
        "email": "email123@email.com",
        "password": "pass123"
    }
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201
    temp_user = res.json()
    temp_user["password"] = user_data["password"]
    return temp_user