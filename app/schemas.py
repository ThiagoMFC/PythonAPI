from pydantic import BaseModel, ConfigDict, EmailStr
from datetime import datetime
from typing import Optional

#define what the request shuould look like
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass


#define reponse
class PostResponse(PostBase):
    #inherits title, title, published from PostBase
    id: int
    created_at: datetime
    owner_id: int
    #ignore reposponse is not a dict and convert sqlalchemy model to pydantic model
    model_config = ConfigDict(from_attributes=True)

#define what create user request should look like
class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    model_config = ConfigDict(from_attributes=True)


class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None
