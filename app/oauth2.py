from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from . import schemas, database, models
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRES_MINUTES)

    to_encode.update({"exp": expire})
    
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

    return encoded_jwt

def verify_access_token(token: str, credentials_exception):

    try:
        
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=settings.ALGORITHM)

        user_id = str(payload.get("user_id"))

        if user_id is None:
            raise credentials_exception

        token_data = schemas.TokenData(id=user_id)

    except JWTError:
        raise credentials_exception

    return token_data

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):

    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Could not validade credentials", headers={"WWW-Authenticate": "Bearer"})

    token = verify_access_token(token, credentials_exception)
    user = db.query(models.User).where(models.User.id == token.id).first()

    return user
