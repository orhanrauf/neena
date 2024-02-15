import openai

from app.core.config import settings

class OpenAIService:
    
    """Class that interacts with OpenAI API"""
    
    ## Contains all class methods for interacting with OpenAI API
    
    def __init__(self):
        self.api_key = settings.OPENAI_API_KEY
        openai.api_key = self.api_key
        # adjust however necessary
        
    def method_that_allows_for_talking_to_openai():
        pass
    
    pass

open_ai_service = OpenAIService()