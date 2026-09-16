from app import schemas
#from .database import client, session
import pytest
#define order of testing 
pytestmark = pytest.mark.order(1)    

def test_create_user(client):
    res = client.post("/users/", json={
        "email": "email123@email.com",
        "password": "pass123"
    })

    assert res.status_code == 201

    data = schemas.UserResponse(**res.json())
    assert data.email == "email123@email.com"
    assert data.id is not None

