-- Query 04: Attendance band and assessment score
--
-- Business question
--   Do students with stronger attendance record higher assessment
--   scores in this data?
--
-- What this query returns
--   One row per attendance band, in band order from lowest attendance
--   to highest. Each row shows the student count, the average score,
--   the share of students recorded as Met, and the overall correlation
--   between attendance rate and score for the 105 students who have
--   both an attendance row and a score.
--
-- How to read it
--   The correlation sits close to zero, and the band averages do not
--   climb in step with attendance. In this one snapshot, attendance
--   alone does not line up with scores in the way many people expect.
--   That is an observation about this dataset, not proof that
--   attendance has no effect. Each student took one assessment in one
--   subject, the subject mix differs across bands, and other factors
--   are not recorded here.

CREATE OR REPLACE VIEW fact_attendance AS
    SELECT * FROM read_csv_auto('data/processed/fact_attendance.csv');
CREATE OR REPLACE VIEW fact_assessment AS
    SELECT * FROM read_csv_auto('data/processed/fact_assessment.csv');

WITH joined AS (
    SELECT
        a.Attendance_Band,
        a.Attendance_Rate,
        s.Score,
        s.Benchmark
    FROM fact_attendance AS a
    INNER JOIN fact_assessment AS s
        ON a.Student_ID = s.Student_ID
)
SELECT
    Attendance_Band,
    COUNT(*) AS students,
    ROUND(AVG(Score), 2) AS average_score,
    ROUND(100.0 * SUM(CASE WHEN Benchmark = 'Met' THEN 1 ELSE 0 END)
        / COUNT(*), 1) AS percent_met,
    (SELECT ROUND(corr(Attendance_Rate, Score), 3) FROM joined)
        AS overall_correlation
FROM joined
GROUP BY Attendance_Band
ORDER BY
    CASE Attendance_Band
        WHEN 'At Risk' THEN 1
        WHEN 'Needs Monitoring' THEN 2
        WHEN 'On Track' THEN 3
        WHEN 'Strong' THEN 4
    END;
