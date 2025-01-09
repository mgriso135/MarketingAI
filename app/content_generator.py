import google.generativeai as genai
import logging
from config import Config

logger = logging.getLogger(__name__)


class ContentGenerator:
    def __init__(self):
        genai.configure(api_key=Config.GOOGLE_API_KEY)
        self.model = genai.GenerativeModel('gemini-pro')

    def generate_linkedin_post(self, idea):
        prompt = f"""
        Generate a short and engaging LinkedIn post based on the following idea.
        Do not mention any of the original authors or their website.
        Your goal is to promote our product.
        Keep the post under 500 characters.
        Idea: {idea}
        """
        try:
           response = self.model.generate_content(prompt)
           if response.text:
              return response.text
           else:
              logger.error("Could not generate linkedin post")
              return ""
        except Exception as e:
            logger.error(f"Error generating Linkedin post: {e}")
            return ""

    def generate_instagram_post(self, idea):
        prompt = f"""
        Generate a short and engaging Instagram post based on the following idea.
        Do not mention any of the original authors or their website.
        Your goal is to promote our product.
        Keep the post under 150 characters.
        Idea: {idea}
        """
        try:
           response = self.model.generate_content(prompt)
           if response.text:
              return response.text
           else:
              logger.error("Could not generate instagram post")
              return ""
        except Exception as e:
            logger.error(f"Error generating instagram post: {e}")
            return ""