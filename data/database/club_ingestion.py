from src.api.football_api import get_team
from data.database.connection import get_connection


def save_club(team):
    """Insert or update a club in PostgreSQL."""

    query = """
        INSERT INTO public.clubs
            (api_football_id, club_name, country)
        VALUES (%s, %s, %s)

        ON CONFLICT (api_football_id)
        DO UPDATE SET
            club_name = EXCLUDED.club_name,
            country = EXCLUDED.country

        RETURNING club_id;
    """

    connection = get_connection()

    try:
        with connection.cursor() as cursor:

            cursor.execute(
                query,
                (
                    team["id"],
                    team["name"],
                    team["country"]
                )
            )

            club_id = cursor.fetchone()[0]

        connection.commit()
        return club_id

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()


def main():
    # Extract data from the API
    team = get_team(541)

    # Load data into PostgreSQL
    club_id = save_club(team)

    print(
        f"Saved {team['name']} "
        f"with database ID {club_id}"
    )


if __name__ == "__main__":
    main()
