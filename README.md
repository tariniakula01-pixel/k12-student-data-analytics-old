# Quad Prep — Data Specialist Practice Project

![Data Quality](https://img.shields.io/badge/focus-data%20quality-16324F) ![Excel](https://img.shields.io/badge/tool-Excel-217346) ![Power%20BI](https://img.shields.io/badge/tool-Power%20BI-F2C811)

## Overview

An end-to-end student-data analytics portfolio project designed around the workflow expected of a Data Specialist: data profiling, quality validation, defensible cleaning, documentation, analysis-ready data, KPI analysis, and leadership reporting.

> **Portfolio note:** This repository uses a practice/anonymized student dataset. It is not an official Quad Preparatory School dataset or policy analysis. Attendance bands used in the dashboard are analysis categories created for this project.

## Business Questions

- How many valid students are represented in the analysis population?
- What is the overall attendance and assessment performance?
- How do attendance and assessment outcomes differ by grade and program?
- Which attendance groups may warrant additional investigation?
- Where do data-quality issues require source-system follow-up?

## Workflow

**Raw data → Profile → Clean → Data Quality Log + Data Dictionary → Analysis Ready → Student Outcome Analysis → KPIs + PivotTables → Leadership Dashboard**

The project deliberately separates **known corrections** from **ambiguous issues**. A value is corrected only when the available data or a documented rule supports the correction; otherwise the issue is flagged for review.

## Key Data-Quality Examples

- Conflicting duplicate Student_ID: retained for source verification rather than guessing which record is correct.
- Days Absent of `-1`: corrected to `3` when `97 enrolled - 94 present = 3` was mathematically supported.
- Days Present greater than Days Enrolled: flagged because the source value requiring correction could not be determined safely.
- Missing assessment score: flagged rather than converted to zero.
- Assessment values above 100: flagged because the scoring scale was not established; the project does not assume a 0–100 scale.
- Negative discipline incident count: flagged because the correct value could not be inferred.

## Results Snapshot

| Metric | Result |
|---|---:|
| Valid students | 117 |
| Average attendance | 91.8% |
| Average assessment score | 78.1 |
| Students below 85% attendance | 22 |
| Grade with highest recorded discipline incidents | Grade 8 (64) |
| Grade with highest average attendance | Grade 7 (93.5%) |

These results are descriptive observations from the practice dataset. They should not be interpreted as causal findings.

## Repository Structure

```text
quad-prep-data-specialist/
├── README.md
├── data/
│   ├── students_raw.csv
│   ├── attendance_raw.csv
│   ├── assessments_raw.csv
│   ├── discipline_raw.csv
│   ├── student_analysis_ready.csv
│   ├── attendance_analysis_ready.csv
│   ├── assessment_analysis_ready.csv
│   ├── discipline_analysis_ready.csv
│   ├── data_quality_log.csv
│   └── data_dictionary.csv
├── workbook/
│   └── Quad_Prep_Data_Specialist_Portfolio.xlsx
├── assets/
│   └── dashboard_preview.png
├── docs/
│   └── project_methodology.md
└── scripts/
    └── README.md
```

## Excel Deliverable

Open `workbook/Quad_Prep_Data_Specialist_Portfolio.xlsx` and start on **Portfolio Dashboard**. Supporting analysis and documentation sheets are included in the workbook.

## Tools

- Excel / advanced formulas
- PivotTables and dashboard design
- Power BI familiarity
- Data quality auditing and documentation
- SQL concepts applicable to relational student data

## Important Analytical Principle

A clean-looking number is not automatically a trustworthy number. The project prioritizes traceability, validation, and defensible decisions over forcing every record into the analysis.

## Author

Tarini — Data Analyst
