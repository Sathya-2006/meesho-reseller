def alias_for(reseller_id: str) -> str:
    return f"ALIAS-{reseller_id[3:]}"


def assert_no_raw_names_leak(
    text: str,
    reseller_names: list[str]
) -> bool:
    """
    Return False if any raw reseller name appears verbatim in the text.
    Otherwise return True.
    """
    for name in reseller_names:
        if name in text:
            return False

    return True


# Raw reseller names from Part 1's top-reseller HAVING query
raw_names = [
    "Mumbai Reseller 1",
    "Mumbai Reseller 4",
    "Hyderabad Reseller 6",
    "Lucknow Reseller 6",
    "Jaipur Reseller 5"
]


# Top-reseller narrative for external use.
# Resellers are referenced only by region + alias.
top_reseller_narrative = """
Top-reseller performance summary:

- West region — ALIAS-19 generated revenue of 75295.09.
- West region — ALIAS-22 generated revenue of 73882.33.
- South region — ALIAS-12 generated revenue of 69936.46.
- North region — ALIAS-06 generated revenue of 64238.97.
- North region — ALIAS-05 generated revenue of 61825.02.

These aliases are used instead of raw reseller names in the
external-facing narrative.
"""


# Required alias tests
assert alias_for("RS019") == "ALIAS-19"
assert alias_for("RS006") == "ALIAS-06"


# Required positive test:
# The narrative contains aliases but no raw reseller names.
assert assert_no_raw_names_leak(
    top_reseller_narrative,
    raw_names
) is True


# Required negative test:
# A raw reseller name is intentionally included.
leaking_narrative = """
Mumbai Reseller 1 generated the highest revenue.
"""

assert assert_no_raw_names_leak(
    leaking_narrative,
    raw_names
) is False


print("alias_for tests: PASS")
print("top-reseller masking positive test: PASS")
print("top-reseller masking negative test: PASS")