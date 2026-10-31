
-- GOAT-AHP PostgreSQL Database Schema

-- 1. Players
CREATE TABLE IF NOT EXISTS public.players (
    player_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    player_name VARCHAR(150) NOT NULL,
    nationality VARCHAR(100),
    career_start INTEGER,
    career_end INTEGER
);

-- 2. Clubs
CREATE TABLE IF NOT EXISTS public.clubs (
    club_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    api_football_id INTEGER UNIQUE,
    club_name VARCHAR(150) NOT NULL,
    country VARCHAR(100)
);

-- 3. Competitions
CREATE TABLE IF NOT EXISTS public.competitions (
    competition_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    api_football_id INTEGER UNIQUE,
    competition_name VARCHAR(150) NOT NULL,
    country VARCHAR(100),
    competition_type VARCHAR(50)
);

-- 4. Matches
CREATE TABLE IF NOT EXISTS public.matches (
    match_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    api_football_id INTEGER UNIQUE,
    competition_id BIGINT NOT NULL,
    season VARCHAR(20) NOT NULL,
    match_date TIMESTAMPTZ NOT NULL,
    home_club_id BIGINT NOT NULL,
    away_club_id BIGINT NOT NULL,
    home_goals INTEGER,
    away_goals INTEGER,

    FOREIGN KEY (competition_id)
        REFERENCES public.competitions(competition_id),

    FOREIGN KEY (home_club_id)
        REFERENCES public.clubs(club_id),

    FOREIGN KEY (away_club_id)
        REFERENCES public.clubs(club_id)
);

-- 5. Historical Club Elo Ratings
CREATE TABLE IF NOT EXISTS public.club_elo_history (
    elo_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    club_id BIGINT NOT NULL,
    match_id BIGINT,
    rating_date TIMESTAMPTZ NOT NULL,
    elo_rating DOUBLE PRECISION NOT NULL,
    model_version VARCHAR(30) NOT NULL,

    FOREIGN KEY (club_id)
        REFERENCES public.clubs(club_id),

    FOREIGN KEY (match_id)
        REFERENCES public.matches(match_id),

    UNIQUE (club_id, match_id, model_version)
);
