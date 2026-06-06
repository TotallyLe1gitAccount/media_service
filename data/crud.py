from models import Video
from sqlalchemy.orm import Session

def create_video(db : Session, filename : str, path : str):
    video = Video(filename=filename, path=path)
    db.add(video)
    db.commit()
    db.refresh()
    
    return video

def get_video(db : Session, video_id : int):
    return db.query(Video).filter_by(Video.id == video_id).first()

def get_all_videos(db : Session):
    return db.query(Video).all()

def delete_video(db : Session, video_id : int):
    video = get_video(db, video_id)
    if video:
        db.delete(video)
        db.commit()

    return video