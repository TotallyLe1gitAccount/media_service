import pytest
from API.services.validators.validation import VideoValidator, MAX_FILE_SIZE
from io import BytesIO
from starlette.datastructures import UploadFile
import asyncio
from unittest.mock import patch

def video_update(duration=120.5, **video_updates):
    video = {
            "codec_type": "video",
            "codec_name": "h264",
            "width": 1920,
            "height": 1080,
            "avg_frame_rate": "60/1",
    }
    video.update(video_updates)

    return {
        "streams": [video],
        "format": {"duration": duration}
    }

def make_upload_file(size: int):
    return UploadFile(
        filename=f"test.{format}",
        file=BytesIO(b"a" * size),
    )

@pytest.fixture
def mock_service():
    return VideoValidator()

#SIZE TESTS 
@pytest.mark.parametrize("size, expected", [
    (1024, (True, {"code": "OK"})),
    (0, (True, {"code": "OK"})),
    (MAX_FILE_SIZE, (True, {"code": "OK"})),
    (MAX_FILE_SIZE + 1, (False, {"code": "file_too_big"}))
])
def test_validate_file_size(mock_service, size, expected):
    file = make_upload_file(size)
    result = mock_service.validate_size(file)

    assert result == expected

#CONTENT TESTS
@pytest.mark.asyncio
@patch("API.services.validators.validation.magic.from_buffer")
async def test_validate_file_content(mock_magic, mock_service):
    mock_magic.return_value = "video/mp4"

    file = make_upload_file(2048)
    result = await mock_service.validate_content(file)

    assert result == (True, {"code": "OK"})

    mock_magic.return_value = "text/plain"

    result = await mock_service.validate_content(file)
    assert result == (False, {"code": "invalid_content"})

#METADATA TESTS
@pytest.mark.parametrize("info, expected",[
    (video_update(), (True, {"code": "OK"})),
    (video_update(codec_type = "unsupported_codec"), (False, {"code": "no_video_stream"})),
    (video_update(codec_name = "unknown_type"), (False, {"code": "unsupported_video_content"})),
    (video_update(width = 0), (False, {"code": "resolution_too_low"})),
    (video_update(height = 0), (False, {"code": "resolution_too_low"})),
    (video_update(width = 10921), (False, {"code": "resolution_too_high"})),
    (video_update(height = 10080), (False, {"code": "resolution_too_high"})),
    (video_update(avg_frame_rate = "30/1"), (True, {"code": "OK"})),
    (video_update(avg_frame_rate = "10000/1"), (False, {"code": "fps_too_high"})),
    (video_update(duration = 100000), (False, {"code": "video_too_long"})),
    (video_update(duration = -1), (False, {"code": "video_too_short"})),

])
def test_validate_metadata(mock_service, info, expected):
    res = mock_service.validate_metadata(info)
    
    assert res == expected
