# Data Dictionary

This dictionary covers every field in the processed tables in `data/processed` and in the Power BI model tables in `powerbi/model`. The two sets hold the same fields. The original dictionary that shipped with the source extracts is preserved in `docs/original/data_dictionary.csv` and covers the source columns, including the name columns that the pipeline drops.

## dim_student

One row per student in the analysis population. Grain: one row per student.

1. Student_ID. Text. Unique student identifier. Source: students.csv. In the processed tables this value is unique and every fact row matches one value here.
2. Enrollment_Status. Text. Enrollment status from the student table. Source: students.csv. Every row in this table reads Active, because the population is defined as Active students.
3. Program. Text. Program group with four standard values: Core, MTSS Tier 1, MTSS Tier 2, MTSS Tier 3. Source: students.csv. Casing standardized in the pipeline.
4. Enrollment_Date. Date. The date the student enrolled. Source: students.csv. Values run from 3 September 2025 to 20 November 2025.

## fact_attendance

One row per student with an attendance record. Grain: one row per student per attendance period. The source data holds one period summary per student, not one row per day. Row count: 108.

1. Student_ID. Text. Links to dim_student.
2. Grade. Whole number. Grade level from 5 to 8.
3. Days_Enrolled. Whole number. Days the student was enrolled in the period. Range in the processed data: 90 to 179.
4. Days_Present. Whole number. Days the student attended.
5. Days_Absent. Whole number. Days the student was absent. Present plus absent equals enrolled on every processed row.
6. Attendance_Rate. Number with one decimal place. Days present as a percent of days enrolled.
7. Attendance_Band. Text. Project category derived from Attendance_Rate. Below 85 is At Risk, 85 to 89.9 is Needs Monitoring, 90 to 94.9 is On Track, 95 and above is Strong. These are project categories, not official school thresholds.
8. Is_Chronic_Absence. Text, Yes or No. Yes when Attendance_Rate is below 90. This is a project definition written for this analysis, not an official school or district definition.

## fact_assessment

One row per student with an assessment record. Row count: 107. Each student appears at most once, with one subject.

1. Student_ID. Text. Links to dim_student.
2. Grade. Whole number. Grade level from 5 to 8.
3. Assessment. Text. The subject of the assessment: ELA, Math, or Science.
4. Assessment_Date. Date. The date of the assessment. Values run from 15 January 2026 to 14 April 2026.
5. Score. Whole number. The assessment score. Range in the processed data: 43 to 100.
6. Benchmark. Text. Met when the score is 70 or above, Below when the score is under 70. The rule was verified against every processed row. Casing standardized in the pipeline.

## fact_discipline

One row per student with a discipline record. Row count: 109.

1. Student_ID. Text. Links to dim_student.
2. Grade. Whole number. Grade level from 5 to 8.
3. Incidents. Whole number. Total discipline incidents recorded for the student in the period. Range: 0 to 6.
4. Major_Incidents. Whole number. Major incidents, a subset of Incidents. Range: 0 to 2.

## fact_student_summary

One row per student in the population, 110 rows. This table joins the four tables above into a single student level view for Excel and for quick checks. Fields match the tables they came from. A field is blank when the student has no row in the source table for that measure: two students have blank attendance fields, three have blank assessment fields, and one has blank discipline fields. Grade in this table comes from the first fact table that records one for the student. Grade agrees across all three fact tables for every student who appears in more than one of them.

## dim_date

One row per calendar day from 1 September 2025 to 30 April 2026, 242 rows. This table exists in `powerbi/model` only and supports the month views in the report.

1. Date. Date. The calendar day.
2. Year. Whole number. Calendar year.
3. Month. Whole number. Calendar month number from 1 to 12.
4. MonthName. Text. Full month name.
5. YearMonth. Text. Year and month in the form 2026-01. Used as the month axis in charts.
6. MonthLabel. Text. Short month label in the form Jan 2026.
