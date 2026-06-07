from fastapi import FastAPI
from API.routes.videos import router as video_router

app = FastAPI()

app.include_router(video_router)