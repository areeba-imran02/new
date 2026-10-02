import pytest
from truvia.evidence import extract_input
def test_extracts_url_host():
    out=extract_input("URL","Visit https://example.com/login")
    assert out["urls"][0]["host"]=="example.com"
def test_rejects_empty():
    with pytest.raises(ValueError): extract_input("URL"," ")
def test_rejects_oversized():
    with pytest.raises(ValueError): extract_input("message","x"*12001)
