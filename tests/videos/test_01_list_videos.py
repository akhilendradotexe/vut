import pytest
import allure
import logging

logger = logging.getLogger(__name__)


@allure.title("List Videos - Default Pagination (No Query Params)")
@allure.description(
    "Verify that the API returns default pagination with page=1 and limit=10 when no query params are passed."
)
@pytest.mark.order(29)
def test_video_list_default_pagination(api_client, auth_token):
    logger.info("Listing videos with default params")
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = api_client.get("/api/video/list", headers=headers)
    logger.info(response.json())

    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["page"] == 1
    assert data["limit"] == 10
    assert isinstance(data["data"], list)
    logger.info("Default pagination verified successfully.")


@allure.title("List Videos - Pagination Params (page=2, limit=5)")
@allure.description(
    "Verify that the API returns correct data when pagination params page=2 and limit=5 are passed."
)
@pytest.mark.order(30)
def test_video_list_with_pagination(api_client, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = api_client.get("/api/video/list?page=2&limit=5", headers=headers)
    logger.info(response.json())

    assert response.status_code == 200
    data = response.json()
    assert data["page"] == 2
    assert data["limit"] == 5


@allure.title("List Videos - Filter by Status")
@allure.description(
    "Verify that the API correctly filters videos by status (e.g., completed)."
)
@pytest.mark.order(31)
def test_video_list_filter_status(api_client, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = api_client.get("/api/video/list?status=completed", headers=headers)
    logger.info(response.json())

    assert response.status_code == 200
    data = response.json()
    for video in data["data"]:
        assert video["status"] == "completed"


@allure.title("List Videos - Filter by Video ID")
@allure.description(
    "Verify that the API returns only the video matching the specified video_id."
)
@pytest.mark.order(32)
def test_video_list_filter_video_id(api_client, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    test_video_id = 26
    response = api_client.get(
        f"/api/video/list?video_id={test_video_id}", headers=headers
    )
    logger.info(response.json())

    assert response.status_code == 200
    data = response.json()
    for video in data["data"]:
        assert video["video_id"] == test_video_id


@allure.title("List Videos - Search by Title")
@allure.description("Verify that the API supports searching videos by title.")
@pytest.mark.order(33)
def test_video_list_search(api_client, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = api_client.get(f"/api/video/list?search=My Test Video", headers=headers)
    logger.info(response.json())

    assert response.status_code == 200
    data = response.json()
    video_data = data["data"]
    assert video_data[0]["title"] == "My Test Video"


@allure.title("List Videos - Filter by Created Date Range")
@allure.description(
    "Verify that the API filters videos by created_from and created_to timestamp range."
)
@pytest.mark.order(34)
def test_video_list_date_range_filter(api_client, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    # These timestamps need to be updated based on actual test data
    from_ts = "2025-08-19"  # e.g. '2025-08-20T04:57:00+00:00'
    to_ts = "2025-08-17"  # e.g. '2025-08-20T05:57:00+00:00'
    response = api_client.get(
        f"/api/video/list?created_from={from_ts}&created_to={to_ts}", headers=headers
    )
    logger.info(response.json())

    assert response.status_code == 200
    data = response.json()
    for video in data["data"]:
        assert from_ts <= video["created_date"] <= to_ts


@allure.title("List Videos - Filter by Views Range")
@allure.description(
    "Verify that the API filters videos based on views_min and views_max."
)
@pytest.mark.order(35)
def test_video_list_views_filter(api_client, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = api_client.get(
        "/api/video/list?views_min=0&views_max=10", headers=headers
    )
    logger.info(response.json())

    assert response.status_code == 200
    data = response.json()
    for video in data["data"]:
        assert 0 <= video["views"] <= 10
