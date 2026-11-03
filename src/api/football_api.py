
import os
import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "https://v3.football.api-sports.io"


def get_team(team_id):
    """Retrieve a team using its API-Football ID."""

    api_key = os.getenv("API_FOOTBALL_KEY")

    if not api_key:
        raise ValueError("API_FOOTBALL_KEY is missing")

    response = requests.get(
        f"{BASE_URL}/teams",
        headers={"x-apisports-key": api_key},
        params={"id": team_id},
        timeout=20
    )

    response.raise_for_status()

    data = response.json()

    if data.get("errors"):
        raise RuntimeError(data["errors"])

    teams = data.get("response", [])

    if not teams:
        raise ValueError(
            f"No team found for ID {team_id}"
        )

    return teams[0]["team"]
