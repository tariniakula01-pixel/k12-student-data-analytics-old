-- Query 07: Assessment results by month
--
-- Business question
--   How did assessment results move across the January to April 2026
--   testing window, and how many assessments had been recorded by
--   each month?
--
-- What this query returns
--   One row per assessment month with the count of assessments, a
--   running total of assessments up to and including that month, the
--   average score, and the share of students recorded as Met.
--
-- How to read it
--   Read the movement with care. The mix of subjects differs by month,
--   and each student appears once, in one subject, in one month. A
--   change between months can reflect which students were assessed
--   rather than any change in learning. This table describes the
--   testing window. It does not track growth for the same students.

CREATE OR REPLACE VIEW fact_assessment AS
    SELECT * FROM read_csv_auto('data/processed/fact_assessment.csv');

WITH monthly AS (
    SELECT
        strftime(Assessment_Date, '%Y-%m') AS assessment_month,
        COUNT(*) AS assessments,
        ROUND(AVG(Score), 2) AS average_score,
        ROUND(100.0 * SUM(CASE WHEN Benchmark = 'Met' THEN 1 ELSE 0 END)
            / COUNT(*), 1) AS percent_met
    FROM fact_assessment
    GROUP BY assessment_month
)
SELECT
    assessment_month,
    assessments,
    SUM(assessments) OVER (ORDER BY assessment_month) AS running_total,
    average_score,
    percent_met
FROM monthly
ORDER BY assessment_month;
