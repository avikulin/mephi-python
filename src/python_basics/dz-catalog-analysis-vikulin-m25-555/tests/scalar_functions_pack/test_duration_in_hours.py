from catalog_analysis.func.scalar import duration_in_hours


def test_duration_in_hours_zero():
    assert duration_in_hours(0) == "0ч 0м"


def test_duration_in_hours_less_than_hour():
    assert duration_in_hours(35) == "0ч 35м"


def test_duration_in_hours_exact_hour():
    assert duration_in_hours(60) == "1ч 0м"


def test_duration_in_hours_mixed():
    assert duration_in_hours(155) == "2ч 35м"


def test_duration_in_hours_multiple_hours():
    assert duration_in_hours(240) == "4ч 0м"


def test_duration_in_hours_returns_string():
    assert isinstance(duration_in_hours(90), str)
