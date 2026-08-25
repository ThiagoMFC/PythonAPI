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

#define a path GET operation (route/endpoint) decorator
@app.get("/")
def root():
    return{"message": "hello"}

@app.get("/posts")
def get_posts():
    return{"data": "posts will go here"}

@app.post("/createposts")
def create_posts(new_post: Post):
    return{"data": new_post.dict()}


