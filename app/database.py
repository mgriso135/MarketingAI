import psycopg2
import logging
from tenacity import retry, stop_after_attempt, wait_exponential
from config import Config

logger = logging.getLogger(__name__)


class Database:
    def __init__(self):
        self.db_url = Config.DATABASE_URL
        self.conn = None

    @retry(
        stop=stop_after_attempt(5), wait=wait_exponential(multiplier=1, min=2, max=10)
    )
    def connect(self):
        try:
            self.conn = psycopg2.connect(self.db_url)
            logger.info("Connected to PostgreSQL.")
        except psycopg2.Error as e:
            logger.error(f"Error connecting to PostgreSQL: {e}")
            raise

    def insert_social_post(self, content, social_media, scheduled_at):
        query = """
            INSERT INTO social_posts (content, social_media, scheduled_at)
            VALUES (%s, %s, %s);
        """
        try:
            cur = self.conn.cursor()
            cur.execute(query, (content, social_media, scheduled_at))
            self.conn.commit()
            logger.info(f"Inserted social post into database: {social_media}, {scheduled_at}")
            cur.close()
        except psycopg2.Error as e:
            logger.error(f"Error inserting into database: {e}")
            raise

    def close(self):
        if self.conn:
            self.conn.close()
            logger.info("PostgreSQL connection closed.")