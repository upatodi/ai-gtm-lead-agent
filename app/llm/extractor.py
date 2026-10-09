"""
Extracts structured lead information using the local Ollama LLM.
"""

import json

from app.llm.ollama_client import generate_response
from app.llm.schemas import LeadProfile


def extract_lead_profile(inquiry):
    """
    Uses the local LLM to extract structured information
    from a real estate lead inquiry.
    """

    prompt = f"""
Extract the real estate lead information from the inquiry below.

Return the information according to the provided JSON schema.

Important:
- Extract information from the inquiry.
- Do not invent information that is not present.
- If information is not mentioned, use null.
- locations may contain multiple locations.
- budget_max_lakh must be expressed in lakhs.
- 1 crore = 100 lakh.
- timeline_months should be numeric when a timeline is explicitly provided.
- wants_to_visit should be true only when the lead explicitly mentions
  visiting, viewing, seeing, or scheduling a property visit.

Lead inquiry:
{inquiry}
"""

    schema = LeadProfile.model_json_schema()

    response = generate_response(
        prompt,
        output_schema=schema,
    )

    data = json.loads(response)

    return LeadProfile(**data)