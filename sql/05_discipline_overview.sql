-- Query 05: Discipline overview by grade
--
-- Business question
--   How are discipline incidents spread across grades, and are they
--   concentrated in a few students or shared across many?
--
-- What this query returns
--   One row per grade plus one row for all grades together. Each row
--   shows the student count, total incidents, incidents per student,
--   the share of students with at least one incident, and total major
--   incidents.
--
-- How to read it
--   Grade 8 holds the most students, so it also holds the highest
--   incident total. The incidents per student column is the fair
--   comparison across grades of different sizes. Most students have
--   zero or one incident, so the totals rest on a small number of
--   students with several incidents each.

CREATE OR REPLACE VIEW fact_discipline AS
    SELECT * FROM read_csv_auto('data/processed/fact_discipline.csv');

SELECT
    CAST(Grade AS VARCHAR) AS grade,
    COUNT(*) AS students,
    SUM(Incidents) AS total_incidents,
    ROUND(AVG(Incidents), 2) AS incidents_per_student,
    ROUND(100.0 * SUM(CASE WHEN Incidents > 0 THEN 1 ELSE 0 END)
        / COUNT(*), 1) AS percent_with_incidents,
    SUM(Major_Incidents) AS total_major_incidents
FROM fact_discipline
GROUP BY Grade

UNION ALL

SELECT
    'All grades' AS grade,
    COUNT(*) AS students,
    SUM(Incidents) AS total_incidents,
    ROUND(AVG(Incidents), 2) AS incidents_per_student,
    ROUND(100.0 * SUM(CASE WHEN Incidents > 0 THEN 1 ELSE 0 END)
        / COUNT(*), 1) AS percent_with_incidents,
    SUM(Major_Incidents) AS total_major_incidents
FROM fact_discipline
ORDER BY
    CASE WHEN grade = 'All grades' THEN 2 ELSE 1 END,
    grade;
