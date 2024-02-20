import openai

from openai import OpenAI
from app.core.config import settings

client = OpenAI()

class OpenAIService:
    
    """Class that interacts with OpenAI API"""
    
    ## Contains all class methods for interacting with OpenAI API
    
    def __init__(self):
        self.api_key = settings.OPENAI_API_KEY
        openai.api_key = self.api_key
        self.model = "gpt-3.5-turbo"
        self.messages = [
            {"role": "system", "content" : "You are an AI assistant, skilled in explaining solutions in simple effective language."},
            {"role": "user", "content" : "How can I set up a new Trello project based on a project roadmap written in Notion?"}
        ]
        
    def process_chat_completion(self):
        return client.chat.completions.create(model=self.model, messages=self.messages)
    
    def extract_answer_from_response(self):
        pass
    
open_ai_service = OpenAIService()
# print(open_ai_service.process_chat_completion())
