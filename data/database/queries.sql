-- Run in any SQLite client, or from Python: pd.read_sql(query, con)

-- 1. Sanity check: every respondent has exactly 28 comparisons
SELECT respondent_id, COUNT(*) AS n_comparisons
FROM pairwise_responses
GROUP BY respondent_id
HAVING COUNT(*) <> 28;                       -- should return 0 rows

-- 2. Who do respondents pick as GOAT?
SELECT goat_choice, COUNT(*) AS n,
       ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM respondents), 1) AS pct
FROM respondents
GROUP BY goat_choice
ORDER BY n DESC;

-- 3. Sample composition by age group and country
SELECT age_group, country, COUNT(*) AS n
FROM respondents
GROUP BY age_group, country
ORDER BY n DESC;

-- 4. Average signed answer per comparison (JOIN not needed, GROUP BY is enough)
--    >0 means the second criterion tends to win, <0 the first
SELECT criterion_a, criterion_b,
       ROUND(AVG(signed_value), 2) AS mean_signed,
       ROUND(AVG(raw_value), 2)    AS mean_raw
FROM pairwise_responses
GROUP BY criterion_a, criterion_b
ORDER BY ABS(AVG(signed_value)) DESC;

-- 5. JOIN example: do Messi supporters answer differently from Ronaldo supporters?
SELECT r.player_supporter, p.criterion_a, p.criterion_b,
       ROUND(AVG(p.signed_value), 2) AS mean_signed, COUNT(*) AS n
FROM pairwise_responses p
JOIN respondents r ON r.respondent_id = p.respondent_id
WHERE r.player_supporter IN ('Lionel Messi', 'Cristiano Ronaldo')
GROUP BY r.player_supporter, p.criterion_a, p.criterion_b
ORDER BY p.criterion_a, p.criterion_b, r.player_supporter;

-- 6. "Always 4" answerers (possible straight-lining)
SELECT respondent_id,
       SUM(CASE WHEN raw_value = 4 THEN 1 ELSE 0 END) AS n_equal_answers
FROM pairwise_responses
GROUP BY respondent_id
ORDER BY n_equal_answers DESC
LIMIT 5;

-- 7. Exclude minors (if your ethics approval requires it) as a reusable view
CREATE VIEW IF NOT EXISTS adult_respondents AS
SELECT * FROM respondents WHERE is_minor = 0;
