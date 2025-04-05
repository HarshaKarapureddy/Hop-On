import pytest
from Search import SearchGS, SearchGEN, AcessToken

def test_GS1_valid_game_name():
    """GS-1: Valid game name returns details"""
    result = SearchGS("The Witcher 3")
    assert result is not None
    assert "name" in result[0]
    assert "genres" in result[0]
    assert "release_dates" in result[0]
    assert "cover" in result[0]

def test_GS2_nonexistent_game():
    assert SearchGS("NonExistentGame123") is None

def test_GS3_empty_input():
    assert SearchGS("") is None

def test_GS4_special_characters():
    result = SearchGS("Final Fantasy VII")
    assert result is None or isinstance(result, list)

def test_GS5_partial_match():
    result = SearchGS("Witcher")
    assert result is not None

def test_GS6_api_failure(monkeypatch):
    def mock_failed_token(*args, **kwargs):
        return None
    monkeypatch.setattr("Search.AcessToken", mock_failed_token)
    assert SearchGS("Any Game") is None

# -------------------------

def test_GEN1_single_valid_genre():
    result = SearchGEN(["Adventure"], 5)
    assert result is not None
    assert len(result) <= 5

def test_GEN2_multiple_valid_genres():
    result = SearchGEN(["Adventure", "Indie"], 3)
    assert result is not None
    assert len(result) <= 3

def test_GEN3_invalid_genre():
    assert SearchGEN(["UnknownGenre"], 5) is None

def test_GEN4_empty_genre_input():
    assert SearchGEN([""], 5) is None

def test_GEN5_invalid_limit_zero():
    assert SearchGEN(["Action"], 0) is None

def test_GEN6_invalid_limit_eleven():
    assert SearchGEN(["RPG"], 11) is None

def test_GEN7_case_insensitive():
    result_lower = SearchGEN(["rpg"], 5)
    result_upper = SearchGEN(["RPG"], 5)
    assert (result_lower is None and result_upper is None) or \
           (result_lower is not None and result_upper is not None)

def test_GEN8_api_failure(monkeypatch):
    def mock_failed_token(*args, **kwargs):
        return None
    monkeypatch.setattr("Search.AcessToken", mock_failed_token)
    assert SearchGEN(["Action"], 5) is None

if __name__ == "__main__":
    pytest.main(["-v", "--tb=short"])
