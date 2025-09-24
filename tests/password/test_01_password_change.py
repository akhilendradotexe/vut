import pytest
import allure
import logging

logger = logging.getLogger(__name__)


@allure.title("Change Password")
@allure.description(
    "Change Password by entering correct previous password and verify success."
)
@pytest.mark.order(11)
def test_password_change(api_client, auth_token):
    logger.info("changing password...")
    payload = {
        "currentPassword": "Admin@123",
        "newPassword": "Password@123",
        "confirmPassword": "Password@123",
    }
    headers = {
        "Authorization": f"Bearer {auth_token}",
        "Content-Type": "application/json",
    }
    response = api_client.post("/api/password/change", json=payload, headers=headers)
    logger.info(response.json())
    assert response.status_code == 200, "Expected OK"

    data = response.json()

    assert data["success"] == True
    assert data["message"] == "Password updated successfully"
    logger.info(
        "passsword changed successfully reverting back to the old password for smooth login process"
    )
    payload = {
        "currentPassword": "Password@123",
        "newPassword": "Admin@123",
        "confirmPassword": "Admin@123",
    }
    headers = {
        "Authorization": f"Bearer {auth_token}",
        "Content-Type": "application/json",
    }
    response = api_client.post("/api/password/change", json=payload, headers=headers)
    assert response.status_code == 200, "Expected OK"

    data = response.json()

    assert data["success"] == True
    assert data["message"] == "Password updated successfully"
    logger.info("password updated successfully!!")


@allure.title("Change Password - Incorrect Current Password")
@allure.description(
    "Attempt to change the password by providing an incorrect current password and Verify failure response."
)
@pytest.mark.order(12)
def test_password_change_wrong_current_password(api_client, auth_token):
    logger.info("Attempting to change password with incorrect current password...")

    payload = {
        "currentPassword": "WrongPassword@123",  # Incorrect current password
        "newPassword": "NewPassword@123",
        "confirmPassword": "NewPassword@123",
    }
    headers = {
        "Authorization": f"Bearer {auth_token}",
        "Content-Type": "application/json",
    }

    response = api_client.post("/api/password/change", json=payload, headers=headers)
    logger.info(response.json())

    # Expecting failure, likely a 400
    assert response.status_code == 400, "Expected failure status code 401"

    data = response.json()

    assert data["success"] == False
    assert data["message"] == "Current Password is incorrect"
    logger.info("validation message captured successfully!!")


@allure.title("Change Password - Mismatch New & Current Password")
@allure.description(
    "Attempt to change the password by providing an incorrect current password and Verify failure response."
)
@pytest.mark.order(13)
def test_password_change_mismatch_new_and_current_password(api_client, auth_token):
    logger.info("Attempting to change password with incorrect current password...")

    payload = {
        "currentPassword": "Admin@123",
        "newPassword": "NewPassword@123",
        "confirmPassword": "NewPassword@1234",
    }
    headers = {
        "Authorization": f"Bearer {auth_token}",
        "Content-Type": "application/json",
    }

    response = api_client.post("/api/password/change", json=payload, headers=headers)
    logger.info(response.json())

    # Expecting failure, likely a 400
    assert response.status_code == 400, "Expected failure status code 400"

    data = response.json()

    assert data["success"] == False
    assert data["error"] == "Confirm password does not match new password"
    logger.info("validation message captured successfully!!")


@allure.title("Change Password - Missing Required Fields")
@allure.description(
    "Attempt to change password with different required fields missing. "
    "Verify that API returns appropriate error response for each case."
)
@pytest.mark.order(14)
@pytest.mark.parametrize(
    "payload, missing_field",
    [
        (  # Missing currentPassword
            {
                "newPassword": "NewPassword@123",
                "confirmPassword": "NewPassword@123",
            },
            "Current password",
        ),
        (  # Missing newPassword
            {
                "currentPassword": "Admin@123",
                "confirmPassword": "NewPassword@123",
            },
            "New password",
        ),
        (  # Missing confirmPassword
            {
                "currentPassword": "Admin@123",
                "newPassword": "NewPassword@123",
            },
            "Confirm password",
        ),
        (  # All fields missing
            {},
            "Current password",
        ),
    ],
)
def test_password_change_missing_fields(api_client, auth_token, payload, missing_field):
    logger.info(f"Testing missing field: {missing_field}")

    headers = {
        "Authorization": f"Bearer {auth_token}",
        "Content-Type": "application/json",
    }

    response = api_client.post("/api/password/change", json=payload, headers=headers)
    logger.info(response.json())

    # API is expected to return a 400 Bad Request or similar
    assert response.status_code == 400, "Expected failure status code (400)"

    data = response.json()
    assert data["success"] == False

    # You can refine the message assertion if your API provides specific error messages
    assert data["error"] == f"{missing_field} is required"
    logger.info("validation message captured successfully!!")


@allure.title("Change Password - No Authorization Token")
@allure.description(
    "Attempt to change the password without providing an Authorization token. "
    "Verify that the API returns a 401 Unauthorized response."
)
@pytest.mark.order(15)
def test_password_change_no_auth_token(api_client):
    logger.info("Attempting to change password without auth token...")

    payload = {
        "currentPassword": "Admin@123",
        "newPassword": "NewPassword@123",
        "confirmPassword": "NewPassword@123",
    }

    headers = {
        "Content-Type": "application/json",  # No Authorization header
    }

    response = api_client.post("/api/password/change", json=payload, headers=headers)
    logger.info(f"Response status code: {response.status_code}")
    logger.info(response.json())

    # Expect 401 Unauthorized
    assert response.status_code == 401, "Expected 401 Unauthorized"

    data = response.json()
    assert data["success"] == False
    assert data["error"] == "Authorization token missing or invalid."
    logger.info("error message captured successfully!!")


@allure.title("Change Password - New Password Length Validation")
@allure.description("Ensure password must be between 8 and 128 characters.")
@pytest.mark.order(16)
@pytest.mark.parametrize(
    "new_password, description,message",
    [
        ("Short1!", "too short", "New password must be at least 8 characters long"),
        (
            "A" * 129 + "1!",
            "too long",
            "New password must not exceed 128 characters",
        ),
    ],
)
def test_password_change_invalid_length(
    api_client, auth_token, new_password, description, message
):
    logger.info(f"Testing password change with {description} password")

    payload = {
        "currentPassword": "Admin@123",
        "newPassword": new_password,
        "confirmPassword": new_password,
    }

    headers = {
        "Authorization": f"Bearer {auth_token}",
        "Content-Type": "application/json",
    }

    response = api_client.post("/api/password/change", json=payload, headers=headers)
    logger.info(response.json())
    data = response.json()
    assert response.status_code == 400
    assert data["success"] == False
    assert data["error"] == message
    logger.info("validation message captured successfully!!")


@allure.title("Change Password - Invalid or Expired Token")
@allure.description("Verify password change fails with expired/invalid token.")
@pytest.mark.order(17)
def test_password_change_invalid_token(api_client):
    logger.info("Attempting password change with invalid token")

    payload = {
        "currentPassword": "Admin@123",
        "newPassword": "Password@1234",
        "confirmPassword": "Password@1234",
    }

    headers = {
        "Authorization": "Bearer invalid.or.expired.token",
        "Content-Type": "application/json",
    }

    response = api_client.post("/api/password/change", json=payload, headers=headers)
    logger.info(response.json())
    data = response.json()

    assert response.status_code == 401
    assert data["success"] == False
    assert data["error"] == "Invalid or expired token."
    logger.info("error message captured successfully!!")


@allure.title("Change Password - SQL Injection Attempt")
@allure.description("Ensure password change blocks SQL injection inputs.")
@pytest.mark.order(18)
def test_password_change_sql_injection(api_client, auth_token):
    logger.info("Testing SQL injection attempt in password fields")

    injection_string = "' OR '1'='1"

    payload = {
        "currentPassword": injection_string,
        "newPassword": injection_string,
        "confirmPassword": injection_string,
    }

    headers = {
        "Authorization": f"Bearer {auth_token}",
        "Content-Type": "application/json",
    }

    response = api_client.post("/api/password/change", json=payload, headers=headers)
    logger.info(response.json())
    data = response.json()

    assert response.status_code == 400
    assert data["success"] == False
    assert (
        data["error"] == "New password must contain at least one lowercase letter (a-z)"
    )
    logger.info("validation message captured successfully!!")
