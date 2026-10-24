# KPI Definitions

Every KPI in this project is defined here once, with its formula, its base, and how to read it. The same definitions are used in the SQL files, the Python notebook, the Excel workbook, and the DAX measures in `powerbi/dax_measures.md`. All KPIs describe the analysis population of 110 Active students unless a base is stated.

## Total Students

Formula: count of rows in `dim_student`. Value: 110. Read it as the size of the analysis population. The student table in the source data holds 117 students; seven are Withdrawn and sit outside the population.

## Average Attendance Rate

Formula: the average of Attendance_Rate across `fact_attendance`. Value: 91.84. Base: 108 students with an attendance row. Each student counts once and counts equally. This is not weighted by days enrolled. A day weighted rate across the same students would read 92.33. The project uses the student level average so that a student enrolled for 90 days counts the same as a student enrolled for 179 days when the question is about students rather than days.

## Chronic Absence Count and Rate

Definition: a student is in the chronic absence group when their attendance rate is below 90 percent. This is a definition written for this project. It is not an official school or district definition.
Count formula: count of attendance rows where Is_Chronic_Absence is Yes. Value: 36.
Rate formula: the count divided by the 108 students with attendance rows. Value: 33.3 percent.

## Attendance Bands

Project categories derived from Attendance_Rate. Below 85 is At Risk, with 21 students. 85 to 89.9 is Needs Monitoring, with 15 students. 90 to 94.9 is On Track, with 28 students. 95 and above is Strong, with 44 students. Counts rest on the 108 students with attendance rows. The bands come from the original version of this project and are kept so the two versions stay comparable. They are analysis categories, not official school thresholds.

## Average Score

Formula: the average of Score across `fact_assessment`. Value: 78.48. Base: 107 students with an assessment row.

## Percent Met Benchmark

Formula: students recorded as Met divided by students with an assessment row, times 100. Value: 75.7 percent, from 81 of 107. Met means a score of 70 or above; Below means a score under 70. Students without an assessment row are not counted in either group. They are missing, not Below, and the distinction matters when the figure is quoted.

## Students Below Benchmark

Formula: count of assessment rows where Benchmark is Below. Value: 26. Their scores run from 43 to 69, and 21 of the 26 scored between 60 and 69.

## Total Incidents and Average Incidents Per Student

Total formula: sum of Incidents across `fact_discipline`. Value: 144, with 13 major incidents inside that total. Base: 109 students with a discipline row.
Average formula: total incidents divided by students with a discipline row. Value: 1.32. The per student figure is the fair comparison between grades of different sizes. Grade totals rise with grade size, so a grade ranking by totals alone would mostly restate the class sizes.

## Students With Incidents

Formula: count of discipline rows where Incidents is above zero. Value: 78 of 109, which is 71.6 percent.

## Average Score Month Change

Formula: the average score in one assessment month minus the average score in the month before it, in score points. Values: February reads 1.82 points under January, March reads 1.12 points under February, and April reads 2.18 points above March. January has no earlier month in the data, so its change is blank. Read this KPI with its caveat: every month rests on a different group of students and a different subject mix, so the change describes the testing window rather than any movement in learning.
