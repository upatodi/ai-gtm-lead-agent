"""
Tests the LLM-based lead extraction.
"""

from app.llm.extractor import extract_lead_profile


inquiry = "I want a 2BHK in College Road."


profile = extract_lead_profile(inquiry)

print("=== EXTRACTED LEAD PROFILE ===")
print(profile)