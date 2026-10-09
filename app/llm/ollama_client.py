"""
Client for interacting with the local Ollama LLM.
"""

import requests


OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "qwen2.5:3b-instruct"


def generate_response(prompt, output_schema=None):
    """
    Sends a prompt to the local Ollama model.

    If output_schema is provided, Ollama is instructed
    to return JSON matching that schema.
    """

    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False,
    }

    if output_schema is not None:
        payload["format"] = output_schema

    response = requests.post(
        OLLAMA_URL,
        json=payload,
        timeout=120,
    )

    response.raise_for_status()

    result = response.json()

    return result["response"]