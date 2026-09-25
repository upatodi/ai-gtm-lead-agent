"""
Reads lead inquiries and applies the lead qualification scoring engine.
"""

import pandas as pd
import re

from app.qualification.scorer import calculate_lead_score

def extract_lead_signals(inquiry):
    """
    Extracts basic qualification signals from a lead inquiry.
    """

    inquiry_lower = inquiry.lower()

    timeline_months = None

    timeline_month_match = re.search(
        r"(\d+)\s*months?",
        inquiry_lower
    )

    timeline_week_match = re.search(
        r"(\d+)\s*weeks?",
        inquiry_lower
    )

    if timeline_month_match:
        timeline_months = int(timeline_month_match.group(1))

    elif timeline_week_match:
        weeks = int(timeline_week_match.group(1))
        timeline_months = round(weeks / 4, 1)

    elif "later this year" in inquiry_lower:
        timeline_months = 6

    elif "another year" in inquiry_lower:
        timeline_months = 12

    budget_max_lakh = None

    crore_match = re.search(
        r"(\d+(?:\.\d+)?)\s*(?:crore|cr)",
        inquiry_lower
    )

    lakh_match = re.search(
        r"(\d+(?:\.\d+)?)(?:\s*-\s*(\d+(?:\.\d+)?))?\s*(?:lakh|lakhs|l)",
        inquiry_lower
    )

    if crore_match:
        budget_max_lakh = float(crore_match.group(1)) * 100

    elif lakh_match:
        if lakh_match.group(2):
            budget_max_lakh = float(lakh_match.group(2))
        else:
            budget_max_lakh = float(lakh_match.group(1))

    has_budget = budget_max_lakh is not None

    has_location = any(
        location in inquiry_lower
        for location in [
            "gangapur road",
            "anandvalli",
            "college road",
            "nashik road",
            "indira nagar",
            "pathardi phata",
            "deolali",
            "satpur",
        ]
    )

    has_property_requirement = any(
        property_type in inquiry_lower
        for property_type in ["1bhk", "2bhk", "3bhk", "4bhk", "villa"]
    )

    wants_to_visit = any(
        phrase in inquiry_lower
        for phrase in ["visit", "finalize quickly", "see the property"]
    )

    return {
        "timeline_months": timeline_months,
        "budget_max_lakh": budget_max_lakh,
        "has_budget": budget_max_lakh is not None,
        "has_location": has_location,
        "has_property_requirement": has_property_requirement,
        "wants_to_visit": wants_to_visit,
    }

LEADS_FILE = "data/leads.csv"

leads_df = pd.read_csv(LEADS_FILE)

print("=== LEAD DATASET ===")
print(leads_df)

scored_leads = []

for _, lead in leads_df.iterrows():

    inquiry = lead["inquiry"]

    signals = extract_lead_signals(inquiry)

    score = calculate_lead_score(**signals)
    scored_leads.append({
    "lead_id": lead["lead_id"],
    "name": lead["name"],
    "email": lead["email"],
    "lead_score": score["lead_score"],
    "priority": score["priority"],
    "reasons": "; ".join(score["reasons"]),
})

    print("\n=== LEAD RESULT ===")
    print(f"Lead ID: {lead['lead_id']}")
    print(f"Name: {lead['name']}")
    print(f"Score: {score['lead_score']}")
    print(f"Priority: {score['priority']}")
    print(f"Reasons: {score['reasons']}")

scored_df = pd.DataFrame(scored_leads)

print("\n=== SCORED LEADS ===")
print(scored_df)

OUTPUT_FILE = "data/scored_leads.csv"

scored_df.to_csv(OUTPUT_FILE, index=False)

print(f"\nScored leads saved to {OUTPUT_FILE}")