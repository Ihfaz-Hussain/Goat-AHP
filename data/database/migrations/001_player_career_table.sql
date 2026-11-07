
-- GOAT-AHP: Extend database for player career ingestion

-- Add Wikidata identifiers to existing tables
ALTER TABLE public.players
ADD COLUMN IF NOT EXISTS wikidata_id VARCHAR(30) UNIQUE;

ALTER TABLE public.clubs
ADD COLUMN IF NOT EXISTS wikidata_id VARCHAR(30) UNIQUE;


-- Store each player's club membership periods
CREATE TABLE IF NOT EXISTS public.player_club_history (
    history_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    player_id BIGINT NOT NULL,
    club_id BIGINT NOT NULL,

    start_year INTEGER,
    end_year INTEGER,

    source_url TEXT,

    CONSTRAINT fk_history_player
        FOREIGN KEY (player_id)
        REFERENCES public.players(player_id),

    CONSTRAINT fk_history_club
        FOREIGN KEY (club_id)
        REFERENCES public.clubs(club_id),

    CONSTRAINT chk_career_years
        CHECK (
            end_year IS NULL
            OR start_year IS NULL
            OR end_year >= start_year
        )
);


-- Store senior international and World Cup summaries
CREATE TABLE IF NOT EXISTS public.player_international_stats (
    international_stat_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    player_id BIGINT NOT NULL
        REFERENCES public.players(player_id),

    stat_scope VARCHAR(30) NOT NULL
        CHECK (stat_scope IN ('senior_international', 'world_cup')),

    appearances INTEGER CHECK (appearances >= 0),
    goals INTEGER CHECK (goals >= 0),
    assists INTEGER CHECK (assists >= 0),

    as_of_date DATE NOT NULL,
    source_url TEXT NOT NULL,
    verified BOOLEAN NOT NULL DEFAULT FALSE,

    UNIQUE (player_id, stat_scope, as_of_date)
);


-- Store team trophies and individual awards
CREATE TABLE IF NOT EXISTS public.player_honours (
    honour_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    player_id BIGINT NOT NULL
        REFERENCES public.players(player_id),

    honour_type VARCHAR(20) NOT NULL
        CHECK (honour_type IN ('team', 'individual')),

    honour_name VARCHAR(150) NOT NULL,
    season VARCHAR(20),

    source_url TEXT NOT NULL
);
