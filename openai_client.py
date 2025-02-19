# openai_client.py

import re
import openai
from nicegui import ui
from logging_utils import log_message, ConsoleColor, trace


OPENAI_API_KEY_REGEX = r'^sk(?:-proj)?-[A-Za-z0-9_-]+$'

class OpenAIClient:
    def __init__(self):
        self.api_key = None

    def set_api_key(self, key: str):
        """Set the OpenAI API key with regex validation."""
        try:
            if not re.match(OPENAI_API_KEY_REGEX, key):
                ui.notify("Invalid OpenAI API key format.", color="red", position="top")
                return
            self.api_key = key
            openai.api_key = key
            ui.notify("API key set successfully!", color="green", position="top")
            log_message("API key validated and set.", session_id="GLOBAL")
        except Exception as e:
            log_message(f"Error in set_api_key: {e}", level="error", session_id="GLOBAL")
            ui.notify("Failed to set API key.", color="red", position="top")

    def get_response(self, prompt: str, role: str = "user", model: str = "gpt-4",
                     temperature: float = 0.7, max_tokens: int = 1000) -> str:
        """Call OpenAI API with a prompt message using the new ChatCompletion interface."""
        try:
            if not self.api_key:
                raise ValueError("OpenAI API key has not been set!")
            log_message("Sending prompt to OpenAI API...", color=ConsoleColor.PURPLE)
            response =  openai.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": "You are a marketing and strategic content expert."},
                    {"role": role, "content": prompt}
                ],
                temperature=temperature,
                max_tokens=max_tokens
            )
            result = response.choices[0].message.content.strip()
            log_message("Received response from OpenAI API.", color=ConsoleColor.GREEN)
            return result
        except Exception as e:
            log_message(f"Error in get_response: {e}", level="error", color=ConsoleColor.RED)
            return ""
