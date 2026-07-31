import jwt
from pwdlib import PasswordHash
import secrets
from config import (
    SECRET_KEY, ALGORHITM,
    ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_DAYS)
import datetime


#TOKEN
def generate_access_token(token_data: dict) -> str:
    to_encode = token_data.copy()
    expired = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expired})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, ALGORHITM)

    return encoded_jwt

def decode_token(token: str):
    try:
        jwt.decode(token, SECRET_KEY, algorithms=[ALGORHITM])

    except jwt.DecodeError:
        return None



