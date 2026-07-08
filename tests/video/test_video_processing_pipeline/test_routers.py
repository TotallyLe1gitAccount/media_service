import pytest
from fastapi.testclient import TestClient
from main import app


@pytest.fixture
def client():
    return TestClient(app)

#def test_post_returns_proper_status(client):
    with open("tests/test_videos/test_vid1.mp4", "rb") as f:
        response = client.post(
            "video/upload",
            files={"file": ("test_vid1.mp4", f, "video/mp4")}
            )

    assert response.status_code == 201