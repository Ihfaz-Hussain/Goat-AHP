import requests
import re
#CR7 wiki data id
CR7_WIKIDATA_ID = "Q11571"

#Construct the API endpoint URL for full entity JSON payload
url = f"https://www.wikidata.org/wiki/Special:EntityData/{CR7_WIKIDATA_ID}.json"

#Execute GET request with custom User-Agent to satisfy API rate-limiting rules
response = requests.get(
    url,
    headers = {"User-Agent": "Goat-AHP/0.1"},
    timeout = 20
)

#Raise an HTTPError if the response status code indicates a failure (4xx/5xx)
response.raise_for_status()

#Convert JSON to a python dictionary and extract the player entity data using the CR7 Wikidata ID
data = response.json()
player = data["entities"][CR7_WIKIDATA_ID]

#Log core attributes
print("Player ID:", player["id"])
print("Player name:", player["labels"]["en"]["value"])
print("Available properties:", len(player["claims"]))


#Extract Cristiano Ronaldo's team memberships
teams = player["claims"]["P54"]

print("Number of team records:", len(teams))

team_ids = []

for team in teams:
    team_id = team["mainsnak"]["datavalue"]["value"]["id"]
    team_ids.append(team_id)

#Remove duplicates by converting to a dictionary and back to a list
unique_ids = list(dict.fromkeys(team_ids))

#Fetch english names for all the teaam ids
response = requests.get(
    f"https://www.wikidata.org/w/api.php",
    params = {
        "action": "wbgetentities",
        "ids": "|".join(unique_ids),
        "format": "json",
        "props": "labels",
        "languages": "en"
    },
    headers = {"User-Agent": "Goat-AHP/0.1"},
    timeout = 20
)
response.raise_for_status()

#store the team data in a dictionary for easy access
team_data = response.json()["entities"]

#Function to determine if a team is a youth team based on its name
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


#Call the function
career = get_career_history(teams, team_data)

#Inspect the returned data
print("Type:", type(career))
print("Number of records:", len(career))


for team_record in teams:
    team_id = team_record["mainsnak"]["datavalue"]["value"]["id"]
    team_name = (
        team_data[team_id]
        .get("labels", {})
        .get("en", {})
        .get("value", "Unknown")
    )

    if is_youth_team(team_name):
        continue

    start_year = get_year(team_record, "P580")
    end_year = get_year(team_record, "P582")

    print(
        f"{team_name}: {start_year} - {end_year}"
    )
