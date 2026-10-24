# Power BI Deliverables

This folder holds the Power BI layer of the project.

## What is here

1. `model` holds the five model tables as CSV files: `dim_student`, `dim_date`, `fact_attendance`, `fact_assessment`, and `fact_discipline`. The script `scripts/05_build_powerbi_model.py` builds this folder from the processed tables.
2. `dax_measures.md` is the measure catalog. Every measure in the model is listed with a plain English definition, its DAX formula, and notes on its denominator and population.
3. `powerbi_project` holds a Power BI project in the PBIP text format: a semantic model written in TMDL with the same tables, relationships, and measures, and a report definition in PBIR format with four pages named Executive Summary, Student Performance, Attendance, and Equity and Program.
4. `dashboard_preview.html` is a preview of the report design that anyone can open in a browser. It uses the same computed values and chart images as the analysis, and it is labeled as a preview inside the file.

## Validation status, stated plainly

The PBIP project was authored as text on a Linux machine. It has not been opened in Power BI Desktop, and it has not been validated by Power BI Desktop or the Power BI service. Every JSON file in the project parses as valid JSON, and the TMDL files follow the published TMDL layout, but that is not the same as a tested report. Treat the project as a complete and careful first version that needs the short manual pass below before it is shared as a working report.

The numbers the report will show have been validated another way. The same KPIs were calculated in pandas and in DuckDB SQL and they agree exactly. That reconciliation is saved in `outputs/kpi_reconciliation.csv`.

## Manual steps to open and validate the project

1. Install Power BI Desktop on a Windows machine and sign in.
2. Open the file `K12StudentAnalytics.pbip` inside the `powerbi_project` folder.
3. If Power BI asks about the data source paths, open the Power Query editor and point each table source step at the matching CSV file inside the `model` folder of this project. The table names and file names match one to one.
4. Mark `dim_date` as the model date table using its `Date` column. The month comparison measures in the catalog depend on this step.
5. Check the relationships view. Each fact table should connect to `dim_student` on `Student_ID`, and `fact_assessment` should connect to `dim_date` on the assessment date.
6. Refresh the model and read the four report pages. Compare the card values on the Executive Summary page with `outputs/kpi_reconciliation.csv`. They should read 110 total students, an average attendance rate of 91.84, an average score of 78.48, and 75.7 percent of assessed students recorded as Met.
7. If a page or visual reports an error, note the page and visual name and adjust the visual fields in Desktop, then save the project from Desktop so the saved definition carries the Desktop corrections.

## Design notes

The report uses a restrained palette of deep navy, gray, and one gold accent. Each page answers one question set. The Executive Summary page leads with four KPI cards and the comparisons a school leader asks for first. The Attendance page carries the project definition of chronic absence in its reading notes, and the Equity and Program page pairs every program result with its student count so small groups are not read as firmly as large ones.
