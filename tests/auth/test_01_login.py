import pytest
import allure
import logging

logger = logging.getLogger(__name__)


@allure.title("Log in with valid credentials")
@allure.description(
    "Log in using valid email and password, and verify successful authentication."
)
@pytest.mark.order(1)
def test_login_success(api_client):
    logger.info("Logging in with valid credentials")

    payload = {
        "email": "jaishree9898@gmail.com",
        "password": "Admin@123",
    }
    headers = {"Content-Type": "application/json"}

    response = api_client.post("/api/auth/login", json=payload, headers=headers)
    logger.info(response.json())

    assert (
        response.status_code == 200
    ), f"Unexpected status code: {response.status_code}"
    response_json = response.json()
    data = response_json.get("data", {})
    access_token = data.get("accessToken")

    assert response_json["success"] == True
    assert response_json["message"] == "Login successful"
    assert access_token is not None, "Access token not found in response"
    assert isinstance(access_token, str), "Access token should be a string"

    logger.info(f"Login successful. Token: {access_token[:30]}...")


@allure.title("SQL Injection Attempt in Login")
@allure.description(
    "Attempt SQL injection in email and password fields and ensure input validation prevents it."
)
@pytest.mark.order(2)
def test_sql_injection_login(api_client):
    logger.info("Testing SQL injection in login credentials")

    payload = {
        "email": "' OR '1'='1",  # Invalid email format
        "password": "' OR '1'='1",
    }
    headers = {"Content-Type": "application/json"}

    response = api_client.post("/api/auth/login", json=payload, headers=headers)
    logger.info(response.json())

    # Expecting validation failure due to invalid email format
    assert (
        response.status_code == 400
    ), f"Expected status 400, got {response.status_code}. Response: {response.text}"

    data = response.json()
    assert data["success"] == False
    assert data["error"] == f'"email" must be a valid email'
    logger.info(
        "SQL injection attempt rejected due to input validation: %s",
        data["error"],
    )


@allure.title("Log in with invalid credentials")
@allure.description(
    "Attempt login using incorrect email and password and verify error response."
)
@pytest.mark.order(3)
def test_login_failure_invalid_credentials(api_client):
    logger.info("Logging in with invalid credentials")

    payload = {
        "email": "jaishree9898@gmail.com",
        "password": "qwertyuiop",
    }

    response = api_client.post("/api/auth/login", json=payload)
    logger.info(response.json())

    assert (
        response.status_code == 401
    ), f"Expected 401 Unauthorized, got {response.status_code}"

    data = response.json()
    assert data["success"] is False
    assert data["message"] == "Invalid email or password"
    assert data["error"] == "INVALID_CREDENTIALS"

    logger.info("Invalid credentials rejected correctly")


@allure.title("Log in with invalid or missing fields")
@allure.description(
    "Validate API error responses for malformed email or missing fields."
)
@pytest.mark.order(4)
@pytest.mark.parametrize(
    "payload, expected_error, description",
    [
        (
            {"email": "userattheratemaildotcom", "password": "qwertyuiop"},
            '"email" must be a valid email',
            "invalid email format",
        ),
        (
            {"password": "qwertyuiop"},
            '"email" is required',
            "missing email",
        ),
        (
            {"email": "qwertyuiop@sjx.com"},
            '"password" is required',
            "missing password",
        ),
    ],
)
def test_login_failure_validation_errors(
    api_client, payload, expected_error, description
):
    logger.info(f"Logging in with {description}")

    response = api_client.post("/api/auth/login", json=payload)
    logger.info(response.json())

    assert (
        response.status_code == 400
    ), f"Expected 400 Bad Request, got {response.status_code}"

    data = response.json()
    assert data["success"] is False
    assert data["error"] == expected_error

    logger.info(f"Validation error returned correctly for {description}")


@allure.title("Login with case-insensitive email")
@allure.description("Ensure login works with email in different casing.")
@pytest.mark.order(5)
def test_login_case_insensitive_email(api_client):
    payload = {"email": "JAISHREE9898@GMAIL.COM", "password": "Admin@123"}

    response = api_client.post("/api/auth/login", json=payload)
    logger.info(response.json())

    assert (
        response.status_code == 200
    ), f"Unexpected status code: {response.status_code}"

    data = response.json().get("data", {})
    access_token = data.get("accessToken")

    assert access_token is not None, "Access token not found in response"
    assert isinstance(access_token, str), "Access token should be a string"

    logger.info(f"Login successful. Token: {access_token[:30]}...")
    logger.info("validation message captured successfully!!")


@allure.title("Login with leading/trailing spaces in email")
@allure.description("Ensure email trimming is handled on the backend.")
@pytest.mark.order(6)
def test_login_email_with_spaces(api_client):
    payload = {"email": "   jaishree9898@gmail.com   ", "password": "Admin@123"}

    response = api_client.post("/api/auth/login", json=payload)
    logger.info(response.json())

    data = response.json()
    assert response.status_code == 400
    assert data["success"] == False
    assert data["error"] == f'"email" must be a valid email'
    logger.info("validation message captured successfully!!")


@allure.title("Login with both fields missing")
@allure.description("Ensure error returned when email and password are missing.")
@pytest.mark.order(7)
def test_login_both_fields_missing(api_client):
    response = api_client.post("/api/auth/login", json={})
    logger.info(response.json())

    assert response.status_code == 400
    assert response.json()["error"] == '"email" is required'
    logger.info("error message captured successfully!!")


@allure.title("Login with unregistered email")
@allure.description("Ensure login fails if the email is not registered.")
@pytest.mark.order(8)
def test_login_unregistered_email(api_client):
    payload = {"email": "notaregistereduser@example.com", "password": "SomePassword123"}

    response = api_client.post("/api/auth/login", json=payload)
    logger.info(response.json())

    assert response.status_code == 401
    assert response.json()["error"] == "INVALID_CREDENTIALS"
    logger.info("error message captured successfully!!")


@allure.title("Login with special characters in email")
@allure.description("Ensure special characters in email are handled properly.")
@pytest.mark.order(9)
def test_login_special_characters_in_email(api_client):
    payload = {"email": "we!rd&email+test@example.com", "password": "AnyPassword123"}

    response = api_client.post("/api/auth/login", json=payload)
    logger.info(response.json())

    assert response.status_code == 401
    assert response.json()["error"] == "INVALID_CREDENTIALS"
    logger.info("error message captured successfully!!")


@allure.title("SQL injection in password field only")
@allure.description("Ensure SQL injection in password does not work.")
@pytest.mark.order(10)
def test_sql_injection_in_password_only(api_client):
    payload = {"email": "jaishree9898@gmail.com", "password": "' OR '1'='1"}

    response = api_client.post("/api/auth/login", json=payload)
    logger.info(response.json())

    assert response.status_code == 401
    assert response.json()["error"] == "INVALID_CREDENTIALS"
    logger.info("error message captured successfully!!")
