from catalog_analysis.func.strings.string_utils import normalize_title


def test_normalize_title_lowercase():
    assert normalize_title("the quiet algorithm") == "The Quiet Algorithm"


def test_normalize_title_mixed_case():
    assert normalize_title("tHe DUNE Chronicles") == "The Dune Chronicles"


def test_normalize_title_whitespace_padded():
    assert normalize_title("  two  left   shoes  ") == "Two Left Shoes"


def test_normalize_title_single_word():
    assert normalize_title("dune") == "Dune"


def test_normalize_title_empty_string():
    assert normalize_title("") == ""


def test_normalize_title_none():
    assert normalize_title(None) == ""


def test_normalize_title_returns_string():
    assert isinstance(normalize_title("the quiet algorithm"), str)
