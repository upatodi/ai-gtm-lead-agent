# Implements deterministic business rules to calculate lead scores, priorities, and scoring reasons

def calculate_lead_score(
    timeline_months=None,
    has_budget=False,
    has_location=False,
    has_property_requirement=False,
    wants_to_visit=False,
):
    score = 0
    reasons = []

    # Purchase timeline
    if timeline_months is not None:
        if timeline_months <= 1:
            score += 35
            reasons.append("Purchase expected within 1 month")
        elif timeline_months <= 3:
            score += 30
            reasons.append("Purchase expected within 3 months")
        elif timeline_months <= 6:
            score += 20
            reasons.append("Purchase expected within 6 months")
        elif timeline_months <= 12:
            score += 5
            reasons.append("Purchase expected within 7-12 months")
        else:
            reasons.append("Purchase expected after 12 months")

    # Budget
    if has_budget:
        score += 20
        reasons.append("Budget provided")

    # Location
    if has_location:
        score += 15
        reasons.append("Specific location provided")

    # Property requirement
    if has_property_requirement:
        score += 15
        reasons.append("Specific property requirement provided")

    # High purchase intent
    if wants_to_visit:
        score += 15
        reasons.append("Lead wants to visit or finalize quickly")

    # Cap score at 100
    score = min(score, 100)

    # Determine priority
    if score >= 80:
        priority = "HIGH"
    elif score >= 50:
        priority = "MEDIUM"
    else:
        priority = "LOW"

    return {
        "lead_score": score,
        "priority": priority,
        "reasons": reasons,
    }