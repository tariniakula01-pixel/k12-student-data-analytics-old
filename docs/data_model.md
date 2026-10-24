# Data Model

The analysis tables form a small star schema. One dimension table describes the students. Three fact tables hold the measures recorded for each student. A date dimension supports the month views in the Power BI model. The same five tables sit in `data/processed` (without the date table) and in `powerbi/model` (with it).

## Tables and grain

1. `dim_student` holds one row per student in the analysis population: 110 rows. Its key is Student_ID.
2. `fact_attendance` holds one row per student with an attendance record: 108 rows. The grain is one row per student for the attendance period. The source data is a period summary, so there is no daily grain anywhere in this project.
3. `fact_assessment` holds one row per student with an assessment record: 107 rows. Each student has at most one assessment, in one subject.
4. `fact_discipline` holds one row per student with a discipline record: 109 rows.
5. `dim_date` holds one row per calendar day from 1 September 2025 to 30 April 2026: 242 rows. Its key is Date.

## Relationships

1. `fact_attendance` joins to `dim_student` on Student_ID. Many attendance rows to one student row. In the data each student has at most one attendance row, so the relationship behaves as one to one today, but it is modeled as many to one because an attendance table would normally hold many rows per student over time.
2. `fact_assessment` joins to `dim_student` on Student_ID, many to one, for the same reason.
3. `fact_discipline` joins to `dim_student` on Student_ID, many to one, for the same reason.
4. `fact_assessment` joins to `dim_date` on Assessment_Date to Date, many to one. This relationship carries the month views and the month comparison measures.
5. `dim_student` joins to `dim_date` on Enrollment_Date to Date, many to one. This supports enrollment month views if a report needs them.

In Power BI terms, filters flow from the dimension tables to the fact tables in a single direction. A page filtered to one program in `dim_student` restricts every fact table at once, which is what keeps the pages consistent with each other.

## Design choices

1. Grade sits on the fact tables rather than on `dim_student`, because the student table in the source data carries no grade. Grade agrees across the three fact tables for every student who appears in more than one of them, verified during the audit, so no fact table disagrees with another about a student grade.
2. The combined table `fact_student_summary` is not part of the star. It exists for the Excel workbook and for quick checks, one row per student with every measure side by side. Reports should use the star tables so filters behave consistently.
3. Measures are kept as DAX measures in a dedicated `_Measures` table rather than as calculated columns, so each KPI is defined once and reused by every visual. The catalog in `powerbi/dax_measures.md` documents each one.
4. Name fields are excluded from the model entirely. The analysis never needs a student name, and a model without names is safer to share.

## Filter behavior to know

Averages in this model rest on the students who have the relevant fact row. Filtering to one grade, for example, shows the average score of assessed students in that grade. Students without an assessment row never enter a score average, in any tool, because the fact row does not exist. The counts of students with attendance and with an assessment are exposed as measures so a reader can always see the base behind an average.
