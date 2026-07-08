import pytest
from API.services.file_storage import VideoSaver
import asyncio
from io import BytesIO
from unittest.mock import Mock

@pytest.mark.asyncio
async def test_file_creates_file(tmp_path):
    content = b"this is a test"

    file = Mock()
    file.file = BytesIO(content)
    
    path = tmp_path / "test.mp4"

    saver = VideoSaver()
    await saver.save_file(file, str(path))

    assert path.read_bytes() == content

