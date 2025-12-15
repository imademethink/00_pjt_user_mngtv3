
import pytest
from config.config import BASE_URL, TIMEOUT, HEADERS
from core.api_client import APIClient

@pytest.fixture(scope="session")
def api_client():
    return APIClient(BASE_URL, TIMEOUT, HEADERS)

@pytest.fixture(scope="session")
def context():
    return {}
