-- Query 01: Headline KPI summary
--
-- Business question
--   What are the headline numbers for this school in the 2025 to 2026
--   school year, using one consistent group of students?
--
-- What this query returns
--   One row with the headline KPIs. Every KPI is calculated on the
--   analysis population of 110 Active students built by
--   scripts/02_clean_and_validate.py. Counts of students differ by KPI
--   because two students have no attendance row and three have no
--   assessment row. The students_with_attendance and
--   students_with_assessment columns state the base for each average.
--
-- How to read it
--   percent_met_benchmark uses the project rule that a score of 70 or
--   above is recorded as Met. chronic_absence_rate uses the project
--   definition of an attendance rate below 90 percent.

CREATE OR REPLACE VIEW dim_student AS
    SELECT * FROM read_csv_auto('data/processed/dim_student.csv');
CREATE OR REPLACE VIEW fact_attendance AS
    SELECT * FROM read_csv_auto('data/processed/fact_attendance.csv');
CREATE OR REPLACE VIEW fact_assessment AS
    SELECT * FROM read_csv_auto('data/processed/fact_assessment.csv');
CREATE OR REPLACE VIEW fact_discipline AS
    SELECT * FROM read_csv_auto('data/processed/fact_discipline.csv');

SELECT
    (SELECT COUNT(*) FROM dim_student) AS total_students,
    (SELECT COUNT(*) FROM fact_attendance) AS students_with_attendance,
    (SELECT ROUND(AVG(Attendance_Rate), 2) FROM fact_attendance)
        AS average_attendance_rate,
    (SELECT COUNT(*) FROM fact_assessment) AS students_with_assessment,
    (SELECT ROUND(AVG(Score), 2) FROM fact_assessment) AS average_score,
    (SELECT ROUND(
        100.0 * SUM(CASE WHEN Benchmark = 'Met' THEN 1 ELSE 0 END) / COUNT(*), 1)
     FROM fact_assessment) AS percent_met_benchmark,
    (SELECT COUNT(*) FROM fact_assessment WHERE Benchmark = 'Below')
        AS students_below_benchmark,
    (SELECT COUNT(*) FROM fact_attendance WHERE Is_Chronic_Absence = 'Yes')
        AS chronic_absence_count,
    (SELECT ROUND(
        100.0 * SUM(CASE WHEN Is_Chronic_Absence = 'Yes' THEN 1 ELSE 0 END)
        / COUNT(*), 1)
     FROM fact_attendance) AS chronic_absence_rate,
    (SELECT SUM(Incidents) FROM fact_discipline) AS total_incidents,
    (SELECT COUNT(*) FROM fact_discipline WHERE Incidents > 0)
        AS students_with_incidents,
    (SELECT ROUND(AVG(Incidents), 2) FROM fact_discipline)
        AS average_incidents_per_student;
