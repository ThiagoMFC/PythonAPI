from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel

#create instance of FastAPI named app
app = FastAPI()

class Post(BaseModel):
    title: str
    content: str

#define a path GET operation (route/endpoint) decorator
@app.get("/")
def root():
    return{"message": "hello"}

@app.get("/posts")
def get_posts():
    return{"data": "posts will go here"}

@app.post("/createposts")
#extract all fields from body, convert to dict, store inside payload
def create_posts(new_post: Post):
    return{"new_post":f"title: {new_post.title} content: {new_post.content}"}

