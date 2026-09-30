import csv


def mom_growth(previous: float, current: float) -> float:
    return round((current - previous) / previous * 100, 2)


def is_flagged(mom_pct: float, threshold: float = 8.0) -> str:
    if abs(mom_pct) > threshold:
        return "flagged"
    elif abs(mom_pct) < threshold:
        return "not_flagged"
    else:
        return "escalate_exact_boundary"


def validate_feed(csv_path: str) -> tuple[bool, list[str]]:
    errors = []

    with open(csv_path, "r") as file:
        reader = csv.DictReader(file)

        for line_number, row in enumerate(reader, start=2):

            if row["category"] == "":
                errors.append(
                    f"line {line_number}: missing category (month={row['month']})"
                )

            if row["revenue"] == "":
                errors.append(
                    f"line {line_number}: missing revenue (category={row['category']})"
                )

            else:
                try:
                    revenue = float(row["revenue"])

                except ValueError:
                    errors.append(
                        f"line {line_number}: revenue not numeric: {row['revenue']!r}"
                    )

                else:
                    if revenue < 0:
                        errors.append(
                            f"line {line_number}: negative revenue ({revenue}) for category={row['category']}"
                        )

    if errors:
        return False, errors
    else:
        return True, []