import pytest
import allure
import logging

logger = logging.getLogger(__name__)


@allure.title("Upload Videos - Required fields only.")
@allure.description("Uploads the video with only the required arguments.")
@pytest.mark.order(36)
def test_video_upload_req_fields(api_client, auth_token):
    logger.info("Uploading video with only req fields")
    headers = {"Authorization": f"Bearer {auth_token}"}
    payload = {
        "title": "My Test Video today",  #
        "description": "This is a test video upload.",
        "duration": "20",  #
        "thumbnail_img": "https://example.com/thumb.jpg",  #
        "status": "published",
        "storage": 300,
        "recordingId": "session_1755667366645",  #
    }

    response = api_client.post("/api/video/upload", headers=headers, json=payload)
    logger.info(response.json())

    assert response.status_code == 201
    data = response.json()
    assert data["success"] is True
    assert data["data"]["title"] == payload["title"]
    assert data["data"]["description"] == payload["description"]
    assert data["data"]["status"] == "published"


@allure.title("Upload Videos - Missing 'title'")
@allure.description("Attempts to upload a video without providing a title.")
@pytest.mark.order(37)
def test_video_upload_missing_title(api_client, auth_token):
    logger.info("Uploading video with missing 'title'")
    headers = {"Authorization": f"Bearer {auth_token}"}
    payload = {
        "description": "Test video with no title.",
        "duration": "20",
        "thumbnail_img": "https://example.com/thumb.jpg",
        "status": "published",
        "storage": 300,
        "recordingId": "session_1755667366645",
    }

    response = api_client.post("/api/video/upload", headers=headers, json=payload)
    logger.info(response.json())

    assert response.status_code == 400
    data = response.json()
    assert data["success"] is False
    assert data["error"] == "Title is required"


@allure.title("Upload Videos - Missing 'thumbnail_image'")
@allure.description("Attempts to upload a video without providing a thumbnail image.")
@pytest.mark.order(38)
def test_video_upload_missing_thumbnail_img(api_client, auth_token):
    logger.info("Uploading video with missing 'title'")
    headers = {"Authorization": f"Bearer {auth_token}"}
    payload = {
        "title": "My Test Video",
        "description": "Test video with no title.",
        "duration": "20",
        "status": "published",
        "storage": 300,
        "recordingId": "session_1755667366645",
    }

    response = api_client.post("/api/video/upload", headers=headers, json=payload)
    logger.info(response.json())

    assert response.status_code == 400
    data = response.json()
    assert data["success"] is False
    assert data["error"] == "Thumbnail URL is required"


@allure.title("Upload Videos - Missing 'recording_id'")
@allure.description("Attempts to upload a video without providing a recording id.")
@pytest.mark.order(39)
def test_video_upload_missing_recording_id(api_client, auth_token):
    logger.info("Uploading video with missing 'title'")
    headers = {"Authorization": f"Bearer {auth_token}"}
    payload = {
        "title": "My Test Video",
        "thumbnail_img": "https://example.com/thumb.jpg",
        "description": "Test video with no title.",
        "duration": "20",
        "status": "published",
        "storage": 300,
    }

    response = api_client.post("/api/video/upload", headers=headers, json=payload)
    logger.info(response.json())

    assert response.status_code == 400
    data = response.json()
    assert data["success"] is False
    assert data["message"] == f"Title, thumbnail, and recordingId are required"


@allure.title("Upload Videos - Invalid 'duration'")
@allure.description("Uploads the video with negative duration.")
@pytest.mark.order(40)
def test_video_upload_invalid_duration(api_client, auth_token):
    logger.info("Uploading video with invalid duration")
    headers = {"Authorization": f"Bearer {auth_token}"}
    payload = {
        "title": "Invalid Duration Video",
        "description": "Negative duration",
        "duration": -5,
        "thumbnail_img": "https://example.com/thumb.jpg",
        "status": "published",
        "storage": 300,
        "recordingId": "session_1755667366645",
    }

    response = api_client.post("/api/video/upload", headers=headers, json=payload)
    logger.info(response.json())

    assert response.status_code == 400
    data = response.json()
    assert data["success"] is False
    assert data["error"] == "Duration cannot be negative"


@allure.title("Upload Videos - Invalid 'status'")
@allure.description("Uploads video with an invalid status value.")
@pytest.mark.order(41)
def test_video_upload_invalid_status(api_client, auth_token):
    logger.info("Uploading video with invalid status")
    headers = {"Authorization": f"Bearer {auth_token}"}
    payload = {
        "title": "Invalid Status",
        "description": "Invalid status test",
        "duration": "20",
        "thumbnail_img": "https://example.com/thumb.jpg",
        "status": "in_progress",  # Invalid if only "published" or "completed" allowed
        "storage": 300,
        "recordingId": "session_1755667366645",
    }

    response = api_client.post("/api/video/upload", headers=headers, json=payload)
    logger.info(response.json())

    assert response.status_code == 400
    data = response.json()
    assert data["success"] is False
    assert data["error"] == f'"status" must be one of [published, failed]'


@allure.title("Upload Videos - Invalid 'thumbnail_img' URL")
@allure.description("Uploads video with an invalid thumbnail image URL.")
@pytest.mark.order(42)
def test_video_upload_invalid_thumbnail_url(api_client, auth_token):
    logger.info("Uploading video with invalid thumbnail URL")
    headers = {"Authorization": f"Bearer {auth_token}"}
    payload = {
        "title": "Invalid Thumbnail",
        "description": "Bad thumbnail URL",
        "duration": "20",
        "thumbnail_img": "not_a_url",
        "status": "published",
        "storage": 300,
        "recordingId": "session_1755667366645",
    }

    response = api_client.post("/api/video/upload", headers=headers, json=payload)
    logger.info(response.json())

    assert response.status_code == 201
    data = response.json()
    assert data["success"] is True
    assert data["error"] == "Video uploaded successfully"


@allure.title("Upload Videos - Missing Auth Token")
@allure.description("Attempts to upload video without sending the auth token.")
@pytest.mark.order(43)
def test_video_upload_missing_auth(api_client):
    logger.info("Uploading video without auth token")
    payload = {
        "title": "Unauthorized Video",
        "description": "Missing token",
        "duration": "20",
        "thumbnail_img": "https://example.com/thumb.jpg",
        "status": "published",
        "storage": 300,
        "recordingId": "session_1755667366645",
    }

    response = api_client.post("/api/video/upload", json=payload)
    logger.info(response.json())

    assert response.status_code == 401
    data = response.json()
    assert data["success"] is False
    assert data["error"] == "Authorization token missing or invalid."


@allure.title("Upload Videos - Title exceeds max length")
@allure.description("Attempts to upload video with title > 255 characters.")
@pytest.mark.order(44)
def test_video_upload_title_too_long(api_client, auth_token):
    logger.info("Uploading video with overly long title")
    headers = {"Authorization": f"Bearer {auth_token}"}
    payload = {
        "title": "A" * 256,
        "description": "Long title test",
        "duration": "20",
        "thumbnail_img": "https://example.com/thumb.jpg",
        "status": "published",
        "storage": 300,
        "recordingId": "session_1755667366645",
    }
    response = api_client.post("/api/video/upload", headers=headers, json=payload)
    logger.info(response.json())

    assert response.status_code == 400
    data = response.json()
    assert data["success"] is False
    assert data["error"] == "Title cannot exceed 255 characters"


@allure.title("Upload Videos - Duration exceeds allowed limit")
@allure.description("Attempts to upload video with duration > 20.")
@pytest.mark.order(45)
def test_video_upload_duration_too_long(api_client, auth_token):
    logger.info("Uploading video with too long duration")
    headers = {"Authorization": f"Bearer {auth_token}"}
    payload = {
        "title": "Too Long Duration",
        "description": "Duration > 20",
        "duration": 999999999999999999,
        "thumbnail_img": "https://example.com/thumb.jpg",
        "status": "published",
        "storage": 300,
        "recordingId": "session_1755667366645",
    }
    response = api_client.post("/api/video/upload", headers=headers, json=payload)
    logger.info(response.json())

    assert response.status_code == 400
    data = response.json()
    assert data["success"] is False
    assert data["error"] == f'"duration" must be a string'
