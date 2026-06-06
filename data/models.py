from sqlalchemy import Column, BigInteger, String, DateTime
from sqlalchemy.orm import DeclarativeBase
from datetime import datetime

class Base(DeclarativeBase):
    pass

class Video(Base):
    __tablename__ = "videos"

    id = Column(BigInteger, primary_key=True)
    filename = Column(String(255), nullable=False)
    path = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.now)
