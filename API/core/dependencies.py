from functools import lru_cache
from API.services.video_service import VideoService
from API.services.validators.validation import VideoValidator
from API.services.processing.video_normalization import VideoNormalizer
from API.services.file_storage import VideoSaver
from data.crud import CRUD as VideoRepo

@lru_cache
def get_video_service() -> VideoService:
        return VideoService(
        validator=VideoValidator(),
        normalizer=VideoNormalizer(),
        saver=VideoSaver(),
        repo=VideoRepo()
    )

@lru_cache
def get_video_repo() -> VideoRepo:
        return VideoRepo()