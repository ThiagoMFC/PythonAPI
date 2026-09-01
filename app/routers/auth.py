from fastapi import APIRouter, Response, status, HTTPException, Depends
from sqlalchemy.orm import Session
from .. import database, schemas, models, utils

router = APIRouter()

@router.post("/login")
def login(user_creds: schemas.UserLogin, 
          db: Session = Depends(database.get_db)):
    user = db.query(models.User).where(models.User.email == user_creds.email).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid credentials")

    if not utils.verify_password(user_creds.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid credentials")
        
    #create token

    
    return {"somethin"}
