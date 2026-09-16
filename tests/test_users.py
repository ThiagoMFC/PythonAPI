from fastapi.testclient import TestClient
from app.main import app
from app import schemas

client = TestClient(app)

def test_create_user():
    res = client.post("/users/", json={
        "email": "email123@email.com",
        "password": "pass123"
    })

    assert res.status_code == 201

    data = schemas.UserResponse(**res.json())
    assert data.email == "email123@email.com"
    assert data.id is not None