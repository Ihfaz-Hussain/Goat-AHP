-- Upsert club record to ensure pipeline idempotency.
-- Inserts a new record, or updates existing data if the api_football_id already exists.
INSERT INTO clubs (api_football_id, club_name, country)
VALUES (541, 'Real Madrid', 'Spain')
-- Catch duplicate key violations on the unique constraint index
ON CONFLICT (api_football_id)
-- If a conflict occurs, overwrite stale attributes with the incoming payload values
DO UPDATE SET
    club_name = EXCLUDED.club_name,
    country = EXCLUDED.country;