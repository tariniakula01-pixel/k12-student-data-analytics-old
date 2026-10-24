# Interview Walkthrough

This guide explains the project in the order a hiring manager usually asks about it. It is written to be rehearsed from. Every answer stays inside what the project actually does, so anything said in an interview can be shown in the repository a minute later.

## 1. What is this project?

A short answer: the project takes four messy school data extracts covering students, attendance, assessments, and discipline, and turns them into one consistent set of reports. It covers one school, grades 5 to 8, in the 2025 to 2026 school year. The data is simulated practice data, and the project says so openly. The point of the project is the workflow: profile the data, clean it with documented rules, validate the result, analyze it in SQL and Python, and report it in Excel and Power BI, with every headline number reconciled across tools.

If asked why a school would want this: leadership teams make decisions from attendance and assessment summaries. When the tables behind those summaries describe different groups of students, the decisions rest on numbers that quietly disagree with each other. This project is built around preventing that.

## 2. What did the data look like when you received it?

Four CSV extracts. The student table held 117 students. Attendance held 119 rows, assessments 118, and discipline 119. The counts already disagree, which was the first signal. Profiling found rows in the fact tables for students who do not exist in the student table, including two identifiers that look like test records, S9999 and S8888. Two category fields carried casing errors: one program written as "MTSS tier 2" and one benchmark written as "met". The student file also carried name columns even though the project documentation said names had been removed.

What was sound: the attendance arithmetic was correct on every row, present plus absent equaled enrolled throughout, and the benchmark field followed a clean rule, Below under 70 and Met at 70 and above, on every row.

## 3. What cleaning decisions did you make, and why?

The biggest decision was the population. The analysis uses the 110 students listed as Active. The seven Withdrawn students are excluded because their records cover a part year, and mixing part year records into averages would treat them as full year students. Every table was then filtered to that one population, and each removed row is listed in the cleaning log with its reason.

The casing errors were fixed with a fixed mapping because the intended values were unambiguous. Names were dropped from every output because the analysis never uses them. Missing records were left missing: two students have no attendance row and three have no assessment row, and no values were invented for them, because a filled in score would flow into every average. No outliers were removed. A score of 43 is unusual, not impossible, and it passes every arithmetic check, so it stays.

The rule that ties it together: correct only what a documented rule supports, flag or exclude the rest, and write down everything.

## 4. Three SQL queries to be ready to explain

First, the KPI summary in `sql/01_kpi_summary.sql`. In words: it builds the headline numbers with subqueries, one per KPI, each reading the table that owns the measure. The part worth explaining is that the counts differ by KPI on purpose. The average attendance rate rests on 108 students and the average score on 107, and the query prints those bases beside the averages so nobody quotes an average without its base.

Second, the attendance query in `sql/02_attendance_by_grade_program.sql`. It uses a common table expression to build grade rows and program rows in one shape, joins them with UNION ALL, and then applies a RANK window function inside each grouping. The talking point: RANK answers the question a leader actually asks, which group is first and which is last, and the student count sits beside every average because the MTSS Tier 3 group holds nine students and its average moves easily.

Third, the validation query in `sql/06_data_validation.sql`. It counts problem rows rather than listing successes. The checks on the source files show what was wrong, 11 attendance rows outside the population, 11 assessment rows, 10 discipline rows, and 2 casing errors. The same checks on the processed tables all return zero. Explaining this file well shows a habit managers value: proof that the numbers were checked, not just produced.

## 5. What do the DAX measures do?

There are 17 measures in one measures table, listed in `powerbi/dax_measures.md`. The pattern is simple. Base measures count rows or average a column, such as Total Students as COUNTROWS of the student table and Average Score as AVERAGE of the score column. Derived measures build on the base ones with DIVIDE, so Percent Met Benchmark divides Students Met Benchmark by Students With Assessment. DIVIDE matters because it returns blank instead of an error when a denominator is zero, which happens when a report is filtered to a group with no assessed students. CALCULATE with a simple filter produces the group counts, such as the chronic absence count of students whose flag reads Yes.

Two measures compare months with DATEADD over the date table. The honest point to make about them: they are included because the date coverage supports them, and their documentation carries the caveat that each month rests on different students, so a month change describes the testing window rather than learning growth.

One definition to be ready for: the average attendance rate is the average of student level rates, each student counted equally, not a rate weighted by days enrolled. The weighted version would read 92.33 against 91.84. The project picked the student level view because its questions are about students.

## 6. How should each dashboard page be read?

Page 1, Executive Summary, answers what is happening: four KPI cards, attendance by grade, the chronic absence rate by program, the score trend across the testing window, and percent Met by grade and subject. The reading habit to describe is that the cards give the headline, and the charts immediately qualify it. The average attendance of 91.84 looks fine until the chronic absence figure of one third of students sits two charts away.

Page 2, Student Performance, covers the score distribution, results by grade and subject, and a program table. Its caveat is printed in the project documentation: each student took one assessment in one subject, so the subject comparison compares groups of students.

Page 3, Attendance, covers the distribution, the bands, and the chronic absence group, with the project definitions stated on the page notes. The band chart against average score carries the project most surprising result, covered in the findings.

Page 4, Equity and Program, places every program result beside its student count. The habit to name: in this project, no group average is ever shown without the size of the group, because a nine student group and a 55 student group should not be read with the same confidence.

## 7. The top three findings

First, attendance and scores barely move together in this data. The correlation is −0.06 across 105 students, and the Strong attendance band averages a lower score, 76.60, than the Needs Monitoring band at 81.27. The interview safe framing: this is one snapshot with one assessment per student, so the finding is that this dataset does not show the expected link, not that attendance does not matter.

Second, one third of students, 36 of 108, sit below the 90 percent attendance line that the project uses for chronic absence, while the median student attends 93.55 percent of days. The average hides the group; the distribution shows it.

Third, MTSS Tier 1 students, the lightest support tier, record the weakest attendance and the weakest benchmark results: 90.08 percent average attendance, half of them in the chronic absence group, and 60.7 percent at Met. The framing: the data supports opening a placement and support review. It does not carry the conclusion.

## 8. Honest limitations to volunteer before being asked

1. The data is simulated. The project demonstrates method on realistic shaped data, and says so in the README.
2. Attendance is a period summary with no dates, so nothing can be said about when absences happened.
3. One assessment per student means no growth measurement and no fair subject comparison for the same students.
4. Nothing in the data supports a cause. Every finding is a pattern with a recommended investigation, not an explanation.
5. The Power BI project files were authored as text in the PBIP format on a Linux machine and have not been opened in Power BI Desktop yet. The numbers behind the report were validated in SQL, Python, and Excel, and the manual steps to open and check the report are written in `powerbi/README.md`. Do not claim the report was tested in Desktop.

Volunteering the fifth point early is a strength. It shows the difference between a number that was reconciled three ways and a file format that still needs its first open in Desktop, and it shows that the distinction is understood rather than discovered by the interviewer.
