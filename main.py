from fastapi import FastAPI
from API.routes.videos import router as video_router
from auth.routes import router as auth_router
from data.core import engine
from data.models import Base

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(video_router)
app.include_router(auth_router)