import pytest
from fastapi.testclient import TestClient
from main import app


@pytest.fixture
def client():
    return TestClient(app)


def test_upload_video(client):
    response = client.post(
        "/video/upload",
        files={"file": ("test.mp4", b"fake data")}
    )

    assert response.status_code == 200
    data = response.json()

    assert "id" in data
    assert data["filename"] == "test.mp4"


def test_delete_video(client):
    upload = client.post(
        "/video/upload",
        files={"file": ("test.mp4", b"fake data")}
    )

    assert upload.status_code == 200

    video_id = upload.json()["id"]

    response = client.delete(f"/video/{video_id}")

    assert response.status_code == 200
    assert response.json()["status"] == "deleted"