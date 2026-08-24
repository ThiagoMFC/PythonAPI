from fastapi import FastAPI

#create instance of FastAPI named app
app = FastAPI()

#define a path GET operation (route/endpoint) decorator
@app.get("/")
def root():
    return{"message": "hello"}