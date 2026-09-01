from fastapi import FastAPI, Response, status, HTTPException, Depends
from . import models, schemas, utils 
from .database import engine, get_db
from sqlalchemy.orm import Session
from typing import List
from .routers import post, user, auth

#create instance of FastAPI named app
app = FastAPI()

models.Base.metadata.create_all(bind=engine)

#import routers
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

#define a path GET operation (route/endpoint) decorator
@app.get("/")
def root():
    return {"message": "hello"}



           
