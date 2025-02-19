# openai_client.py

import re
import openai
from tracing import create_span
from nicegui import ui
from logging_utils import log_message, ConsoleColor
from opentelemetry import trace

OPENAI_API_KEY_REGEX = r'^sk(?:-proj)?-[A-Za-z0-9_-]+$'

class OpenAIClient:
    def __init__(self):
        self.api_key = None
        self.tracer = trace.get_tracer(__name__)

    @create_span("set_api_key")
    def set_api_key(self, key: str):
        """Set the OpenAI API key with regex validation."""
        try:
            with self.tracer.start_as_current_span("validate_api_key") as span:
                span.set_attribute("key_length", len(key))
                if not re.match(OPENAI_API_KEY_REGEX, key):
                    ui.notify("Invalid OpenAI API key format.", color="red", position="top")
                    span.set_attribute("validation_success", False)
                    return
                span.set_attribute("validation_success", True)

            self.api_key = key
            openai.api_key = key
            ui.notify("API key set successfully!", color="green", position="top")
            log_message("API key validated and set.", session_id="GLOBAL")
        except Exception as e:
            log_message(f"Error in set_api_key: {e}", level="error", session_id="GLOBAL")
            ui.notify("Failed to set API key.", color="red", position="top")

    @create_span("get_response")
    async def get_response(self, prompt: str, role: str = "user", model: str = "gpt-4",
                     temperature: float = 0.7, max_tokens: int = 1000) -> str:
        """Call OpenAI API with a prompt message using the new ChatCompletion interface."""
        try:
            if not self.api_key:
                raise ValueError("OpenAI API key has not been set!")

            # Tracer les paramètres de la requête
            with self.tracer.start_as_current_span("prepare_request") as span:
                span.set_attribute("model", model)
                span.set_attribute("temperature", temperature)
                span.set_attribute("max_tokens", max_tokens)
                span.set_attribute("prompt_length", len(prompt))
                log_message("Sending prompt to OpenAI API...", color=ConsoleColor.PURPLE)

            # Tracer l'appel API
            with self.tracer.start_as_current_span("api_call") as span:
                response = openai.chat.completions.create(
                    model=model,
                    messages=[
                        {"role": "system", "content": "You are a marketing and strategic content expert."},
                        {"role": role, "content": prompt}
                    ],
                    temperature=temperature,
                    max_tokens=max_tokens
                )
                result = response.choices[0].message.content.strip()
                span.set_attribute("response_length", len(result))
                log_message("Received response from OpenAI API.", color=ConsoleColor.GREEN)
                return result

        except Exception as e:
            # Tracer les erreurs
            with self.tracer.start_as_current_span("error_handling") as span:
                span.set_attribute("error_type", type(e).__name__)
                span.set_attribute("error_message", str(e))
                log_message(f"Error in get_response: {e}", level="error", color=ConsoleColor.RED)
                return ""