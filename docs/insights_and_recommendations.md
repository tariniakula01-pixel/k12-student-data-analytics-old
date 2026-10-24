# Insights and Recommendations

Every finding below comes from the rebuilt analysis on the population of 110 Active students. Each finding states its base, because the counts differ slightly by measure: 108 students have attendance rows, 107 have assessment rows, and 109 have discipline rows. The data is simulated practice data for one school, so the findings describe patterns in this dataset and the working habits they reward. They are not findings about any real school.

## Finding 1: Attendance and scores barely move together in this data

1. Question. Do students with stronger attendance record higher scores?
2. Method. Attendance bands were compared on average score, and the correlation between attendance rate and score was calculated for the 105 students who hold both records. Sources: `sql/04_attendance_vs_assessment.sql` and the notebook band section.
3. Observed result. The correlation reads −0.06, as close to no linear relationship as a real dataset usually gets. The band averages agree. Strong band students average 76.60, On Track students 81.07, Needs Monitoring students 81.27, and At Risk students 77.20. The averages do not climb as attendance rises.
4. Why it matters. A report that assumed the usual pattern would misread this school year. Interventions chosen on that assumption would target attendance as a score lever when this data shows no such link to pull.
5. Recommended next step. Before drawing any program conclusion, a school team should look at score patterns by subject and grade inside each band, and should treat attendance work and academic support as separate efforts with separate evidence until richer data exists.
6. Caveat. One assessment per student, a subject mix that differs across bands, and no record of prior achievement. This finding cannot show that attendance has no effect on learning. It shows only that this dataset does not display the expected relationship.

## Finding 2: One third of students sit in the chronic absence group

1. Question. How large is the group of students with attendance below 90 percent, the project definition of chronic absence?
2. Method. The Is_Chronic_Absence flag built in the pipeline was counted across the 108 students with attendance rows. Sources: `sql/01_kpi_summary.sql` and the attendance distribution in the notebook.
3. Observed result. 36 of 108 students, 33.3 percent, sit below 90 percent. 21 students sit below 85 percent. The median attendance rate is 93.55 percent, so the typical student attends well while a large minority does not.
4. Why it matters. The headline average of 91.84 percent sounds comfortable and would hide this group in a summary report. A third of the school attending under 90 percent is the fact a leadership team needs first.
5. Recommended next step. Report attendance as a distribution and a group count alongside the average in any recurring report, and review the below 85 percent group student by student, since 21 students is a list a counselor team can actually work through.
6. Caveat. The 90 percent line is a project definition, not an official threshold, and the attendance data is a period summary with no dates, so nothing here shows when the absences happened.

## Finding 3: MTSS Tier 1 students show the weakest attendance and benchmark results

1. Question. Which program groups show the weakest outcomes?
2. Method. Attendance and assessment results were grouped by program in `sql/02_attendance_by_grade_program.sql` and `sql/03_assessment_performance.sql`, with student counts beside every figure.
3. Observed result. MTSS Tier 1 students record the lowest average attendance at 90.08 percent, the highest chronic absence rate at 50.0 percent of its 26 students with attendance rows, the lowest average score at 74.93, and the lowest share at Met at 60.7 percent. Tier 1 is the lightest support tier in the MTSS model.
4. Why it matters. The group receiving the lightest support is the group with the weakest snapshot on two separate measures. That pairing deserves a review of whether tier placements and tier supports are doing what the model intends.
5. Recommended next step. A school team should review the Tier 1 list against current teacher knowledge, check whether placement reviews are scheduled, and confirm that Tier 1 supports are actually reaching these students. The data supports opening that review; it does not carry the answer.
6. Caveat. Tier 1 holds 28 students, and placement into a tier reflects need, so weaker results inside a support tier are partly the model working as designed. MTSS Tier 3 holds only nine students, and its higher averages should not be read as firmly as the larger groups.

## Finding 4: Grade 6 records the weakest benchmark results

1. Question. Which grade shows the weakest assessment results?
2. Method. Assessment results were grouped by grade in `sql/03_assessment_performance.sql`.
3. Observed result. Grade 6 records 63.6 percent of its assessed students at Met and the lowest average score at 76.50. Grade 7 records 81.8 percent at Met, grade 8 records 78.9 percent, and grade 5 records 76.0 percent.
4. Why it matters. Grade 6 is the transition year into the upper grades in many schools, and a gap this size, about 18 points of percent Met under grade 7, is the kind of signal that should reach a leadership agenda while the year can still respond to it.
5. Recommended next step. Look at the grade 6 results by subject before any wider conclusion, since the subject mix can move a grade figure, and review the eight grade 6 students recorded as Below as a named list.
6. Caveat. Grade 6 rests on 22 assessed students. Two or three students changing category would move the percent Met figure by about ten points, so the size of the gap is less certain than its direction.

## Finding 5: Subject results differ, and the comparison itself is limited

1. Question. How do results differ across ELA, Math, and Science?
2. Method. Assessment results were grouped by subject in `sql/03_assessment_performance.sql`.
3. Observed result. ELA records 87.5 percent at Met with an average score of 81.69 across 32 students. Math records 76.5 percent at Met with an average of 76.68 across 34 students. Science records 65.9 percent at Met with an average of 77.46 across 41 students, and holds 14 of the 26 Below results.
4. Why it matters. Science carries the largest share of Below results, so support planning that reads only the whole school figure would miss where the Below group is concentrated.
5. Recommended next step. Treat the subject split as a prompt to check the assessment design and the student assignment pattern: which students were assigned which subject, and whether the Science assessment was harder or the group weaker. If the school can assess every student in every subject in a future cycle, the comparison becomes direct.
6. Caveat. Each student took one assessment in one subject, so these rows compare different groups of students. The gap may reflect who sat each subject as much as the subjects themselves. No ranking of teaching quality can be drawn from it.

## Finding 6: Discipline incidents are widespread but shallow, and grade 8 carries the highest rate

1. Question. Are discipline incidents concentrated in a few students or spread across many, and how do grades compare?
2. Method. Discipline records were summarized in `sql/05_discipline_overview.sql`, using incidents per student for grade comparisons because grade sizes differ.
3. Observed result. 78 of 109 students, 71.6 percent, hold at least one incident, while the average is 1.32 incidents per student and only 14 students hold three or more. Grade 8 records the highest rate at 1.60 incidents per student and the highest total at 64 incidents, with 5 of the 13 major incidents. Grade 7 records the lowest rate at 0.95.
4. Why it matters. The pattern is a broad base of single incidents rather than a small group in crisis. That shape points toward schoolwide expectations and early responses rather than intensive work with a handful of students, apart from the 14 students with repeated incidents who do need individual attention.
5. Recommended next step. Keep the two views separate in reporting: a schoolwide view for the broad base, and a named review of the 14 students with three or more incidents. Compare grades on incidents per student, never on raw totals.
6. Caveat. Incident recording depends on staff practice, which this data cannot show. A grade with more recorded incidents may record more carefully rather than behave worse, so the figures open a conversation rather than settle one.

## Finding 7: The shipped files described a different population in every table

1. Question. Can the numbers in the original project be trusted as one consistent story?
2. Method. The audit compared identifiers across the four source files, reran the original README headline figures on a single defined population, and recorded the differences in `docs/data_quality_report.md`.
3. Observed result. The fact tables held 11, 11, and 10 rows outside any single population definition, including 11 rows pointing at students absent from the student table entirely. Two category values carried casing errors that split their groups. The original headline figures shifted when rebuilt on one population: average score 78.1 became 78.48, and the count of students below 85 percent attendance moved from 22 to 21.
4. Why it matters. None of the errors was large, and every one of them was invisible in the finished reports. A reader of the original dashboard had no way to know that its attendance average and its score average described different sets of students. Trust in a report rests on exactly this layer.
5. Recommended next step. Any recurring version of this reporting should keep the population definition, the cleaning log, and the validation checks as standing parts of the workflow, and should print the base count beside every average.
6. Caveat. The absolute differences are small in this dataset. The finding is about method rather than magnitude: on a larger and messier extract, the same habits decide whether the numbers hold up.
