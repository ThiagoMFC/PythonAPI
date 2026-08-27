from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange



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

@app.post("/posts", status_code = status.HTTP_201_CREATED)
def create_posts(new_post: Post):
    post_dict = new_post.dict()
    #add random id for testing purposes
    post_dict["id"] = randrange(0, 1000000)
    my_posts.append(post_dict)
    return {"data": post_dict}


@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    post = next((post for post in my_posts if post["id"] == id), None)
    if post is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = f"post id {id} was not found")
    return {"data": post} 

@app.delete("/posts/{id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    #deleting from dict for testing purposes
    for i, post in enumerate(my_posts):
        if post['id'] == id:
            my_posts.pop(i)
            return Response(status_code=status.HTTP_204_NO_CONTENT)
    #when no post is found
    raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, 
                        detail= f"Post id {id} doesn't exist")

@app.put("/posts/{id}")
def update_post(post: Post, id: int):
    for i, p in enumerate(my_posts):
            if p['id'] == id:
                my_posts[i] = post.dict()
                return {"message" : "post updated"}
    #when no post is found
    raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, 
                        detail= f"Post id {id} doesn't exist")
           


