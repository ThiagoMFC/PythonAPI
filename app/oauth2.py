from jose import JWTError, jwt
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

# Load the .env file
load_dotenv(override=True)

def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.now() + timedelta(minutes=int(os.getenv('ACCESS_TOKEN_EXPIRES_MINUTES')))

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, os.getenv('SECRET_KEY'), algorithm=os.getenv('ALGORITHM'))

    return encoded_jwt

