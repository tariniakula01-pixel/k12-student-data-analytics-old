-- Query 03: Assessment performance by grade and by subject
--
-- Business question
--   Where are assessment results strongest and weakest when students
--   are grouped by grade, and when results are grouped by subject?
--
-- What this query returns
--   One row per grade and one row per subject, marked in the grouping
--   column. Each row shows the student count, the average score, the
--   share of students recorded as Met, and the count of students
--   recorded as Below. The rank_in_group column ranks rows inside each
--   grouping by the share recorded as Met, highest first.
--
-- How to read it
--   Every student in this data took exactly one assessment in one
--   subject. The subject rows therefore compare different groups of
--   students, not the same students across subjects. A subject gap can
--   reflect who sat the assessment as much as the subject itself.
--   Met means a score of 70 or above in this data.

CREATE OR REPLACE VIEW fact_assessment AS
    SELECT * FROM read_csv_auto('data/processed/fact_assessment.csv');

WITH grouped AS (
    SELECT
        'Grade' AS grouping,
        CAST(Grade AS VARCHAR) AS group_name,
        COUNT(*) AS students,
        ROUND(AVG(Score), 2) AS average_score,
        ROUND(100.0 * SUM(CASE WHEN Benchmark = 'Met' THEN 1 ELSE 0 END)
            / COUNT(*), 1) AS percent_met,
        SUM(CASE WHEN Benchmark = 'Below' THEN 1 ELSE 0 END)
            AS students_below
    FROM fact_assessment
    GROUP BY Grade

    UNION ALL

    SELECT
        'Subject' AS grouping,
        Assessment AS group_name,
        COUNT(*) AS students,
        ROUND(AVG(Score), 2) AS average_score,
        ROUND(100.0 * SUM(CASE WHEN Benchmark = 'Met' THEN 1 ELSE 0 END)
            / COUNT(*), 1) AS percent_met,
        SUM(CASE WHEN Benchmark = 'Below' THEN 1 ELSE 0 END)
            AS students_below
    FROM fact_assessment
    GROUP BY Assessment
)
SELECT
    grouping,
    group_name,
    students,
    average_score,
    percent_met,
    students_below,
    RANK() OVER (
        PARTITION BY grouping ORDER BY percent_met DESC
    ) AS rank_in_group
FROM grouped
ORDER BY grouping, rank_in_group;
