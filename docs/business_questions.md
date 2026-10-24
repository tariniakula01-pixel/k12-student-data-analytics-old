# Business Questions

The project answers a short list of questions that a school leadership team would ask about one school year. Every question is answered on the same analysis population of 110 Active students, and every answer can be traced to a SQL file, a notebook section, or a workbook sheet.

## The questions

1. What are the headline numbers for the year? Total students, average attendance rate, average score, the share of assessed students recorded as Met, and the size of the chronic absence group. Answered by `sql/01_kpi_summary.sql`, the KPI Summary sheet in the Excel workbook, and the first page of the Power BI report.
2. Which grades and which programs show the strongest and weakest attendance, and where is absence below 90 percent most common? Answered by `sql/02_attendance_by_grade_program.sql` and the Attendance page of the report.
3. Where are assessment results strongest and weakest by grade and by subject, and how many students sit below the benchmark? Answered by `sql/03_assessment_performance.sql` and the Student Performance page of the report.
4. Do students with stronger attendance record higher scores in this data? Answered by `sql/04_attendance_vs_assessment.sql` and the attendance band section of the notebook. The answer is that this dataset shows almost no relationship, and the finding is documented with its caveats in `docs/insights_and_recommendations.md`.
5. How are discipline incidents spread across grades, and are they concentrated in a few students or shared across many? Answered by `sql/05_discipline_overview.sql` and the discipline section of the notebook.
6. How did results move across the January to April 2026 testing window? Answered by `sql/07_assessment_trend_by_month.sql`, with the warning that each student appears once, so the monthly view describes the testing window rather than growth.
7. Can the numbers be trusted? Which records were changed or removed during cleaning, and do the processed tables pass the validation checks? Answered by `sql/06_data_validation.sql`, `outputs/cleaning_log.csv`, `outputs/validation_results.csv`, and `docs/data_quality_report.md`.

## Questions the data cannot answer

1. Why any pattern exists. The data records no teaching details, no prior achievement, and no home circumstances, so no result in this project explains a cause.
2. Whether students improved over the year. Each student has one assessment record, so growth cannot be measured.
3. How subjects compare for the same students. Each student took one assessment in one subject.
4. How this school compares with other schools. The data covers one school, so the only benchmarks available are the project own groups and its documented definitions.
