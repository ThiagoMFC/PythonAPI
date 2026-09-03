from fastapi import Response, status, HTTPException, Depends, APIRouter
from .. import models, schemas, oauth2 
from ..database import get_db
from sqlalchemy.orm import Session
from typing import List

router = APIRouter(prefix="/posts")

@router.get("/", response_model=List[schemas.PostResponse])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    posts = db.query(models.Post).where(models.Post.published == True).all()
    return posts

@router.post("/", status_code = status.HTTP_201_CREATED, 
          response_model=schemas.PostResponse)
def create_posts(new_post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    #Using ORM sqlalchemy / unpack new_post dict into correct format
    new_p = models.Post(**new_post.model_dump())
    # Add to db
    db.add(new_p)
    #Commit changes
    db.commit()
    #Retrieve data from db (Returning *)
    db.refresh(new_p)
    return  new_p


@router.get("/{id}", response_model=schemas.PostResponse)
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).where(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = f"post id {id} was not found")
    return post

@router.delete("/{id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).where(models.Post.id == id)
    post = post_query.first()

    if not post:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, 
                                detail= f"Post id {id} doesn't exist")

    post_query.update({'published': False}, synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
    
@router.put("/{id}", response_model=schemas.PostResponse)
def update_post(post: schemas.PostCreate, id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).where(models.Post.id == id)
    post_to_update = post_query.first()

    if not post_to_update:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, 
                                detail= f"Post id {id} doesn't exist")

    post_query.update(post.model_dump(), synchronize_session=False)
    db.commit()
    db.refresh(post_to_update)
    return post_to_update