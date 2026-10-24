-- Query 06: Data validation checks
--
-- Business question
--   Can the numbers in this project be trusted? Which problems existed
--   in the source files, and do any of them remain in the processed
--   tables?
--
-- What this query returns
--   One row per check with the count of problem rows. The first three
--   checks run on the source files and count rows whose Student_ID has
--   no matching Active student in the analysis population. The
--   remaining checks run on the processed tables, where every count
--   should read zero.
--
-- How to read it
--   A nonzero count on a processed table means the cleaning pipeline
--   needs attention before any result is shared. The same checks are
--   also written by scripts/02_clean_and_validate.py into
--   outputs/validation_results.csv.

CREATE OR REPLACE VIEW src_students AS
    SELECT * FROM read_csv_auto('data/source/students.csv');
CREATE OR REPLACE VIEW src_attendance AS
    SELECT * FROM read_csv_auto('data/source/attendance.csv');
CREATE OR REPLACE VIEW src_assessments AS
    SELECT * FROM read_csv_auto('data/source/assessments.csv');
CREATE OR REPLACE VIEW src_discipline AS
    SELECT * FROM read_csv_auto('data/source/discipline.csv');
CREATE OR REPLACE VIEW dim_student AS
    SELECT * FROM read_csv_auto('data/processed/dim_student.csv');
CREATE OR REPLACE VIEW fact_attendance AS
    SELECT * FROM read_csv_auto('data/processed/fact_attendance.csv');
CREATE OR REPLACE VIEW fact_assessment AS
    SELECT * FROM read_csv_auto('data/processed/fact_assessment.csv');
CREATE OR REPLACE VIEW fact_discipline AS
    SELECT * FROM read_csv_auto('data/processed/fact_discipline.csv');

WITH active_students AS (
    SELECT Student_ID FROM src_students WHERE Enrollment_Status = 'Active'
)
SELECT 'Source attendance rows outside the analysis population' AS check_name,
       COUNT(*) AS problem_rows
FROM src_attendance
WHERE Student_ID NOT IN (SELECT Student_ID FROM active_students)

UNION ALL

SELECT 'Source assessment rows outside the analysis population',
       COUNT(*)
FROM src_assessments
WHERE Student_ID NOT IN (SELECT Student_ID FROM active_students)

UNION ALL

SELECT 'Source discipline rows outside the analysis population',
       COUNT(*)
FROM src_discipline
WHERE Student_ID NOT IN (SELECT Student_ID FROM active_students)

UNION ALL

SELECT 'Processed attendance rows with no matching student',
       COUNT(*)
FROM fact_attendance
WHERE Student_ID NOT IN (SELECT Student_ID FROM dim_student)

UNION ALL

SELECT 'Processed assessment rows with no matching student',
       COUNT(*)
FROM fact_assessment
WHERE Student_ID NOT IN (SELECT Student_ID FROM dim_student)

UNION ALL

SELECT 'Processed discipline rows with no matching student',
       COUNT(*)
FROM fact_discipline
WHERE Student_ID NOT IN (SELECT Student_ID FROM dim_student)

UNION ALL

SELECT 'Processed attendance rows where present plus absent differs from enrolled',
       COUNT(*)
FROM fact_attendance
WHERE Days_Present + Days_Absent <> Days_Enrolled

UNION ALL

SELECT 'Processed assessment rows breaking the rule Below means score under 70',
       COUNT(*)
FROM fact_assessment
WHERE (Score < 70) <> (Benchmark = 'Below')

UNION ALL

SELECT 'Source Program values written with inconsistent casing',
       COUNT(*)
FROM src_students
WHERE Program NOT IN ('Core', 'MTSS Tier 1', 'MTSS Tier 2', 'MTSS Tier 3')

UNION ALL

SELECT 'Source Benchmark values written with inconsistent casing',
       COUNT(*)
FROM src_assessments
WHERE Benchmark NOT IN ('Met', 'Below');
