import logging
import time
from datetime import datetime, timedelta
from config import Config
from content_planner import ContentPlanner
from content_generator import ContentGenerator
from social_media import SocialMedia
from database import Database
from simple_queue import SimpleQueue


def setup_logging():
    logging.basicConfig(
        level=Config.LOG_LEVEL,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )


def main():
    setup_logging()
    logger = logging.getLogger(__name__)
    Config.check_required_variables()

    queue = SimpleQueue("social_posts")
    db = Database()
    db.connect()

    planner = ContentPlanner()
    generator = ContentGenerator()
    social = SocialMedia()

    while True:
        content_ideas = planner.plan_content()
        for idea in content_ideas:
            linkedin_post = generator.generate_linkedin_post(idea)
            instagram_post = generator.generate_instagram_post(idea)

            if linkedin_post:
                success = social.post_linkedin(linkedin_post)
                if success:
                    now = datetime.now()
                    db.insert_social_post(linkedin_post, "linkedin", now)
                    queue.enqueue(f"LinkedIn post scheduled: {linkedin_post}")

            if instagram_post:
                success = social.post_instagram(instagram_post)
                if success:
                    now = datetime.now()
                    db.insert_social_post(instagram_post, "instagram", now)
                    queue.enqueue(f"Instagram post scheduled: {instagram_post}")

        time.sleep(60 * 60)  # Check every hour

    db.close()


if __name__ == "__main__":
    main()