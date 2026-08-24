from fastapi import FastAPI

#create instance of FastAPI named app
app = FastAPI()

#define a path GET operation (route/endpoint) decorator
@app.get("/")
def root():
    return{"message": "hello"}

@app.get("/posts")
def get_posts():
    return{"data": "posts will go here"}