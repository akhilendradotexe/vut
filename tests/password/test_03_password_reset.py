import pytest
import allure
import logging
from time import sleep

logger = logging.getLogger(__name__)


@allure.title("Reset Password - Field Validation Scenarios")
@allure.description(
    "Covers cases such as missing fields, password length issues, mismatched confirmPassword, and invalid reset token and get respective errors."
)
@pytest.mark.order(27)
@pytest.mark.parametrize(
    "payload, expected_status, expected_error, description",
    [
        (
            {"confirmPassword": "Password@123"},  # Missing password
            400,
            "New password is required",
            "Missing password",
        ),
        (
            {"password": "Password@123"},  # Missing confirmPassword
            400,
            "Confirm password is required",
            "Missing confirmPassword",
        ),
        (
            {"password": "short1", "confirmPassword": "short1"},
            400,
            "New password must be at least 8 characters long",
            "Password too short",
        ),
        (
            {"password": "A" * 130 + "1!", "confirmPassword": "A" * 130 + "1!"},
            400,
            "New password must not exceed 128 characters",
            "Password too long",
        ),
        (
            {"password": "Password@123", "confirmPassword": "Different@123"},
            400,
            "Confirm password does not match new password",
            "Mismatched confirmPassword",
        ),
    ],
)
def test_password_reset_negative_cases(
    api_client, auth_token, payload, expected_status, expected_error, description
):
    logger.info(f"Testing password reset: {description}")

    headers = {
        "Authorization": f"Bearer {auth_token}",
        "Content-Type": "application/json",
    }

    response = api_client.post("/api/password/reset", json=payload, headers=headers)
    logger.info(response.json())

    assert (
        response.status_code == expected_status
    ), f"Expected {expected_status}, got {response.status_code}"

    data = response.json()
    assert data["success"] is False
    assert expected_error in data.get("error", data.get("message", ""))

    logger.info(
        f"Negative test '{description}' passed, error message captured successfully!!"
    )


@allure.title("Reset Password - Expired or Invalid Token")
@allure.description(
    "Verify that reset password fails with an expired or malformed token."
)
@pytest.mark.order(28)
def test_password_reset_invalid_token(api_client):
    logger.info("Testing reset password with invalid/expired token")

    payload = {
        "password": "ValidPass@123",
        "confirmPassword": "ValidPass@123",
    }

    headers = {
        "Authorization": "Bearer invalid_or_expired_token_here",
        "Content-Type": "application/json",
    }

    response = api_client.post("/api/password/reset", json=payload, headers=headers)
    logger.info(response.json())

    assert response.status_code == 401
    data = response.json()
    assert data["success"] is False
    assert data["message"] == "Invalid or expired token"
    logger.info("validation message captured successfully!!")
