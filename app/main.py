from fastapi import FastAPI, Response, status, HTTPException, Depends
from . import models, schemas 
from .database import engine, get_db
from sqlalchemy.orm import Session

#create instance of FastAPI named app
app = FastAPI()

models.Base.metadata.create_all(bind=engine)

#define a path GET operation (route/endpoint) decorator
@app.get("/")
def root():
    return {"message": "hello"}


@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).where(models.Post.published == True).all()
    return {"data": posts}

@app.post("/posts", status_code = status.HTTP_201_CREATED)
def create_posts(new_post: schemas.PostCreate, db: Session = Depends(get_db)):
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
    post = db.query(models.Post).where(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = f"post id {id} was not found")
    return {"data": post} 

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
    
@app.put("/posts/{id}")
def update_post(post: schemas.PostCreate, id: int, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).where(models.Post.id == id)
    post_to_update = post_query.first()

    if not post_to_update:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, 
                                detail= f"Post id {id} doesn't exist")

    post_query.update(post.model_dump(), synchronize_session=False)
    db.commit()
    db.refresh(post_to_update)
    
    return {"data" : post_to_update}
           


