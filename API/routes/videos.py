from ..core.dependencies import get_video_service, get_video_repo
from fastapi import APIRouter, UploadFile, HTTPException, File, Depends
from data.core import get_db
from sqlalchemy.orm import Session
import os

router = APIRouter(prefix='/video')

@router.get('/')
def show_videos(db: Session = Depends(get_db), repo = Depends(get_video_repo)):
    return repo.get_all_videos(db)

@router.get('/{video_id}')
def show_video(video_id: int, db: Session = Depends(get_db), repo = Depends(get_video_repo)):
    video = repo.get_video(db, video_id=video_id)

    if not video:
        raise HTTPException(status_code=404, detail="video not found")

    return {
    "data": video
    }

@router.post('/upload')
async def upload_video(
    file: UploadFile = File(...), 
    db: Session = Depends(get_db),
    service = Depends(get_video_service)):
    return await service.upload_video(file, db)

@router.delete('/{video_id}')
def del_video(video_id: int, db: Session = Depends(get_db), repo = Depends(get_video_repo)):
    video = repo.get_video(db, video_id)

    if not video:
        raise HTTPException(status_code=404, detail="video not found")

    if os.path.exists(video.path):
        os.remove(video.path)
    
    repo.delete_video(db, video_id)

    return {
    "data": {"status": "deleted"}
    }