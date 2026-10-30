from catalog_analysis.func.scalar import decade_label


def test_decade_label_new():
    assert decade_label(2021) == "новые"
    assert decade_label(2030) == "новые"


def test_decade_label_recent():
    assert decade_label(2015) == "недавние"
    assert decade_label(2020) == "недавние"


def test_decade_label_old():
    assert decade_label(2014) == "старые"
    assert decade_label(1980) == "старые"
