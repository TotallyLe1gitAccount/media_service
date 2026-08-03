from auth.security import hash_password, verify_password
from auth.security import generate_access_token
from auth.schemas import LoginRequest, RegisterRequest, Token

class UserAlreadyExistsError(Exception):
    pass

class InvalidUserOrPasswordError(Exception):
    pass

class AuthService:
    def __init__(self, db, repo):
        self.repo = repo
        self.db = db

    async def register(self, data : RegisterRequest):
        user = self.repo.get_user_by_username(
        db=self.db,
        username=data.username
        )

        if user:
            raise UserAlreadyExistsError()

        user = self.repo.get_user_by_email(
            db=self.db, 
            email=data.email)
        if user:
            raise UserAlreadyExistsError()

        hashed_password = hash_password(data.password)
        created_user = self.repo.create_user(
            db=self.db, 
            username=data.username,
            email=data.email,
            password_hash=hashed_password)

        return {
            "id": created_user.id,
            "username": created_user.username,
            "email": created_user.email
        }

    async def login(self, data: LoginRequest):
        user = self.repo.get_user_by_email(
            db=self.db, 
            email=data.email)

        if user is None:
            raise InvalidUserOrPasswordError()

        if not verify_password(data.password, user.password_hash):
            raise InvalidUserOrPasswordError()
      
        token = generate_access_token({"sub": str(user.id)})
        
        return Token(
        access_token=token,
        token_type="bearer"
        )