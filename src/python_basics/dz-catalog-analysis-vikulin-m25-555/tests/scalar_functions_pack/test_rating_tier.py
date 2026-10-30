from catalog_analysis.func.scalar import rating_tier


def test_rating_tier_masterpiece():
    assert rating_tier(9) == "шедевр"
    assert rating_tier(10) == "шедевр"
    assert rating_tier(9.5) == "шедевр"


def test_rating_tier_good():
    assert rating_tier(7) == "хорошо"
    assert rating_tier(8.5) == "хорошо"
    assert rating_tier(8.9) == "хорошо"


def test_rating_tier_average():
    assert rating_tier(5) == "средне"
    assert rating_tier(6.5) == "средне"
    assert rating_tier(6.9) == "средне"


def test_rating_tier_weak():
    assert rating_tier(4.9) == "слабо"
    assert rating_tier(0) == "слабо"
