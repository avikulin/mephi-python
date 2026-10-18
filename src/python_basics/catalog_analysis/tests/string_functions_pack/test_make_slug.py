from catalog_analysis.func.strings.string_utils import make_slug


def test_make_slug_title_case():
    assert make_slug("The Quiet Algorithm") == "the-quiet-algorithm"


def test_make_slug_lowercase():
    assert make_slug("the quiet algorithm") == "the-quiet-algorithm"


def test_make_slug_whitespace_padded():
    assert make_slug(" a  b ") == "a-b"


def test_make_slug_multiple_inner_spaces():
    assert make_slug("A  B  C") == "a-b-c"


def test_make_slug_single_word():
    assert make_slug("Dune") == "dune"


def test_make_slug_empty_string():
    assert make_slug("") == ""


def test_make_slug_none():
    assert make_slug(None) == ""


def test_make_slug_returns_string():
    assert isinstance(make_slug("The Quiet Algorithm"), str)
