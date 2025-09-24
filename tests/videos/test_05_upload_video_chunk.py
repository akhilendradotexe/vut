import pytest
import allure
import logging
import os

logger = logging.getLogger(__name__)

VIDEO_FILE_PATH = "utils/recording.mp4"

# ---------- POSITIVE TEST CASE ---------- #


@allure.title("Upload Chunk - Valid Request")
@allure.description("Upload a valid video chunk with correct recording ID.")
@pytest.mark.order(80)
def test_upload_chunk_success(api_client):
    with open(VIDEO_FILE_PATH, "rb") as file:
        files = {
            "recordingId": (None, "session_1755516734335"),
            "videoChunks": ("recording.mp4", file, "video/mp4"),
        }

        response = api_client.post("/api/video/upload-chunk", files=files)
        logger.info(response.json())

    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["message"] == "1 chunks uploaded successfully."


# ---------- NEGATIVE TEST CASES ---------- #


@allure.title("Upload Chunk - Missing Video File")
@allure.description("Should return 400 when videoChunks field is missing.")
@pytest.mark.order(81)
def test_upload_chunk_missing_file(api_client):
    files = {
        "recordingId": (None, "session_1755516734335"),
    }

    response = api_client.post("/api/video/upload-chunk", files=files)
    logger.info(response.text)

    assert response.status_code == 400


@allure.title("Upload Chunk - Missing Recording ID")
@allure.description("Should return 400 when recordingId is missing.")
@pytest.mark.order(82)
def test_upload_chunk_missing_recording_id(api_client):
    with open(VIDEO_FILE_PATH, "rb") as file:
        files = {
            "videoChunks": ("recording.mp4", file, "video/mp4"),
        }

        response = api_client.post("/api/video/upload-chunk", files=files)
        logger.info(response.text)

    assert response.status_code == 400


@allure.title("Upload Chunk - Invalid File Type")
@allure.description("Should return 400 when file is not a supported format.")
@pytest.mark.order(83)
def test_upload_chunk_invalid_file_type(api_client):
    files = {
        "recordingId": (None, "session_1755516734335"),
        "videoChunks": ("not_a_video.txt", b"hello", "text/plain"),
    }

    response = api_client.post("/api/video/upload-chunk", files=files)
    logger.info(response.text)

    assert response.status_code == 400


@allure.title("Upload Chunk - SQL Injection in recordingId")
@allure.description("Should return 400 for suspicious recording ID input.")
@pytest.mark.order(84)
def test_upload_chunk_sql_injection(api_client):
    with open(VIDEO_FILE_PATH, "rb") as file:
        files = {
            "recordingId": (None, "'; DROP TABLE users_tbl;--"),
            "videoChunks": ("recording.mp4", file, "video/mp4"),
        }

        response = api_client.post("/api/video/upload-chunk", files=files)
        logger.info(response.text)

    assert response.status_code == 400


@allure.title("Upload Chunk - Empty File Upload")
@allure.description("Should return 400 when uploaded file is empty.")
@pytest.mark.order(85)
def test_upload_chunk_empty_file(api_client):
    files = {
        "recordingId": (None, "session_empty"),
        "videoChunks": ("empty.mp4", b"", "video/mp4"),
    }

    response = api_client.post("/api/video/upload-chunk", files=files)
    logger.info(response.text)

    assert response.status_code == 400


@allure.title("Upload Chunk - Invalid Auth Token")
@allure.description("Should return 401 or 403 if invalid token is used.")
@pytest.mark.order(86)
def test_upload_chunk_invalid_token(api_client):
    with open(VIDEO_FILE_PATH, "rb") as file:
        files = {
            "recordingId": (None, "session_auth_fail"),
            "videoChunks": ("recording.mp4", file, "video/mp4"),
        }

        headers = {"Authorization": "Bearer invalid_token"}

        response = api_client.post(
            "/api/video/upload-chunk", files=files, headers=headers
        )
        logger.info(response.text)

    assert response.status_code == 401
