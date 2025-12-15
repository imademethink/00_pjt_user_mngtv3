
import requests
from utils.logger import get_logger

logger = get_logger(__name__)

class APIClient:
    def __init__(self, base_url, timeout, headers):
        self.base_url = base_url
        self.timeout = timeout
        self.headers = headers

    def call(self, method, endpoint, **kwargs):
        url = f"{self.base_url}{endpoint}"
        logger.info(f"{method} {url}")
        if 'json' in kwargs:
            logger.info(f"Request Body: {kwargs['json']}")
        if 'params' in kwargs:
            logger.info(f"Query Params: {kwargs['params']}")

        resp = requests.request(
            method,
            url,
            timeout=self.timeout,
            headers=self.headers,
            **kwargs
        )
        logger.info(f"Response Code: {resp.status_code}")
        logger.info(f"Response Body: {resp.text}")
        return resp
