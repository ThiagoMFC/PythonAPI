from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
import psycopg2
from psycopg2.extras import RealDictCursor
import time
import os
from dotenv import load_dotenv
from . import models 
from .database import engine, get_db
from sqlalchemy.orm import Session

#create instance of FastAPI named app
app = FastAPI()

# Load the variables from the .env file
load_dotenv()

models.Base.metadata.create_all(bind=engine)


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


#define a path GET operation (route/endpoint) decorator
@app.get("/")
def root():
    return {"message": "hello"}


@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    #cursor.execute(""" SELECT * FROM posts WHERE published = True""")
    #posts = cursor.fetchall()
    posts = db.query(models.Post).where(models.Post.published == True).all()
    return {"data": posts}

@app.post("/posts", status_code = status.HTTP_201_CREATED)
def create_posts(new_post: Post, db: Session = Depends(get_db)):
    # %s sanitizes variable to avoid sql injection
    #cursor.execute(""" INSERT INTO posts (title, content, published) 
    #    VALUES (%s, %s, %s) RETURNING * """, 
    #    (new_post.title, new_post.content, new_post.published))
    #new_p = cursor.fetchone()
    #commit changes in DB
    #conn.commit()


    #  Using ORM sqlalchemy / unpack new_post dict into correct format
    new_p = models.Post(**new_post.model_dump())
    # Add to db
    db.add(new_p)
    # Aommit changes
    db.commit()
    # Retrieve data from db (Returning *)
    db.refresh(new_p)
    return {"data": new_p}


@app.get("/posts/{id}")
def get_post(id: int, db: Session = Depends(get_db)):
    #cursor.execute(""" SELECT * FROM posts WHERE id = %s AND published =
    #        True """, (str(id)))
    #post = cursor.fetchone()

    post = db.query(models.Post).where(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = f"post id {id} was not found")
    return {"data": post} 

@app.delete("/posts/{id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute(""" UPDATE posts SET published = 'False' 
                    WHERE id = %s AND published = True RETURNING *""",
                   (str(id)))
    post = cursor.fetchone()
    conn.commit()
    if not post:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, 
                                detail= f"Post id {id} doesn't exist")

    return Response(status_code=status.HTTP_204_NO_CONTENT)
    
@app.put("/posts/{id}")
def update_post(post: Post, id: int):
    cursor.execute(""" UPDATE posts SET title = %s, content = %s 
                        WHERE id = %s AND published = True RETURNING *""",
                       (post.title, post.content, str(id)))
    post_updated = cursor.fetchone()
    conn.commit()
    if not post_updated:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, 
                                detail= f"Post id {id} doesn't exist")
    return {"data" : post_updated}
           


