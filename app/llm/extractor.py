"""
Extracts structured lead information using the local Ollama LLM.
"""

import json

from app.llm.ollama_client import generate_response
from app.llm.schemas import LeadProfile


def extract_lead_profile(inquiry):
    """
    Extract structured information from a real estate lead inquiry.
    """

    prompt = f"""
You are an information extraction system for a real estate lead qualification
application.

Your task is to extract ONLY information that is explicitly stated or clearly
expressed in the lead inquiry.

Return the information according to the provided JSON schema.

FIELD DEFINITIONS:

1. bedrooms
- This is the numeric number of bedrooms requested.
- BHK refers to the number of bedrooms.
- For example:
  - "1BHK" means 1 bedroom.
  - "2BHK" means 2 bedrooms.
  - "3 BHK" means 3 bedrooms.
- Extract only the numeric bedroom count.
- Do NOT put "2BHK" or "3BHK" into property_type.

2. property_type
- This means the actual type of property.
- Examples include apartment, villa, house, plot, or similar property types.
- Only populate this field when the lead explicitly specifies a property type.
- A BHK number is NOT a property type.
- If no property type is explicitly mentioned, return null.

3. locations
- Extract all locations explicitly mentioned by the lead.
- If multiple locations are mentioned, include all of them.
- Do not invent locations.
- Return an empty list if no location is mentioned.

4. budget_max_lakh
- Extract the maximum budget specified by the lead.
- Convert all amounts into lakhs.
- 1 crore = 100 lakh.
- For example:
  - 70 lakh = 70
  - 1 crore = 100
  - 1.3 crore = 130
- If no budget is mentioned, return null.

5. timeline_months
- Extract the intended purchase timeline in months.
- Pay close attention to the unit used in the inquiry.
- If the inquiry specifies weeks, convert weeks to months.
- 1 week = 0.25 months.
- Therefore:
  - 4 weeks = 1 month
  - 6 weeks = 1.5 months
  - 8 weeks = 2 months
  - 12 weeks = 3 months
- For a range, use the midpoint.
- For example:
  - "within 1 month" = 1
  - "in 6 weeks" = 1.5
  - "within 3-4 months" = 3.5
  - "later this year" = 6
  - "another year" = 12
- Do not confuse a number followed by "weeks" with the same number of months.
- If no timeline is mentioned, return null.

6. wants_to_visit
- This field represents explicit property-visit intent.
- Return true ONLY when the lead explicitly requests or proposes a physical
  property visit, viewing, inspection, or seeing the property.
- Examples that mean true:
  - "I want to visit the property."
  - "Can I see the property this weekend?"
  - "I'd like to schedule a visit."
  - "Can we arrange a viewing?"
- Return false when the lead only:
  - wants to buy soon
  - wants to finalize quickly
  - is actively looking
  - is researching
  - is interested in a property
  - has a short purchase timeline
- Purchase urgency is NOT visit intent.
- Do not infer a visit request from any other field.
- If the inquiry does not explicitly request a visit or viewing, return false.

IMPORTANT RULES:
- Do not invent information.
- Do not infer information that is not stated.
- Use null for missing scalar values.
- Use an empty list for missing locations.
- Return false for wants_to_visit unless an explicit visit request exists.
- Follow the field definitions above exactly.

LEAD INQUIRY:
{inquiry}
"""

    schema = LeadProfile.model_json_schema()

    response = generate_response(
        prompt,
        output_schema=schema,
    )

    data = json.loads(response)

    return LeadProfile(**data)