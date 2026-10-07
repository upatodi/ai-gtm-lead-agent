"""
Client for interacting with the local Ollama LLM.
"""

import requests


OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "qwen2.5:3b-instruct"


def generate_response(prompt):
    """
    Sends a prompt to the local Ollama model
    and returns the generated response.
    """

    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False,
    }

    response = requests.post(
        OLLAMA_URL,
        json=payload,
        timeout=120,
    )

    response.raise_for_status()

    result = response.json()

    return result["response"]