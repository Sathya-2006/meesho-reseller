from growth_engine import is_flagged, mom_growth, validate_feed


def test_mom_growth():
    result = mom_growth(104520.77, 185107.61)

    assert result == 77.1


def test_is_flagged():
    mom = mom_growth(104520.77, 185107.61)

    result = is_flagged(mom)

    assert result == "flagged"


def test_exact_boundary():
    mom = mom_growth(100000, 108000)

    result = is_flagged(mom)

    assert mom == 8.0
    assert result == "escalate_exact_boundary"


test_mom_growth()
print("test_mom_growth: PASS")

test_is_flagged()
print("test_is_flagged: PASS")

test_exact_boundary()
print("test_exact_boundary: PASS")


def test_corrupted_feed():
    result, errors = validate_feed(
        "part2_engine/fixtures/corrupted_feed.csv"
    )

    expected_errors = [
        "line 3: negative revenue (-4200.0) for category=Western Wear",
        "line 4: missing category (month=July)",
        "line 6: missing revenue (category=Home & Kitchen)"
    ]

    assert result == False
    assert errors == expected_errors


test_corrupted_feed()
print("test_corrupted_feed: PASS")


def test_valid_feed():
    result, errors = validate_feed(
        "part2_engine/fixtures/monthly_category_revenue.csv"
    )

    assert result == True
    assert errors == []


test_valid_feed()
print("test_valid_feed: PASS")