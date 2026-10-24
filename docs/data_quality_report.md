# Data Quality Report

This report records what was wrong with the source extracts, how each problem was treated, and the before and after counts. The full record of every change sits in `outputs/cleaning_log.csv`. The checks that guard the processed tables sit in `outputs/validation_results.csv` and in `sql/06_data_validation.sql`.

## The problems found

### 1. Fact rows that point at students outside the population

The three fact tables held rows whose Student_ID does not belong to any Active student in the student table: 11 attendance rows, 11 assessment rows, and 10 discipline rows.

Inside those counts sit 11 rows that point at students who do not appear in the student table at all. Attendance holds four of them, for S1004, S1005, S1011, and S9999. Assessments holds four, for S1004, S1005, S1011, and S8888. Discipline holds three, for S1004, S1005, and S1011. The remaining rows belong to the seven Withdrawn students, who appear in the student table but sit outside the analysis population.

Treatment: every such row is excluded from the processed fact tables, and each exclusion is listed in the cleaning log with its reason. Nothing was deleted from the source files. The effect matters: in the shipped files, each table described a different group of students, so an attendance average and a score average were calculated on different populations without any sign on the page.

### 2. Inconsistent casing in two category fields

Student S1025 carries the program value "MTSS tier 2" while every other row uses "MTSS Tier 2". Student S1029 carries the benchmark value "met" while every other row uses "Met". Any group summary in Excel, SQL, or Power BI would split those single students into groups of their own.

Treatment: both fields are standardized in the pipeline with a fixed mapping, and both changes are in the cleaning log. After cleaning, a validation check confirms that no Program value sits outside the four standard values and no Benchmark value sits outside Met and Below.

### 3. Flagged records from the original quality log that sit missing from single files

The original data quality log, preserved in `docs/original/data_quality_log.csv`, documents issues found during the first version of this project: a duplicate student record with conflicting details for S1004, days present above days enrolled for S1008, a score of 130 for S1007, a missing score for S1019, an incident count recorded as negative 2 for S1012, a corrected absence value for S1021, a populated attendance rate for S1015, and an unknown grade for S1011.

In the shipped source files, some of those records are simply absent from exactly one file. S1008 has no attendance row. S1007 and S1019 have no assessment rows. S1012 has no discipline row. Meanwhile S1004 and S1011, whose student records were held back, still have rows in all three fact tables. The pattern reads as an earlier partial fix: the questionable rows were dropped file by file, which left the tables describing different students.

Treatment: the rebuild takes one consistent route. The population is defined once, from the student table, and every fact table is filtered to that population. Students whose flagged rows are missing keep their other records, and the gaps are visible in the summary table as blank fields with known counts: two students without attendance, three without an assessment, one without a discipline row.

### 4. Student names carried in a file described as name free

The original methodology states that the GitHub copy removes student name fields. The shipped student file still holds a Last_Name column and a Full Name column. The data is simulated, so no real student is exposed, but the file did not match its own documentation.

Treatment: the pipeline drops both name columns from every processed output. The source extract keeps them, because the source layer is preserved as received, and the drop is recorded in the cleaning log.

### 5. Headline figures in the original README that do not reconcile

The original README reported 117 valid students, an average attendance rate of 91.8, an average score of 78.1, 22 students below 85 percent attendance, grade 8 with the highest discipline incidents at 64, and grade 7 with the highest average attendance at 93.5.

Rechecked on the rebuilt population of 110 Active students, the figures read: 110 students, an average attendance rate of 91.84 across 108 students, an average score of 78.48 across 107 students, and 21 students below 85 percent attendance. The discipline and grade 7 attendance readings hold: grade 8 still records 64 incidents in total and the highest rate per student, and grade 7 still records the highest average attendance, now 93.25. The small shifts come from the population definition, not from new data. This is the practical reason the project now states its population next to every headline figure.

## Before and after counts

1. Attendance rows outside the analysis population: 11 before, 0 after.
2. Assessment rows outside the analysis population: 11 before, 0 after.
3. Discipline rows outside the analysis population: 10 before, 0 after.
4. Program values with inconsistent casing: 1 before, 0 after.
5. Benchmark values with inconsistent casing: 1 before, 0 after.
6. Attendance rows where present plus absent differs from enrolled: 0 before, 0 after. The source arithmetic was already sound.
7. Assessment rows breaking the rule that Below means a score under 70: 0 before, 0 after. The benchmark rule was already sound.

## Validation after cleaning

The pipeline runs 15 checks on the processed tables. All 15 pass. The checks cover the row counts of every table, zero fact rows without a matching student, the attendance arithmetic, the benchmark rule, the standardized category lists, duplicate student identifiers in the summary table, attendance rates inside 0 to 100, and a grade present for every student in the summary. The results sit in `outputs/validation_results.csv`, and the headline KPIs were calculated independently in pandas and in DuckDB and agree exactly, as recorded in `outputs/kpi_reconciliation.csv`.
