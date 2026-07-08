import pytest
import subprocess
from API.services.validators.ffm import probe
import subprocess
import os

def generate_fake_video(path):
    cmd = [
        "ffmpeg",
        "-y",
        "-f", "lavfi",
        "-i", "testsrc=duration=5:size=640x360:rate=30",
        "-f", "lavfi",
        "-i", "sine=frequency=440:duration=5",
        "-c:v", "libx264",
        "-c:a", "aac",
        "-shortest",
        str(path)
    ]
    subprocess.run(cmd, check=True)


@pytest.fixture
def fake_video(tmp_path):
    file_path = tmp_path / "test.mp4"
    generate_fake_video(file_path)
    return file_path

def test_probe_returns_parsed_json(fake_video):
    data = probe(fake_video)

    assert isinstance(data, dict)

def test_probe_returns_metadata(fake_video):
    data = probe(fake_video)

    assert "streams" in data
    assert "format" in data

def test_probe_raises_file_not_found():
    nonexistent_path = "nonexistent/video.mp4"
    with pytest.raises(FileNotFoundError) as exc_info:
        probe(nonexistent_path)


    assert str(exc_info.value) == (
        f"File not found: "
        f"{os.path.abspath(nonexistent_path)}"
    )



