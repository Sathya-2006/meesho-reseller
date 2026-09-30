import csv
import json
import os
import sys


# ---------------------------------------------------------
# Project path setup
# ---------------------------------------------------------

PROJECT_ROOT = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

sys.path.insert(0, PROJECT_ROOT)


# ---------------------------------------------------------
# Import Part 2 functions UNMODIFIED
# ---------------------------------------------------------

from part2_engine.growth_engine import (
    validate_feed,
    mom_growth,
    is_flagged
)


# ---------------------------------------------------------
# Load monthly revenue by category
# ---------------------------------------------------------

def load_revenue_by_category(csv_path: str) -> dict:
    revenue_by_category = {}

    with open(csv_path, "r") as file:
        reader = csv.DictReader(file)

        for row in reader:
            category = row["category"]
            revenue = float(row["revenue"])

            revenue_by_category[category] = revenue

    return revenue_by_category


# ---------------------------------------------------------
# Get month from CSV
# ---------------------------------------------------------

def get_month_from_csv(csv_path: str) -> str:
    with open(csv_path, "r") as file:
        reader = csv.DictReader(file)

        first_row = next(reader)

        return first_row["month"]


# ---------------------------------------------------------
# Part 3 template-fill logic
# ---------------------------------------------------------

def draft_message(
    category: str,
    previous_revenue: float,
    current_revenue: float,
    mom_pct: float,
    month: str,
    prev_month: str
) -> str:

    return (
        f"Context: {category} revenue is being compared "
        f"between {prev_month} and {month}. "
        f"Insight: FACT — {category} revenue changed by "
        f"{mom_pct}% month-over-month. "
        f"Implication: The stakeholder should review "
        f"{category} performance and investigate the "
        f"drivers of this movement. "
        f"HYPOTHESIS: Changes in reseller activity or "
        f"product demand may have contributed, but the "
        f"supplied data does not prove a specific cause."
    )


# ---------------------------------------------------------
# Main agent runner
# ---------------------------------------------------------

def run(
    month: str,
    previous_month_csv: str,
    current_month_csv: str
) -> dict:

    # -----------------------------------------------------
    # 1. Validate current monthly feed
    # -----------------------------------------------------

    valid, validation_errors = validate_feed(
        current_month_csv
    )

    # -----------------------------------------------------
    # 2. HARD STOP if validation fails
    # -----------------------------------------------------

    if not valid:

        return {
            "run_month": month,
            "validation_status": "invalid",
            "validation_errors": validation_errors,
            "flagged_categories": [],
            "suppressed_categories": [],
            "escalated_categories": [],
            "action_taken": "hard_stop"
        }

    # -----------------------------------------------------
    # 3. Load previous and current revenue
    # -----------------------------------------------------

    previous_revenue = load_revenue_by_category(
        previous_month_csv
    )

    current_revenue = load_revenue_by_category(
        current_month_csv
    )

    prev_month = get_month_from_csv(
        previous_month_csv
    )

    # -----------------------------------------------------
    # 4. Calculate MoM and apply flag rule
    # -----------------------------------------------------

    flagged = []
    escalated = []

    for category, current_value in current_revenue.items():

        previous_value = previous_revenue[category]

        mom_pct = mom_growth(
            previous_value,
            current_value
        )

        flag_status = is_flagged(
            mom_pct
        )

        if flag_status == "flagged":

            flagged.append({
                "category": category,
                "mom_pct": mom_pct,
                "previous_revenue": previous_value,
                "current_revenue": current_value
            })

        elif flag_status == "escalate_exact_boundary":

            escalated.append(category)

    # -----------------------------------------------------
    # 5. Sort flagged categories by absolute MoM
    # -----------------------------------------------------

    flagged.sort(
        key=lambda item: abs(item["mom_pct"]),
        reverse=True
    )

    # -----------------------------------------------------
    # 6. Draft top 3
    # -----------------------------------------------------

    final_flagged = []
    suppressed = []

    for index, item in enumerate(flagged):

        if index < 3:

            message = draft_message(
                category=item["category"],
                previous_revenue=item["previous_revenue"],
                current_revenue=item["current_revenue"],
                mom_pct=item["mom_pct"],
                month=month,
                prev_month=prev_month
            )

            item["drafted"] = True
            item["message"] = message

            final_flagged.append(item)

        else:

            suppressed.append(
                item["category"]
            )

    # -----------------------------------------------------
    # 7. Return structured JSON result
    # -----------------------------------------------------

    return {
        "run_month": month,
        "validation_status": "valid",
        "validation_errors": [],
        "flagged_categories": final_flagged,
        "suppressed_categories": suppressed,
        "escalated_categories": escalated,
        "action_taken": "drafted_and_held_for_approval"
    }



if __name__ == "__main__":
    may_csv = os.path.join(
        PROJECT_ROOT,
        "part4_agent",
        "may_revenue.csv"
    )

    june_csv = os.path.join(
        PROJECT_ROOT,
        "part4_agent",
        "june_revenue.csv"
    )

    result = run(
        month="June",
        previous_month_csv=may_csv,
        current_month_csv=june_csv
    )

    print(
        json.dumps(
            result,
            indent=2
        )
    )