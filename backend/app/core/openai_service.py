import openai

from app.core.config import settings
from typing import Any, List
from openai.types.chat.chat_completion import ChatCompletion

class OpenAIService:

    """Class that interacts with OpenAI API"""

    def __init__(self, openai_api_key: str = settings.OPENAI_API_KEY, model: str = "gpt-4") -> None:
        self.model = model
        self.client = openai.OpenAI(api_key=openai_api_key)
    
    def get_response_to_request(self, request: str) -> str:
        messages = [
            {
                "role": "system",
                "content": "You are an AI assistant, skilled in explaining solutions in simple yet effective language.",
            },
            {"role": "user", "content": request},
        ]
        chat_completion = self._create_chat_completion_for_messages(messages)
        return self._extract_last_message_from_chat_completion(chat_completion)

    def _create_chat_completion_for_messages(self, messages: List) -> ChatCompletion:
        try:
            chat_completion = self.client.chat.completions.create(model=self.model, messages=messages)
            return chat_completion
        except openai.APIConnectionError as e:
            print("The server could not be reached")
            print(e.__cause__)
        except openai.RateLimitError as e:
            print("A 429 status code was received; we should back off a bit.")
        except openai.APIStatusError as e:
            print("Another non-200-range status code was received")
            print(e.status_code)
            print(e.response)

    def _extract_last_message_from_chat_completion(self, chat_completion) -> str:
        return chat_completion.choices[0].message.content


openai_service = OpenAIService()
