import pytest
from app import _parse_json_from_text, _detect_language


def test_parse_json_direct():
    s = '{"a": 1, "b": [1,2]}'
    obj = _parse_json_from_text(s)
    assert obj['a'] == 1


def test_parse_json_in_text():
    s = 'Some text before {"x": 10, "y": "ok"} some text after'
    obj = _parse_json_from_text(s)
    assert obj['x'] == 10


def test_parse_json_raises_on_no_json():
    with pytest.raises(ValueError):
        _parse_json_from_text('no json here')


def test_detect_language_hebrew():
    heb = 'שלום, זה טקסט בעברית'
    assert _detect_language(heb) == 'he'


def test_detect_language_english():
    eng = 'Hello, this is english'
    assert _detect_language(eng) == 'en'


def test_detect_language_empty():
    assert _detect_language('') == 'en'
