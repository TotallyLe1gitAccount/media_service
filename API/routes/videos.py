from data.crud import create_video, get_all_videos, get_video, delete_video
from data.core import get_db
from sqlalchemy.orm import Session
from API.services.validators.validation import validate_content, validate_size, validate_metadata
from API.services.validators.ffm import probe
from API.services.file_storage import save_file
import os
import uuid
import asyncio

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
async def upload_video(file: UploadFile = File(...), db: Session = Depends(get_db)):
    os.makedirs("uploads", exist_ok=True)

    file_name = f"{uuid.uuid4()}.mp4"
    file_location = f'uploads/{file_name}'

    if not await validate_size(file):
        raise HTTPException(status_code=413, detail="file size too big")

    if not await validate_content(file):
        raise HTTPException(status_code=400, detail="invalid type")

    save_file(file, file_location)

    file_info = probe(file_location)
    ok, error = validate_metadata(file_info)

    if not ok:
        raise HTTPException(status_code=400, detail=error)

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