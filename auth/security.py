import jwt
from pwdlib import PasswordHash
import secrets
from config import (
    SECRET_KEY, ALGORITHM,
    ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_DAYS)
import datetime


#TOKEN
def generate_access_token(token_data: dict) -> str:
    to_encode = token_data.copy()
    expired = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expired})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)

    return encoded_jwt

def decode_token(token: str):
    try:
        payload = jwt.decode(
            token, 
            SECRET_KEY, 
            algorithms=[ALGORITHM])

        return payload

    except Exception as e:
        print("JWT ERROR:", repr(e))
        return None
    
#PASSWORD 
password_hash = PasswordHash.recommended() 

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_hash.verify(plain_password, hashed_password)

def hash_password(password: str) -> str:
    return password_hash.hash(password)
    
