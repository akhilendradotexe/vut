import pytest
import allure
import logging

logger = logging.getLogger(__name__)


@allure.title("Get Video by ID - Valid ID")
@allure.description(
    "Successfully retrieve video by providing a valid video ID in the path."
)
@pytest.mark.order(46)
def test_get_video_by_valid_id(api_client, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = api_client.get(f"/api/video/{90}", headers=headers)
    logger.info(response.json())

    assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}"
    data = response.json()
    assert data["success"] is True
    assert data["status"] == 200
    assert data["message"] == "Video retrieved successfully"
    assert data["data"]["video_id"] == 90


@allure.title("Get Video by ID - Non-Existent ID")
@allure.description(
    "Requesting a video ID that does not exist should return a 404 Not Found."
)
@pytest.mark.order(47)
def test_get_video_non_existent_id(api_client, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = api_client.get(f"/api/video/{99999}", headers=headers)
    logger.info(response.json())

    assert response.status_code == 404
    data = response.json()
    assert data["success"] is False
    assert data["status"] == 404
    assert data["message"] == "Video not found"


@allure.title("Get Video by ID - Invalid ID Format")
@allure.description(
    "Using a non-integer (string) as video ID should return 400 or 422 depending on validation."
)
@pytest.mark.order(48)
def test_get_video_invalid_id_format(api_client, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = api_client.get("/api/video/invalid-id", headers=headers)
    logger.info(response.json())

    data = response.json()
    assert data["success"] is False
    assert data["status"] == 404
    assert data["message"] == "Video not found"


@allure.title("Get Video by ID - Missing ID")
@allure.description(
    "Omitting the video ID from the path should result in a 404 due to malformed URL."
)
@pytest.mark.order(49)
def test_get_video_missing_id(api_client, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = api_client.get("/api/video/", headers=headers)
    logger.info(response.text)

    assert response.status_code == 404


@allure.title("Get Video by ID - Missing Auth Token")
@allure.description("Ensure the API rejects requests without an Authorization header.")
@pytest.mark.order(50)
def test_get_video_missing_auth_token(api_client):
    response = api_client.get("/api/video/90")  # No headers
    logger.info(response.json())

    assert response.status_code == 401
    data = response.json()
    assert data["error"] == "Authorization token missing or invalid."


@allure.title("Get Video by ID - Invalid Auth Token")
@allure.description("Ensure the API rejects requests with an invalid Bearer token.")
@pytest.mark.order(51)
def test_get_video_invalid_auth_token(api_client):
    headers = {"Authorization": "Bearer invalid.token.here"}
    response = api_client.get("/api/video/90", headers=headers)
    logger.info(response.json())

    assert response.status_code == 401
    data = response.json()
    assert data["error"] == "Invalid or expired token."


@allure.title("Get Video by ID - SQL Injection Attempt")
@allure.description("Ensure SQL injection strings in the ID are rejected.")
@pytest.mark.order(52)
def test_get_video_sql_injection_in_id(api_client, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    malicious_id = "1 OR 1=1"  # Or "1'; DROP TABLE videos; --"
    response = api_client.get(f"/api/video/{malicious_id}", headers=headers)
    logger.info(response.json())

    assert response.status_code == 404
    data = response.json()
    assert data["message"] == "Video not found"
