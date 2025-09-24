import os
import pytest
import logging
import sys
from utils.api_client import APIClient
from utils.utils import generate_account_status_name

# 👇 Make sure the logs directory exists
os.makedirs("logs", exist_ok=True)

# ✅ Logging setup: log to both terminal and file
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(funcName)s:%(lineno)d - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),  # Terminal
        logging.FileHandler("logs/test.log", mode="w"),  # File (overwrites each run)
    ],
)
logger = logging.getLogger(__name__)


@pytest.fixture(scope="session")
def api_client():
    return APIClient()


@pytest.fixture(scope="session")
def auth_token(api_client):
    payload = {
        "email": "jaishree9898@gmail.com",
        "password": "Admin@123",
    }

    headers = {"Content-Type": "application/json"}
    response = api_client.post("/api/auth/login", json=payload, headers=headers)

    assert response.status_code == 200, f"Login failed: {response.text}"

    data = response.json().get("data", {})
    assert "accessToken" in data

    return data["accessToken"]


# -------------------- Test Data Fixtures --------------------


@pytest.fixture(scope="session")
def account_status_name():
    """Generates a shared account status value for all tests."""
    return generate_account_status_name()


# -------------------- Clean Allure Results & Reports --------------------


@pytest.hookimpl(tryfirst=True)
def pytest_sessionstart(session):
    """Clean up old Allure raw results and HTML report before test session starts."""
    for folder in ["allure-results"]:
        if os.path.exists(folder):
            try:
                for filename in os.listdir(folder):
                    file_path = os.path.join(folder, filename)
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)
                    elif os.path.isdir(file_path):
                        import shutil

                        shutil.rmtree(file_path)
                logger.info(f"Cleared contents of '{folder}'")
            except Exception as e:
                logger.warning(f"Failed to clear contents of '{folder}': {e}")
        else:
            os.makedirs(folder)
            logger.info(f"Created missing folder '{folder}'")
