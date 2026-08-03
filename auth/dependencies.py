from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from auth.security import decode_token
from auth.service import AuthService
from data.core import get_db
from data.models import User
from data.crud.user import UserCRUD as repo

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="auth/login"
)

def get_current_user(
        token: str = Depends(oauth2_scheme),
        db: Session = Depends(get_db)
):
    payload = decode_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )

    user_id =int(payload.get("sub"))
    user = db.get(User, user_id)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED
            )

    return user

def get_auth_service(
    db = Depends(get_db),
    repository = Depends(repo)
):
    return AuthService(db, repository)

