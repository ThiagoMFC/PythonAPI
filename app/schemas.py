from pydantic import BaseModel
from typing import Optional

#define what the request shuould look like
class PostBase(BaseModel):
    title: str
    content: str
    published: Optional[bool] = True

class PostCreate(PostBase):
    pass
