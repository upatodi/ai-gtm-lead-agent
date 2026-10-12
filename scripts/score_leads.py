"""
Reads lead inquiries, extracts structured information using the local LLM,
and applies deterministic lead qualification scoring.
"""

import pandas as pd

from app.llm.extractor import extract_lead_profile
from app.qualification.scorer import calculate_lead_score


LEADS_FILE = "data/leads.csv"
OUTPUT_FILE = "data/scored_leads.csv"


leads_df = pd.read_csv(LEADS_FILE)

print("=== LEAD DATASET ===")
print(leads_df)


scored_leads = []


for _, lead in leads_df.iterrows():

    inquiry = lead["inquiry"]

    # Step 1: Extract structured information using the LLM
    profile = extract_lead_profile(inquiry)

    # Step 2: Convert the extracted profile into
    # the signals expected by the deterministic scorer
    signals = {
        "timeline_months": profile.timeline_months,
        "has_budget": profile.budget_max_lakh is not None,
        "budget_max_lakh": profile.budget_max_lakh,
        "has_location": len(profile.locations) > 0,
        "has_property_requirement": (
            profile.bedrooms is not None
            or profile.property_type is not None
        ),
        "bedrooms": profile.bedrooms,
        "property_type": profile.property_type,
        "wants_to_visit": profile.wants_to_visit,
    }

    # Step 3: Apply deterministic business rules
    score = calculate_lead_score(**signals)

    scored_leads.append({
        "lead_id": lead["lead_id"],
        "name": lead["name"],
        "email": lead["email"],
        "timeline_months": profile.timeline_months,
        "budget_max_lakh": profile.budget_max_lakh,
        "bedrooms": profile.bedrooms,
        "property_type": profile.property_type,
        "locations": "; ".join(profile.locations),
        "wants_to_visit": profile.wants_to_visit,
        "lead_score": score["lead_score"],
        "priority": score["priority"],
        "reasons": "; ".join(score["reasons"]),
    })

    print("\n=== LEAD RESULT ===")
    print(f"Lead ID: {lead['lead_id']}")
    print(f"Name: {lead['name']}")
    print(f"Extracted Profile: {profile}")
    print(f"Score: {score['lead_score']}")
    print(f"Priority: {score['priority']}")
    print(f"Reasons: {score['reasons']}")


scored_df = pd.DataFrame(scored_leads)


print("\n=== SCORED LEADS ===")
print(scored_df)


scored_df.to_csv(OUTPUT_FILE, index=False)

print(f"\nScored leads saved to {OUTPUT_FILE}")