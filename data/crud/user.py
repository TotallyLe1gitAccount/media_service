from data.models import User
from sqlalchemy.orm import Session
from sqlalchemy import select, delete
from typing import Optional

class UserCRUD:
    def create_user(self, db: Session, username: str, email: str, password_hash: str):
        user = User(
            username=username,
            email=email,
            password_hash=password_hash
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        return user

    def delete_user(self, db: Session, id: int):
        stmt = delete(User).where(User.id == id)

        db.execute(stmt)
        db.commit()

    def edit_user(
            self, 
            db: Session, 
            id: int,
            new_username: Optional[str], 
            new_email: Optional[str], 
            new_password_hash: Optional[str]):

        user = db.scalar(
            select(User).where(User.id == id)
        )
        if user is not None:
            return None

        if new_username is not None:
            user.username = new_username
        
        if new_email is not None:
            user.email = new_email

        if new_password_hash is not None:
            user.password_hash = new_password_hash

        db.commit()
        db.refresh(user)

        return user

    def get_user_by_email(self, db: Session, email: str):
        return db.scalar(
            select(User).where(User.email == email)
        )

    def get_user_by_username(self, db: Session, username: str):
        return db.scalar(
            select(User).where(User.username == username)
        )


    def get_users(self, db: Session, limit=1000):
        return db.scalars(
            select(User).limit(limit)
        ).all()
