CREATE TABLE players(
    player_id SERIAL PRIMARY KEY,
    planyer_name varchar(100) NOT NULL,
    career_start INT,
    career_end INT,
);

CREATE TABLE club_seasons (
    player_id INT NOT NULL,
    season VARCHAR(9) NOT NULL,
    club VARCHAR(100) NOT NULL,
    appearances INT,
    goals INT,
    assists INT,

    FOREIGN KEY (player_id) REFERENCES players(player_id)
);

CREATE TABLE international (
    player_id INT NOT NULL,
    year INT NOT NULL,
    national_team VARCHAR(100) NOT NULL,
    appearances INT,
    goals INT,

    FOREIGN KEY (player_id) REFERENCES players(player_id)
);

CREATE TABLE matches (
    match_id SERIAL PRIMARY KEY,
    player_id INT NOT NULL,
    date DATE NOT NULL,
    team VARCHAR(100),
    opponent VARCHAR(100),
    result CHAR(1),

    FOREIGN KEY (player_id) REFERENCES players(player_id),

    CHECK (result IN ('W', 'D', 'L'))
);

CREATE TABLE trophies (
    player_id INT NOT NULL,
    year INT NOT NULL,
    competition VARCHAR(100) NOT NULL,
    trophy_type VARCHAR(50),

    FOREIGN KEY (player_id) REFERENCES players(player_id)
);

CREATE TABLE awards (
    player_id INT NOT NULL,
    year INT NOT NULL,
    award VARCHAR(100) NOT NULL,
    category VARCHAR(100),

    FOREIGN KEY (player_id) REFERENCES players(player_id)
);

CREATE TABLE world_cup (
    player_id INT NOT NULL,
    tournament INT NOT NULL,
    appearances INT,
    minutes INT,
    goals INT,
    assists INT,
    stage_reached VARCHAR(50),

    FOREIGN KEY (player_id) REFERENCES players(player_id)
);

