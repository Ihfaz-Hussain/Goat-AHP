--store the players being compared 
CREATE TABLE players (
    player_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    player_name VARCHAR(100) NOT NULL UNIQUE,
);

CREATE TABLE competition_strength(
    competition VARCHAR(100) PRIMARY KEY,
    strength_score INT NOT NULL
)