"""
Evaluates LLM-based lead extraction across the lead dataset.
"""

import pandas as pd

from app.llm.extractor import extract_lead_profile


LEADS_FILE = "data/leads.csv"


leads_df = pd.read_csv(LEADS_FILE)


results = []


for _, lead in leads_df.iterrows():

    print("\n" + "=" * 60)
    print(f"Lead: {lead['lead_id']} - {lead['name']}")
    print(f"Inquiry: {lead['inquiry']}")

    try:
        profile = extract_lead_profile(lead["inquiry"])

        print("\nExtracted Profile:")
        print(profile)

        results.append({
            "lead_id": lead["lead_id"],
            "bedrooms": profile.bedrooms,
            "property_type": profile.property_type,
            "locations": "; ".join(profile.locations),
            "budget_max_lakh": profile.budget_max_lakh,
            "timeline_months": profile.timeline_months,
            "wants_to_visit": profile.wants_to_visit,
            "status": "success",
        })

    except Exception as error:

        print("\nExtraction failed:")
        print(error)

        results.append({
            "lead_id": lead["lead_id"],
            "bedrooms": None,
            "property_type": None,
            "locations": "",
            "budget_max_lakh": None,
            "timeline_months": None,
            "wants_to_visit": None,
            "status": "failed",
        })


results_df = pd.DataFrame(results)


OUTPUT_FILE = "data/llm_extraction_results.csv"

results_df.to_csv(
    OUTPUT_FILE,
    index=False,
)


print("\n" + "=" * 60)
print("LLM EXTRACTION EVALUATION COMPLETE")
print("=" * 60)

print(results_df)

print(f"\nResults saved to {OUTPUT_FILE}")