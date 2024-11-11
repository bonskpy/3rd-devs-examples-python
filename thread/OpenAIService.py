import openai
import os

class OpenAIService:

    def __init__(self):
        self.openai = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def completion(self, messages: list[dict], model: str = "gpt-4o-mini", stream: bool = False):
        
        try:
            completion = self.openai.chat.completions.create(
                messages=messages,
                model=model,
                stream=stream
            )
            return completion.choices[0].message.content
        
        except openai.OpenAIError as e:
            raise Exception(f"OpenAI API error: {str(e)}")





