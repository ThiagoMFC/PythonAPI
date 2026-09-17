from app import schemas
#from .database import client, session
import pytest
from app.config import settings
from jose import JWTError, jwt

#define order of testing 
pytestmark = pytest.mark.order(2)

#create user for tests




def test_login_user(client, test_user):
    res = client.post("/login", data={
        "username": test_user["email"],
        "password": test_user["password"]
    })
    assert res.status_code == 200
    #check access_token
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(login_res.access_token, settings.SECRET_KEY, algorithms=settings.ALGORITHM)
    user_id = str(payload.get("user_id"))
    assert int(user_id) == test_user["id"]

@pytest.mark.parametrize("email, password, status_code", [
    (None, "badpassword", 422),
    ("john@email.com", None, 422),
    ("wrongemail@email.com", "pass123", 403),
    ("email123@email.com", "badpassword", 403)
])
def test_incorrect_user(client, email, password, status_code):
    res = client.post("/login", data={
        "username": email,
        "password": password})
    assert res.status_code == status_code

