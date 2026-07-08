import pytest
import subprocess
from API.services.processing.video_normalization import VideoNormalizer
import subprocess
import os
from unittest.mock import patch


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

def test_normalize_creates_file(tmp_path, fake_video):
    output_path =  tmp_path / "processed.mp4"

    normalizer = VideoNormalizer()
    res = normalizer.normalize_video(fake_video, output_path)

    assert os.path.exists(output_path)
    assert os.path.getsize(output_path) > 0
    assert res == output_path
    

@patch("subprocess.run")
def test_build_command(mock_run):
    mock_run.return_value.returncode = 0
    mock_run.return_value.stderr = ""
    normalizer = VideoNormalizer()

    normalizer.normalize_video(
        "input.mp4",
        "output.mo4",
        fps=60,
        crf=18
        )
    
    mock_run.assert_called_once()
    args, kwargs = mock_run.call_args

    assert kwargs["text"] is True
    assert kwargs["stdout"] == subprocess.PIPE
    
    cmd = args[0]

    assert "-vf" in cmd
    assert "fps=60" in cmd
    assert "-crf" in cmd
    assert "18" in cmd
    
