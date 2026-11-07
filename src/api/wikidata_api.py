from os import name

import requests
import re


#function to retrieve player from wikidata
def get_player(player_id):
    """Retrieve a player using its Wikidata ID."""
    url = f"https://www.wikidata.org/wiki/Special:EntityData/{player_id}.json"
    response = requests.get(
        url,
        headers={"User-Agent": "Goat-AHP/0.1"},
        timeout=20
    )
    response.raise_for_status()
    data = response.json()
    player = data["entities"][player_id]
    return player

#removes any age-group teams from the career history using regex pattern
def is_youth_team(team_name):
    pattern = r"\b(?:under[- ]?\d{2}|u[- ]?\d{2})\b"

    return bool(
        re.search(pattern, team_name, re.IGNORECASE)
    )

#Function to extract the start and end years of a team membership from the qualifiers
def get_year(team_record, property_id):
    qualifiers = team_record.get("qualifiers", {})

    dates = qualifiers.get(property_id, [])

    if not dates:
        return None

    date_value = dates[0]["datavalue"]["value"]["time"]

    return int(date_value[1:5])

#classifier function for checking teams taken into goat calculation
def classify_team(team_name):
    name = team_name.lower()

    if is_youth_team(name):
        return "youth"
    if "olympic" in name:
        return "olympic"
    
    if "barcelona atlètic" in name or "barcelona c" in name:
        return "reserve"

    if "national" in name:
        return "senior_national"

    return "senior_club"

    
#define function to get career history of a player based on team membership records and team data    
def get_career_history(teams, team_data):
    career = []
    for team_record in teams:
        team_id = team_record["mainsnak"]["datavalue"]["value"]["id"]

        team_name = (
            team_data[team_id]
            .get("labels", {})
            .get("en", {})
            .get("value", "Unknown")
        )

        #Skip age-group teams
        if is_youth_team(team_name):
            continue

        start_year = get_year(team_record, "P580")
        end_year = get_year(team_record, "P582")

        #Create a structured membership record
        record = {
            "team_id": team_id,
            "team_name": team_name,
            "start_year": start_year,
            "end_year": end_year
        }

        #Add the record to the career list
        career.append(record)

    return career

#get team data
def get_team_data(teams):
    team_ids = [team["mainsnak"]["datavalue"]["value"]["id"] for team in teams]
    unique_ids = list(dict.fromkeys(team_ids))

    if not unique_ids:
        return {}
    # Fetch team names from Wikidata
    response = requests.get(
        "https://www.wikidata.org/w/api.php",
        params={
            "action": "wbgetentities",
            "ids": "|".join(unique_ids),
            "format": "json",
            "props": "labels",
            "languages": "en"
        },
        headers={"User-Agent": "Goat-AHP/0.1"},
        timeout=20
    )

    response.raise_for_status()

    return response.json()["entities"]


def main():
    player_ids = ["Q11571", "Q615"]

    for player_id in player_ids:

        # Step 1: Retrieve the player
        player = get_player(player_id)

        # Step 2: Extract team membership records
        teams = player["claims"].get("P54", [])

        # Step 3: Retrieve team information
        team_data = get_team_data(teams)

        # Step 4: Build the career history
        career = get_career_history(teams, team_data)

        # Step 5: Display results
        player_name = player["labels"]["en"]["value"]

        print(f"\n=== {player_name} ===")

        for record in career:
            print(
                f"{record['team_name']}: "
                f"{record['start_year']} - {record['end_year']}"
            )


if __name__ == "__main__":
    main()
