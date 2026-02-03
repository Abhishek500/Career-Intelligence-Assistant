import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise RuntimeError("GEMINI_API_KEY not found")

genai.configure(api_key=api_key)


class GeminiClient:
    def __init__(self, model="gemini-3-flash-preview"):
        self.model_name = model
        self._model = None

    def _get_model(self):
        if self._model is None:
            self._model = genai.GenerativeModel(self.model_name)
        return self._model

    def generate(self, prompt: str) -> str:
        response = self._get_model().generate_content(
            prompt,
            generation_config={
                "temperature": 0.2,
                "max_output_tokens": 8192,  # Increased to 2048
            }
        )
        return response.text

    def extract(self, prompt: str, input_text: str) -> str:
        """Extract structured data from text using the given prompt."""
        full_prompt = f"{prompt}\n\nText to analyze:\n{input_text}"
        return self.generate(full_prompt)
