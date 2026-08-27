from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
import os
from dotenv import load_dotenv

#create instance of FastAPI named app
app = FastAPI()

# Load the variables from the .env file
load_dotenv()

class Post(BaseModel):
    title: str
    content: str
    published: Optional[bool] = True

#try connecting to DB every 5 seconds until succeeds
while True:
    try:
        conn = psycopg2.connect(host = os.getenv('DB_HOST'), 
                                database=os.getenv('DB_NAME'), 
                                user=os.getenv('DB_USER'), 
                                password=os.getenv('DB_USER_PWD'), 
                                cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print ("DB connection successful")
        break
    except Exception as error:
        print("DB connection failed")
        print("Error: ", error)
        time.sleep(5)

#hardcode some posts for testing purposes
my_posts = [{"title": "title of post 1", "content": "content of post 1", "published": True, "id": 1},
             {"title": "title of post 2", "content": "content of post 2", "published": True, "id": 2}]

#define a path GET operation (route/endpoint) decorator
@app.get("/")
def root():
    return {"message": "hello"}

@app.get("/posts")
def get_posts():
    cursor.execute(""" SELECT * FROM posts """)
    posts = cursor.fetchall()
    return {"data": posts}

@app.post("/posts", status_code = status.HTTP_201_CREATED)
def create_posts(new_post: Post):
    # %s sanitizes variable to avoid sql injection
    cursor.execute(""" INSERT INTO posts (title, content, published) 
        VALUES (%s, %s, %s) RETURNING * """, 
        (new_post.title, new_post.content, new_post.published))

    new_p = cursor.fetchone()
    #commit changes in DB
    conn.commit()
    return {"data": new_p}


@app.get("/posts/{id}")
def get_post(id: int):
    cursor.execute(""" SELECT * FROM posts WHERE id = %s """, (str(id)))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = f"post id {id} was not found")
    return {"data": post} 

@app.delete("/posts/{id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute(""" UPDATE posts SET published = 'False' 
                    WHERE id = %s RETURNING *""",
                   (str(id)))
    post = cursor.fetchone()
    conn.commit()
    if not post:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, 
                                detail= f"Post id {id} doesn't exist")

    return Response(status_code=status.HTTP_204_NO_CONTENT)
    
@app.put("/posts/{id}")
def update_post(post: Post, id: int):
    for i, p in enumerate(my_posts):
            if p['id'] == id:
                post_dict = post.dict()
                post_dict['id'] = id
                my_posts[i] = post_dict
                return {"message" : "post updated"}
    #when no post is found
    raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, 
                        detail= f"Post id {id} doesn't exist")
           


