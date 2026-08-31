from fastapi import FastAPI, Response, status, HTTPException, Depends
from . import models, schemas, utils 
from .database import engine, get_db
from sqlalchemy.orm import Session
from typing import List


#create instance of FastAPI named app
app = FastAPI()

models.Base.metadata.create_all(bind=engine)


#define a path GET operation (route/endpoint) decorator
@app.get("/")
def root():
    return {"message": "hello"}


@app.get("/posts", response_model=List[schemas.PostResponse])
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).where(models.Post.published == True).all()
    return posts

@app.post("/posts", status_code = status.HTTP_201_CREATED, 
          response_model=schemas.PostResponse)
def create_posts(new_post: schemas.PostCreate, db: Session = Depends(get_db)):
    #Using ORM sqlalchemy / unpack new_post dict into correct format
    new_p = models.Post(**new_post.model_dump())
    # Add to db
    db.add(new_p)
    #Commit changes
    db.commit()
    #Retrieve data from db (Returning *)
    db.refresh(new_p)
    return  new_p


@app.get("/posts/{id}", response_model=schemas.PostResponse)
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).where(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = f"post id {id} was not found")
    return post

@app.delete("/posts/{id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).where(models.Post.id == id)
    post = post_query.first()

    if not post:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, 
                                detail= f"Post id {id} doesn't exist")

    post_query.update({'published': False}, synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
    
@app.put("/posts/{id}", response_model=schemas.PostResponse)
def update_post(post: schemas.PostCreate, id: int, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).where(models.Post.id == id)
    post_to_update = post_query.first()

    if not post_to_update:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, 
                                detail= f"Post id {id} doesn't exist")

    post_query.update(post.model_dump(), synchronize_session=False)
    db.commit()
    db.refresh(post_to_update)
    return post_to_update
           
@app.post("/users", status_code=status.HTTP_201_CREATED, 
          response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    #hash password
    user.password = utils.hash_password(user.password)
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.get("/users/{id}", response_model=schemas.UserResponse)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).where(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, 
                                        detail= f"User with id {id} not found")

    return user