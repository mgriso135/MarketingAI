import requests
import logging
from datetime import datetime
from config import Config
from tenacity import retry, stop_after_attempt, wait_exponential

logger = logging.getLogger(__name__)


class SocialMedia:
    def __init__(self):
        self.linkedin_api_key = Config.LINKEDIN_API_KEY
        self.linkedin_api_secret = Config.LINKEDIN_API_SECRET
        self.instagram_api_key = Config.INSTAGRAM_API_KEY
        self.instagram_api_secret = Config.INSTAGRAM_API_SECRET

    @retry(
        stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=5)
    )
    def post_linkedin(self, content):
        # Dummy LinkedIn posting (Replace this with actual LinkedIn API interaction)
        logger.info(f"LinkedIn Posting: {content}")
        return True

    @retry(
        stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=5)
    )
    def post_instagram(self, content):
        # Dummy Instagram posting (Replace this with actual Instagram API interaction)
        logger.info(f"Instagram Posting: {content}")
        return True