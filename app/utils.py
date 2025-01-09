import logging
from tenacity import retry, stop_after_attempt, wait_exponential
import requests

logger = logging.getLogger(__name__)

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=1, max=5))
def send_request_with_retry(method, url, **kwargs):
    """Sends a request using requests with retry logic."""
    try:
        response = method(url, **kwargs)
        response.raise_for_status()
        return response
    except requests.exceptions.RequestException as e:
        logger.error(f"Error during request to {url}: {e}")
        raise