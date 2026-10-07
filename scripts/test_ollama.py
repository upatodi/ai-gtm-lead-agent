"""
Tests the connection between Python and the local Ollama model.
"""

from app.llm.ollama_client import generate_response


prompt = """
Return a short greeting confirming that you are a local AI model.
"""


response = generate_response(prompt)

print("=== OLLAMA RESPONSE ===")
print(response)