"""
@Author: ShuttleAI
@Version: 2
@Date: 2-7-2024
"""
import httpx
from .log import log

class ShuttleClient:
    def __init__(self, api_key):
        self.api_key = api_key 
        self.base_url = "https://api.shuttleai.app/v1"
    
    @property
    def models(self):
        try:
            url = f"{self.base_url}/models"
            response = httpx.get(url, timeout=60)
            return response.json()
        except Exception as e:
            log.error(f"[ShuttleAI] Error: {e}")

    def chat_completion(self, model, messages, stream=False, plain=False, **kwargs):
     try:
        url = f"{self.base_url}/chat/completions"
        headers = {"Authorization": f"Bearer {self.api_key}"}

        if plain: # If plain_message is True, convert the plain message to the structured format
            messages = [{"role": "user", "content": messages}]

        data = {
            "model": model,
            "messages": messages,
            "stream": stream,
        }

        for key, value in kwargs.items():
                data[key] = value if value is not None else data[key]  # Set default value if None

        response = httpx.post(url, json=data, headers=headers, timeout=60)
        return response.json() if not stream else response.text
     except Exception as e:
         log.error(f"[ShuttleAI] Error: {e}")

    def images_generations(self, model, prompt, n=1):
        try:
            url = f"{self.base_url}/images/generations"
            headers = {"Authorization": f"Bearer {self.api_key}"}
            data = {
                "model": model,
                "prompt": prompt,
                "n": n
            }
            response = httpx.post(url, json=data, headers=headers, timeout=60)
            return response.json()
        except Exception as e:
            log.error(f"[ShuttleAI] Error: {e}")
    
    def audio_generations(self, input, voice, model: str = "ElevenLabs",):
        try:
            url = f"{self.base_url}/audio/generations"
            headers = {"Authorization": f"Bearer {self.api_key}"}
            data = {
                "model": model,
                "input": input,
                "voice": voice
            }
            response = httpx.post(url, json=data, headers=headers, timeout=60)
            return response.json()
        except Exception as e:
            log.error(f"[ShuttleAI] Error: {e}")