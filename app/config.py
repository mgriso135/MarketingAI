import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    LINKEDIN_API_KEY = os.getenv("LINKEDIN_API_KEY")
    LINKEDIN_API_SECRET = os.getenv("LINKEDIN_API_SECRET")
    INSTAGRAM_API_KEY = os.getenv("INSTAGRAM_API_KEY")
    INSTAGRAM_API_SECRET = os.getenv("INSTAGRAM_API_SECRET")
    DATABASE_URL = os.getenv("DATABASE_URL")
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

    @staticmethod
    def check_required_variables():
        if not all(
            [
                Config.GOOGLE_API_KEY,
                Config.DATABASE_URL,
            ]
        ):
            raise ValueError("Missing required env variable.")