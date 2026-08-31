from pydantic import BaseModel
from datetime import datetime

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
    #ignore reposponse is not a dict and convert sqlalchemy model to pydantic model
    class Config: orm_mode = True