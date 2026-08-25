from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional

#create instance of FastAPI named app
app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: Optional[bool] = True

#hardcode some posts for testing purposes
my_posts = [{"title": "title of post 1", "content": "content of post 1", "published": True, "id": 1},
             {"title": "title of post 2", "content": "content of post 2", "published": True, "id": 2}]

#define a path GET operation (route/endpoint) decorator
@app.get("/")
def root():
    return {"message": "hello"}

@app.get("/posts")
def get_posts():
    return {"data": my_posts}

@app.post("/posts")
def create_posts(new_post: Post):
    return {"data": new_post.dict()}


