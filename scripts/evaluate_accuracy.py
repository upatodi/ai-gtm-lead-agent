"""
Compares LLM extraction results against ground truth.
"""

import pandas as pd


RESULTS_FILE = "data/llm_extraction_results.csv"
GROUND_TRUTH_FILE = "data/lead_ground_truth.csv"


results_df = pd.read_csv(RESULTS_FILE)
truth_df = pd.read_csv(GROUND_TRUTH_FILE)


merged_df = results_df.merge(
    truth_df,
    on="lead_id",
    suffixes=("_predicted", "_actual"),
)


def normalize_locations(value):
    """
    Converts a semicolon-separated location string
    into a normalized set.
    """

    if pd.isna(value) or value == "":
        return set()

    return {
        location.strip().lower()
        for location in str(value).split(";")
    }


def values_match(predicted, actual):
    """
    Compares two values while treating missing values consistently.
    """

    if pd.isna(predicted) and pd.isna(actual):
        return True

    if pd.isna(predicted) or pd.isna(actual):
        return False

    return predicted == actual


fields = [
    "bedrooms",
    "property_type",
    "budget_max_lakh",
    "timeline_months",
    "wants_to_visit",
]


print("=== FIELD-LEVEL ACCURACY ===")

total_correct = 0
total_fields = 0


for field in fields:

    correct = 0

    for _, row in merged_df.iterrows():

        predicted = row[f"{field}_predicted"]
        actual = row[f"{field}_actual"]

        if values_match(predicted, actual):
            correct += 1

    total = len(merged_df)
    accuracy = (correct / total) * 100

    total_correct += correct
    total_fields += total

    print(
        f"{field}: "
        f"{correct}/{total} "
        f"({accuracy:.1f}%)"
    )


# ---------------------------------------------------------
# Location accuracy
# ---------------------------------------------------------

location_correct = 0

for _, row in merged_df.iterrows():

    predicted = normalize_locations(
        row["locations_predicted"]
    )

    actual = normalize_locations(
        row["locations_actual"]
    )

    if predicted == actual:
        location_correct += 1


location_total = len(merged_df)
location_accuracy = (
    location_correct / location_total
) * 100


print(
    f"locations: "
    f"{location_correct}/{location_total} "
    f"({location_accuracy:.1f}%)"
)


total_correct += location_correct
total_fields += location_total


overall_accuracy = (
    total_correct / total_fields
) * 100


print("\n=== OVERALL ACCURACY ===")
print(
    f"{total_correct}/{total_fields} "
    f"({overall_accuracy:.1f}%)"
)