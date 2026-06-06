from data.crud import create_video, get_all_videos, get_video, delete_video
from data.core import get_db
from sqlalchemy.orm import Session
import os

from fastapi import APIRouter, UploadFile, HTTPException, File, Depends

router = APIRouter(prefix='/video')

@router.get('/')
def show_videos(db: Session = Depends(get_db)):
    videos = get_all_videos(db)

    return videos

@router.get('/{video_id}')
def show_video(video_id: int, db: Session = Depends(get_db)):
    video = get_video(db, video_id=video_id)

    if not video:
        raise HTTPException(status_code=404, detail="video not found")

    return video 

@router.post('/upload')
def upload_video(file : UploadFile = File(...), db: Session = Depends(get_db)):
    file_location = f'uploads/{file.filename}'
    
    with open(file_location, "wb") as f:
        f.write(file.file.read())

    video = create_video(db, filename=file.filename, path=file_location)

    return video

@router.delete('/{video_id}')
def del_video(video_id: int, db: Session = Depends(get_db)):
    video = get_video(db, video_id)

    if not video:
        raise HTTPException(status_code=404, detail="video not found")

    if os.path.exists(video.path):
        os.remove(video.path)

    delete_video(db, video_id)

    return {"status": "deleted"}