from fastapi import FastAPI
from . import models
from .database import engine
from .routers import post, user, auth, vote

#create instance of FastAPI named app
app = FastAPI()

models.Base.metadata.create_all(bind=engine)

#import routers
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

#define a path GET operation (route/endpoint) decorator
@app.get("/")
def root():
    return {"message": "hello"}



           
