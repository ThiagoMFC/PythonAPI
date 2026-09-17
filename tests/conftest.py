#configuration file used to share fixtures, hooks, and plugins across multiple test files without needing to import them explicitly



from fastapi.testclient import TestClient
from app.main import app

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import settings
from app.database import get_db, Base
import pytest
from app.oauth2 import create_access_token
from app import models



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

@pytest.fixture
def test_user2(client):
    user_data = {
        "email": "email@email.com",
        "password": "pass123"
    }
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201
    temp_user = res.json()
    temp_user["password"] = user_data["password"]
    return temp_user
#======================================================= TOKEN CREATION FIXTURE ===========================================================
@pytest.fixture
def test_token(test_user):
    return create_access_token({"user_id": test_user["id"]})


@pytest.fixture
def authorized_client(client, test_token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {test_token}"
    }
    return client

#======================================================== POST CREATION FIXTURE ======================================================
@pytest.fixture
def test_posts(test_user, session, test_user2):
    post_data = [
        {
            "title": "first",
            "content": "1st content",
            "owner_id": test_user["id"]
        },
        {
            "title": "second",
            "content": "second content",
            "owner_id": test_user["id"]
        },
        {
            "title": "3rd",
            "content": "3rd content",
            "owner_id": test_user["id"]
        },
        {
            "title": "4th",
            "content": "4th content",
            "owner_id": test_user2["id"]
        },
    ]

    #convert dicts in list to post models
    def create_post_model(post):
        return models.Post(**post)
    #create map of post models
    post_map = map(create_post_model, post_data)
    #convert map to list
    posts = list(post_map)
    #use list to add posts to db
    session.add_all(posts)
    session.commit()
    posts = session.query(models.Post).all()
    return posts