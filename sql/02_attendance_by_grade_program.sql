-- Query 02: Attendance by grade and by program
--
-- Business question
--   Which grades and which programs have the strongest and weakest
--   attendance, and where is absence below 90 percent most common?
--
-- What this query returns
--   One row per grade and one row per program, marked in the grouping
--   column. Each row shows the student count, the average attendance
--   rate, the share of students in the chronic absence group as defined
--   by this project (a rate below 90 percent), and the average number
--   of days absent. The rank_in_group column ranks the rows inside
--   each grouping by average attendance, highest first.
--
-- How to read it
--   Grade 8 is the largest grade, so its averages rest on more students
--   than the MTSS Tier 3 program group, which holds nine students.
--   Small groups move a lot when one student changes, so read the
--   student count next to every average.

CREATE OR REPLACE VIEW fact_student_summary AS
    SELECT * FROM read_csv_auto('data/processed/fact_student_summary.csv');

WITH grouped AS (
    SELECT
        'Grade' AS grouping,
        CAST(Grade AS VARCHAR) AS group_name,
        COUNT(Attendance_Rate) AS students,
        ROUND(AVG(Attendance_Rate), 2) AS average_attendance_rate,
        ROUND(100.0 * SUM(CASE WHEN Is_Chronic_Absence = 'Yes' THEN 1 ELSE 0 END)
            / COUNT(Attendance_Rate), 1) AS chronic_absence_rate,
        ROUND(AVG(Days_Absent), 1) AS average_days_absent
    FROM fact_student_summary
    GROUP BY Grade

    UNION ALL

    SELECT
        'Program' AS grouping,
        Program AS group_name,
        COUNT(Attendance_Rate) AS students,
        ROUND(AVG(Attendance_Rate), 2) AS average_attendance_rate,
        ROUND(100.0 * SUM(CASE WHEN Is_Chronic_Absence = 'Yes' THEN 1 ELSE 0 END)
            / COUNT(Attendance_Rate), 1) AS chronic_absence_rate,
        ROUND(AVG(Days_Absent), 1) AS average_days_absent
    FROM fact_student_summary
    GROUP BY Program
)
SELECT
    grouping,
    group_name,
    students,
    average_attendance_rate,
    chronic_absence_rate,
    average_days_absent,
    RANK() OVER (
        PARTITION BY grouping ORDER BY average_attendance_rate DESC
    ) AS rank_in_group
FROM grouped
ORDER BY grouping, rank_in_group;
