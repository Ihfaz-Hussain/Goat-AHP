from src.api.wikidata_api import classify_team, is_youth_team

def test_youth_team_detection():
    assert is_youth_team("Portugal U21") is True
    assert is_youth_team("England under-17") is True
    assert is_youth_team("Barcelona U19") is True

def test_team_classification():
    assert classify_team("Portugal U21") == "youth"
    assert classify_team("England under-17") == "youth"
    assert classify_team("Barcelona U19") == "youth"
    assert classify_team("Real Madrid") == "senior_club"
    assert classify_team("Manchester United") == "senior_club"
    assert classify_team("Juventus") == "senior_club"


def test_senior_team_detection():
    assert is_youth_team("Real Madrid") is False
    assert is_youth_team("Manchester United") is False
    assert is_youth_team("Juventus") is False
