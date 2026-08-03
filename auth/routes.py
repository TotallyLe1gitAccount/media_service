from fastapi import APIRouter, Depends, HTTPException, status
from data.core import get_db
from auth.dependencies import get_auth_service, get_current_user, oauth2_scheme
from auth.service import AuthService, UserAlreadyExistsError, InvalidUserOrPasswordError
from auth.schemas import (
    RegisterRequest, RegisterResponse,
    LoginRequest, Token, UserResponse
)
from typing import Annotated

router = APIRouter(prefix="/auth")

@router.post("/register", response_model=RegisterResponse)
async def register(service: Annotated[AuthService, Depends(get_auth_service)], form_data: RegisterRequest):
    try:
        user = await service.register(form_data)
        return user
    
    except UserAlreadyExistsError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, 
            detail="User already exists")


@router.post("/login", response_model=Token)
async def login(service: Annotated[AuthService, Depends(get_auth_service)], form_data: LoginRequest):
    try:
        access_token = await service.login(form_data)
        return access_token
    
    except InvalidUserOrPasswordError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")


@router.get("/me", response_model=UserResponse)
def get_me(
    user = Depends(get_current_user)
):
    return user
    
