import pytest
import allure
import logging

logger = logging.getLogger(__name__)


@allure.title("View Video - Valid ID")
@allure.description("Should increment view count and return video data successfully.")
@pytest.mark.order(53)
def test_view_video_valid_id(api_client):
    i = 0
    response = api_client.get("/api/video/view/v2/90?key=2459595ca341cfbcb85f740fd4562827")
    logger.info(response.json())

    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["status"] == 200
    assert data["data"]["views"] == 1


@allure.title("View Video - Non-existent ID")
@allure.description("Should return 404 when video doesn't exist.")
@pytest.mark.order(54)
def test_view_video_non_existent_id(api_client):
    response = api_client.get("/api/video/view/v2/99999")
    logger.info(response.json())

    assert response.status_code == 404
    data = response.json()
    assert data["success"] is False
    assert data["message"] == "Video not found"


@allure.title("View Video - Invalid ID Format (string)")
@allure.description("Should return 400 or 422 for invalid ID type.")
@pytest.mark.order(55)
def test_view_video_invalid_id_format(api_client):
    response = api_client.get("/api/video/view/v2/abc")
    logger.info(response.json())

    assert response.status_code == 404
    data = response.json()
    assert data["success"] is False
    assert data["message"] == "Video not found"


@allure.title("View Video - Missing ID in Path")
@allure.description("Should return 404 or 405 when path param is missing.")
@pytest.mark.order(56)
def test_view_video_missing_id(api_client):
    response = api_client.get("/api/video/view/v2/")
    logger.info(response.text)

    assert response.status_code == 404
    data = response.json()
    assert data["success"] is False
    assert data["message"] == "Video not found"


@allure.title("View Video - SQL Injection in ID")
@allure.description("Should reject SQL injection-like input in path.")
@pytest.mark.order(57)
def test_view_video_sql_injection(api_client):
    malicious_id = "1 OR 1=1"
    response = api_client.get(f"/api/video/view/{malicious_id}")
    logger.info(response.text)

    assert response.status_code == 404
    data = response.json()
    assert data["success"] is False
    assert data["message"] == "Video not found"


@allure.title("View Video - With Auth Token (Owner)")
@allure.description("Should still allow to view but will not increment view count.")
@pytest.mark.order(58)
def test_view_video_guest_user(api_client, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = api_client.get("/api/video/view/v2/90", headers=headers)
    logger.info(response.json())

    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["message"] == "Video retrieved successfully"
    assert data["data"]["view_incremented"] is False
    assert data["data"]["user_authenticated"] is True


@allure.title("View Video - Zero or Negative ID")
@allure.description("Should handle edge case where ID is 0 or negative.")
@pytest.mark.order(59)
@pytest.mark.parametrize("video_id", [0, -1])
def test_view_video_zero_negative_id(api_client, video_id):
    response = api_client.get(f"/api/video/view/{video_id}")
    logger.info(response.text)

    assert response.status_code == 404
    data = response.json()
    assert data["success"] is False
    assert data["message"] == "Video not found"


@allure.title("View Video - XSS Injection in ID")
@allure.description("Send XSS-like script as ID and ensure it's handled safely.")
@pytest.mark.order(60)
def test_view_video_xss_injection(api_client):
    xss_id = "<script>alert(1)</script>"
    response = api_client.get(f"/api/video/view/{xss_id}")
    logger.info(response.text)

    assert response.status_code in [400, 404]
