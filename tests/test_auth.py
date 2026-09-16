from app import schemas
from .database import client, session
import pytest
#define order of testing 
pytestmark = pytest.mark.order(2)

#create user for tests
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



def test_login_user(client, test_user):
    res = client.post("/login", data={
        "username": test_user["email"],
        "password": test_user["password"]
    })

    assert res.status_code == 200