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

