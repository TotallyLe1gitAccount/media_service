from pydantic import BaseModel, ConfigDict
from datetime import datetime

class VideoBase(BaseModel):
    pass

class VideoCreate(VideoBase):
    pass

class VideoOut(VideoBase):
    id : int
    filename: str
    path : str
    created_at : datetime

    model_config = ConfigDict(from_attributes=True)

class VideoResponse(BaseModel):
    data : VideoOut

class VideoListResponse(BaseModel):
    data : list[VideoOut]