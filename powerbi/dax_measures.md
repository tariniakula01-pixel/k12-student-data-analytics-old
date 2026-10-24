# DAX Measure Catalog

This catalog lists every measure in the Power BI semantic model. Each entry gives the measure name, a plain English definition, the DAX formula, and notes on the denominator and the population. All measures live in a dedicated measures table named `_Measures` so they are easy to find inside Power BI.

The model tables are `dim_student`, `fact_attendance`, `fact_assessment`, `fact_discipline`, and `dim_date`. The population for every measure is the analysis population of 110 Active students. Counts of students differ between measures because two students have no attendance row and three have no assessment row. Each measure that rests on a smaller base says so.

One definition matters throughout. The Average Attendance Rate is the average of individual student attendance rates, so each student counts once and counts equally. It is not weighted by days enrolled. A day weighted rate across the same students would read 92.33 percent instead of 91.84 percent. The project uses the student level average everywhere so that SQL, Python, Excel, and Power BI agree.

## Student counts

### Total Students

Definition: the number of students in the analysis population.

```dax
Total Students = COUNTROWS ( dim_student )
```

Notes: returns 110 on the current data. This is the base count for the whole report.

### Students With Attendance

Definition: the number of students who have an attendance row.

```dax
Students With Attendance = COUNTROWS ( fact_attendance )
```

Notes: returns 108. Two Active students, S1008 and S1030, have no attendance row in the source data.

### Students With Assessment

Definition: the number of students who have an assessment row.

```dax
Students With Assessment = COUNTROWS ( fact_assessment )
```

Notes: returns 107. Three Active students, S1007, S1019, and S1044, have no assessment row.

## Attendance measures

### Average Attendance Rate

Definition: the average of the attendance rates of students who have an attendance row.

```dax
Average Attendance Rate = AVERAGE ( fact_attendance[Attendance_Rate] )
```

Notes: returns 91.84 on the current data, based on 108 students. See the weighting note at the top of this catalog.

### Total Days Absent

Definition: the total days absent across students with an attendance row.

```dax
Total Days Absent = SUM ( fact_attendance[Days_Absent] )
```

Notes: returns 1105 on the current data.

### Chronic Absence Count

Definition: the number of students whose attendance rate falls below 90 percent, the chronic absence definition written for this project.

```dax
Chronic Absence Count =
CALCULATE (
    COUNTROWS ( fact_attendance ),
    fact_attendance[Is_Chronic_Absence] = "Yes"
)
```

Notes: returns 36 on the current data. The 90 percent line is a project definition, not an official school or district definition.

### Chronic Absence Rate

Definition: the share of students with an attendance row who fall in the chronic absence group.

```dax
Chronic Absence Rate =
DIVIDE ( [Chronic Absence Count], [Students With Attendance] )
```

Notes: returns 33.3 percent on the current data. The denominator is the 108 students with attendance rows, not the full population of 110.

## Assessment measures

### Average Score

Definition: the average assessment score across students who have an assessment row.

```dax
Average Score = AVERAGE ( fact_assessment[Score] )
```

Notes: returns 78.48 on the current data, based on 107 students.

### Students Met Benchmark

Definition: the number of assessed students recorded as Met, which means a score of 70 or above in this data.

```dax
Students Met Benchmark =
CALCULATE (
    COUNTROWS ( fact_assessment ),
    fact_assessment[Benchmark] = "Met"
)
```

Notes: returns 81 on the current data.

### Students Below Benchmark

Definition: the number of assessed students recorded as Below, which means a score under 70 in this data.

```dax
Students Below Benchmark =
CALCULATE (
    COUNTROWS ( fact_assessment ),
    fact_assessment[Benchmark] = "Below"
)
```

Notes: returns 26 on the current data.

### Percent Met Benchmark

Definition: the share of assessed students recorded as Met.

```dax
Percent Met Benchmark =
DIVIDE ( [Students Met Benchmark], [Students With Assessment] )
```

Notes: returns 75.7 percent on the current data. The denominator is the 107 assessed students. Students without an assessment row are not counted as Below; they are simply not in this measure.

## Discipline measures

### Total Incidents

Definition: the total discipline incidents recorded across students with a discipline row.

```dax
Total Incidents = SUM ( fact_discipline[Incidents] )
```

Notes: returns 144 on the current data, based on 109 students.

### Total Major Incidents

Definition: the total major discipline incidents recorded across students with a discipline row.

```dax
Total Major Incidents = SUM ( fact_discipline[Major_Incidents] )
```

Notes: returns 13 on the current data.

### Students With Incidents

Definition: the number of students with at least one recorded incident.

```dax
Students With Incidents =
CALCULATE (
    COUNTROWS ( fact_discipline ),
    fact_discipline[Incidents] > 0
)
```

Notes: returns 78 on the current data.

### Average Incidents Per Student

Definition: total incidents divided by the number of students with a discipline row.

```dax
Average Incidents Per Student =
DIVIDE ( [Total Incidents], COUNTROWS ( fact_discipline ) )
```

Notes: returns 1.32 on the current data. This per student view is the fair way to compare grades of different sizes.

## Month comparison measures

The assessment dates run from January to April 2026, and the model holds a date table, so one month comparison is included. Read it with the project caveat: each student appears once, in one subject, in one month, so a change between months can reflect which students were assessed rather than any change in learning.

### Average Score Previous Month

Definition: the average score in the month before the month in the current filter context.

```dax
Average Score Previous Month =
CALCULATE (
    [Average Score],
    DATEADD ( dim_date[Date], -1, MONTH )
)
```

Notes: returns blank for January 2026 because the data holds no December 2025 assessments. The measure needs the date table marked as the model date table, or the relationships from `fact_assessment` to `dim_date` in place, to behave as described.

### Average Score Month Change

Definition: the average score in the current month minus the average score in the previous month, in score points.

```dax
Average Score Month Change =
[Average Score] - [Average Score Previous Month]
```

Notes: returns blank for January 2026. On the current data the month averages are 80.29 for January, 78.47 for February, 77.35 for March, and 79.53 for April, so the changes are small and rest on different groups of students each month.
