import pytest
import allure
import logging
from time import sleep

logger = logging.getLogger(__name__)


@allure.title("Forgot Password - Valid Email")
@allure.description(
    "Trigger password reset link by providing a registered email address."
)
@pytest.mark.order(19)
def test_password_forgot_success(api_client, auth_token):
    logger.info("Requesting password reset link with valid email")

    payload = {"email": "jaishree9898@gmail.com"}

    headers = {
        "Authorization": f"Bearer {auth_token}",
        "Content-Type": "application/json",
    }

    response = api_client.post("/api/password/forgot", json=payload, headers=headers)
    logger.info(response.json())

    assert (
        response.status_code == 201
    ), f"Expected 201 Created, got {response.status_code}"

    data = response.json()
    assert data["success"] is True
    assert data["message"] == "Password reset link sent"

    logger.info("Password reset link sent successfully.")


@allure.title("Forgot Password - Unregistered Email")
@allure.description(
    "Attempt to trigger a password reset using an unregistered email. Should return 404 Not Found."
)
@pytest.mark.order(20)
def test_password_forgot_unregistered_email(api_client, auth_token):
    logger.info("Requesting password reset with an unregistered email")

    payload = {"email": "jaishree@gmail.com"}

    headers = {
        "Authorization": f"Bearer {auth_token}",
        "Content-Type": "application/json",
    }

    response = api_client.post("/api/password/forgot", json=payload, headers=headers)
    logger.info(response.json())

    assert (
        response.status_code == 404
    ), f"Expected 404 Not Found, got {response.status_code}"

    data = response.json()
    assert data["success"] is False
    assert data["message"] == "User not found"

    logger.info("Unregistered email correctly returned 404 Not Found.")


@allure.title("Forgot Password - Invalid Email Format")
@allure.description(
    "Verify that the API returns a 400 error for an invalid email format."
)
@pytest.mark.order(21)
def test_password_forgot_invalid_email_format(api_client, auth_token):
    payload = {"email": "invalid-email-format"}
    headers = {
        "Authorization": f"Bearer {auth_token}",
        "Content-Type": "application/json",
    }
    response = api_client.post("/api/password/forgot", json=payload, headers=headers)
    logger.info(response.json())

    assert response.status_code == 400
    data = response.json()
    assert data["success"] is False
    assert data["error"] == '"email" must be a valid email'
    logger.info("validation error captured successfully!!.")


@allure.title("Forgot Password - Missing Email Field")
@allure.description("Verify the API returns a 400 error when email is missing.")
@pytest.mark.order(22)
def test_password_forgot_missing_email_field(api_client, auth_token):
    payload = {}  # No email
    headers = {
        "Authorization": f"Bearer {auth_token}",
        "Content-Type": "application/json",
    }
    response = api_client.post("/api/password/forgot", json=payload, headers=headers)
    logger.info(response.json())

    assert response.status_code == 400
    data = response.json()
    assert data["success"] is False
    assert data["error"] == '"email" is required'
    logger.info("error message captured successfully!!")


@allure.title("Forgot Password - Empty Email String")
@allure.description("Verify the API handles empty email strings gracefully.")
@pytest.mark.order(23)
def test_password_forgot_empty_email_string(api_client, auth_token):
    payload = {"email": ""}
    headers = {
        "Authorization": f"Bearer {auth_token}",
        "Content-Type": "application/json",
    }
    response = api_client.post("/api/password/forgot", json=payload, headers=headers)
    logger.info(response.json())

    assert response.status_code == 400
    data = response.json()
    assert data["success"] is False
    assert data["error"] == '"email" is not allowed to be empty'
    logger.info("validation message captured successfully!!")


@allure.title("Forgot Password - SQL Injection in Email")
@allure.description("Verify the API rejects SQL injection attempts in the email field.")
@pytest.mark.order(24)
def test_password_forgot_sql_injection(api_client, auth_token):
    payload = {"email": "' OR '1'='1"}
    headers = {
        "Authorization": f"Bearer {auth_token}",
        "Content-Type": "application/json",
    }
    response = api_client.post("/api/password/forgot", json=payload, headers=headers)
    logger.info(response.json())

    assert response.status_code == 400
    data = response.json()
    assert data["success"] is False
    assert data["error"] == '"email" must be a valid email'
    logger.info("validation message captured successfully!!")


@allure.title("Forgot Password - Case Insensitive Email")
@allure.description("Verify the system handles uppercase emails (case-insensitive).")
@pytest.mark.order(25)
def test_password_forgot_case_insensitive_email(api_client, auth_token):
    payload = {"email": "JAISHREE9898@GMAIL.COM"}
    headers = {
        "Authorization": f"Bearer {auth_token}",
        "Content-Type": "application/json",
    }
    response = api_client.post("/api/password/forgot", json=payload, headers=headers)
    logger.info(response.json())

    assert response.status_code == 201
    data = response.json()
    assert data["success"] is True
    assert data["message"] == "Password reset link sent"
    logger.info("link sent successfully!!")


@allure.title("Forgot Password - Special Characters in Email")
@allure.description("Verify the system rejects emails with invalid special characters.")
@pytest.mark.order(26)
def test_password_forgot_special_characters_email(api_client, auth_token):
    payload = {"email": "user!@gmail.com"}
    headers = {
        "Authorization": f"Bearer {auth_token}",
        "Content-Type": "application/json",
    }
    response = api_client.post("/api/password/forgot", json=payload, headers=headers)
    logger.info(response.json())

    assert response.status_code == 404
    data = response.json()
    assert data["success"] is False
    assert data["message"] == "User not found"
    logger.info("error message captured successfully!!")
