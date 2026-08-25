# Project Methodology

## 1. Source Data
Four related datasets were used: Students, Attendance, Assessments, and Discipline. `Student_ID` is the common identifier; conceptually it acts as the primary identifier in the student master dataset and a linking/foreign-key field in the related datasets.

## 2. Profiling
Checks included record counts, duplicate IDs, missing values, invalid values, formatting, data types, and logical consistency.

## 3. Cleaning Rules
Only defensible corrections were made. Exact duplicates can be removed after documentation; conflicting records remain flagged. Derived values are calculated only when reliable source fields support them.

## 4. Analysis-Ready Layer
The analysis-ready data excludes unresolved/ambiguous records from valid student-level analysis. This prevents bad records from being reintroduced simply to increase the row count.

## 5. Analysis
The project uses KPIs and grouped summaries to compare grades and programs. Attendance bands are used to make attendance analysis easier to interpret:

- `<85%` — At Risk
- `85–89.9%` — Needs Monitoring
- `90–94.9%` — On Track
- `95%+` — Strong Attendance

These are project analysis categories, not official school thresholds.

## 6. Reporting
The leadership dashboard prioritizes a small set of KPIs, grade/program comparisons, attendance-band distribution, and concise takeaways. Findings are phrased as observations rather than causal claims.

## 7. Privacy
The GitHub-ready copy removes student first/last-name fields. Do not publish real student PII, protected records, or confidential SIS exports to a public repository.
