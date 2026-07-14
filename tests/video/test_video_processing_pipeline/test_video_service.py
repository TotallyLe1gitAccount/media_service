import pytest
from unittest.mock import Mock, AsyncMock
from API.services.video_service import VideoService
import asyncio

@pytest.mark.asyncio
async def test_video_service_upload_returns_validation_size_error():
    validator = Mock()
    normalizer = Mock()
    saver = Mock()
    repo = Mock()

    file = None
    db = None

    video_service = VideoService(
        validator,
        normalizer,
        saver,
        repo
    )
    validator.validate_size.return_value = (False, "test_size_error")

    res = await video_service.upload_video(file, db)    
    assert res == "test_size_error"

@pytest.mark.asyncio
async def test_video_service_upload_returns_validation_content_error():
    validator = Mock()
    normalizer = Mock()
    saver = Mock()
    repo = Mock()

    file = None
    db = None

    video_service = VideoService(
        validator,
        normalizer,
        saver,
        repo
    )

    validator.validate_size.return_value = (True, None)
    validator.validate_content = AsyncMock(
        return_value = (False, "test_content_error")
    )

    res = await video_service.upload_video(file, db)    
    assert res == "test_content_error"

@pytest.mark.asyncio
async def test_video_service_upload_returns_validation_metadata_error():
    validator = Mock()
    normalizer = Mock()
    saver = Mock()
    repo = Mock()

    file = None
    db = None

    video_service = VideoService(
        validator,
        normalizer,
        saver,
        repo
    )

    validator.validate_size.return_value = (True, None)
    validator.validate_content = AsyncMock(
        return_value = (True, None)
    )
    validator.validate_metadata.return_value = (False, "test_metadata_error")

    res = await video_service.upload_video(file, db)    
    assert res == "test_metadata_error"

@pytest.mark.asyncio
async def test_upload_stops_after_size_validation_error():
    validator = Mock()
    normalizer = Mock()
    saver = Mock()
    repo = Mock()

    file = None
    db = None
    video_service = VideoService(
        validator,
        normalizer,
        saver,
        repo
    )
    validator.validate_size.return_value = (False, "test_size_error")

    await video_service.upload_video(file, db)   

    validator.validate_content.assert_not_called()
    normalizer.probe.assert_not_called()
    validator.validate_metadata.assert_not_called()
    normalizer.normalizer_video.assert_not_called()
    repo.create_video.assert_not_called()

@pytest.mark.asyncio
async def test_upload_stops_after_content_validation_error():
    validator = Mock()
    normalizer = Mock()
    saver = Mock()
    repo = Mock()

    file = None
    db = None
    video_service = VideoService(
        validator,
        normalizer,
        saver,
        repo
    )
    validator.validate_size.return_value = (True, None)
    validator.validate_content = AsyncMock(
        return_value = (False, "test_content_error")
    )

    await video_service.upload_video(file, db)    

    normalizer.probe.assert_not_called()
    validator.validate_metadata.assert_not_called()
    normalizer.normalizer_video.assert_not_called()
    repo.create_video.assert_not_called()

@pytest.mark.asyncio
async def test_upload_stops_after_metadata_validation_error():
    validator = Mock()
    normalizer = Mock()
    saver = Mock()
    repo = Mock()

    file = None
    db = None
    video_service = VideoService(
        validator,
        normalizer,
        saver,
        repo
    )
    validator.validate_size.return_value = (True, None)
    validator.validate_content = AsyncMock(
        return_value = (True, None)
    )
    validator.validate_metadata.return_value = (False, "test_metadata_error")

    await video_service.upload_video(file, db)    

    normalizer.normalizer_video.assert_not_called()
    repo.create_video.assert_not_called()

@pytest.mark.asyncio
async def test_video_service_upload_returns_created_video():
    validator = Mock()
    normalizer = Mock()
    saver = Mock()
    repo = Mock()
    
    file = Mock()
    file.filename = "video.mp4"
    db = None

    validator.validate_size.return_value = (True, None)
    validator.validate_content = AsyncMock(return_value=(True, None))
    normalizer.probe.return_value = {
        "width": 1920,
        "height": 1080,
        "duration": 60,
    }

    validator.validate_metadata.return_value = (True, None)
    normalizer.normalizer_video.return_value = "/processed/video.mp4"

    created_video = Mock()
    repo.create_video.return_value = created_video

    video_service = VideoService(
        validator,
        normalizer,
        saver,
        repo
    )
    result = await video_service.upload_video(file, db)

    assert result == created_video
