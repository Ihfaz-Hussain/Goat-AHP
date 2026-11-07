
from src.api.wikidata_api import get_player
from data.database.connection import get_connection


def save_player(player_id):
    """Fetch a player from Wikidata and save them to PostgreSQL."""

    player = get_player(player_id)

    player_name = player["labels"]["en"]["value"]

    query = """
        INSERT INTO public.players (player_name, wikidata_id)
        VALUES (%s, %s)
        ON CONFLICT (wikidata_id)
        DO UPDATE SET player_name = EXCLUDED.player_name
        RETURNING player_id;
    """

    conn = get_connection()

    try:
        with conn:
            with conn.cursor() as cursor:
                cursor.execute(query, (player_name, player_id))
                database_id = cursor.fetchone()[0]

        print(f"Saved {player_name} with database ID {database_id}")

        return database_id

    finally:
        conn.close()


def main():
    for player_id in ["Q11571", "Q615"]:
        save_player(player_id)


if __name__ == "__main__":
    main()
