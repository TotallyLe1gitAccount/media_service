import os
from typing import Annotated
from ..core.dependencies import get_video_service, get_video_repo
from fastapi import APIRouter, UploadFile, HTTPException, File, Depends
from data.core import get_db
from sqlalchemy.orm import Session
from data.crud import CRUD as VideoRepo
from API.services.video_service import VideoService
from ..core.schemas.video_schemas import VideoResponse, VideoListResponse
from ..core.schemas.api_schemas import ApiResponse

router = APIRouter(prefix='/video')

@router.get('/', status_code=200, response_model=VideoListResponse)
def show_videos(
    db: Annotated[Session, Depends(get_db)], 
    repo: Annotated[VideoRepo, Depends(get_video_repo)]
    ):
    return repo.get_all_videos(db)

@router.get('/{video_id}', status_code=200, response_model=VideoResponse)
def show_video(
    video_id: int, 
    db: Annotated[Session, Depends(get_db)], 
    repo: Annotated[VideoRepo, Depends(get_video_repo)]
    ):
    video = repo.get_video(db, video_id=video_id)

    if not video:
        raise HTTPException(status_code=404, detail="video not found")

    return {
    "data": video
    }

@router.post('/upload', status_code=201, response_model=VideoResponse)
async def upload_video( 
    db: Annotated[Session, Depends(get_db)],
    service: Annotated[VideoService, Depends(get_video_service)],
    file: UploadFile = File(...)
    ):
    video = await service.upload_video(file, db)
    return {"data" : video}


@router.delete('/{video_id}', response_model=ApiResponse)
def del_video(
    video_id: int, 
    db: Annotated[Session, Depends(get_db)], 
    repo: Annotated[VideoRepo, Depends(get_video_repo)]
    ):
    video = repo.get_video(db, video_id)

    if not video:
        raise HTTPException(status_code=404, detail="video not found")

    if os.path.exists(video.path):
        os.remove(video.path)
    
    repo.delete_video(db, video_id)

    return {
    "data": {
        "status": "deleted"
        }
    }