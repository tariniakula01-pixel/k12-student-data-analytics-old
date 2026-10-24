# Methodology and Limitations

## About the data

The dataset is simulated practice data built for this portfolio project. It describes one school, grades 5 to 8, in the 2025 to 2026 school year. It is not data about any real school, and the students in it are not real students. Four related extracts make up the source data: students, attendance, assessments, and discipline. Student_ID is the common identifier. Conceptually it is the primary identifier in the student table and a linking field in the other three.

The source extracts are the earliest layer of this project that exists. No earlier raw files were available, so the pipeline starts from these extracts and treats them as the source of record. They sit unchanged in `data/source`.

## Workflow

1. Profile. `scripts/01_profile_data.py` describes each source file: row counts, columns, data types, missing values, distinct values, duplicated rows, and repeated identifiers. The output sits in `outputs/data_profile_summary.csv`.
2. Clean and validate. `scripts/02_clean_and_validate.py` standardizes category casing, defines the analysis population, filters every fact table to that population, derives the attendance band and the chronic absence flag, drops name columns from the outputs, and writes the processed tables to `data/processed`. Every change is listed in `outputs/cleaning_log.csv`, and 15 validation checks are written to `outputs/validation_results.csv`.
3. Analyze in SQL. The files in `sql` run against the processed tables in DuckDB. Each one answers a named business question. `sql/run_all.py` runs them in order and saves the results to `outputs/sql_results`.
4. Analyze in Python. `notebooks/01_exploratory_analysis.ipynb` repeats the headline analysis with pandas and matplotlib, adds the distributions, and saves the charts used across the project to `assets/charts`.
5. Report. The Excel workbook is built by `scripts/03_build_workbook.py`. The Power BI model tables are copied into `powerbi/model` by `scripts/05_build_powerbi_model.py`, and the report itself is defined in the PBIP project in `powerbi/powerbi_project`.
6. Reconcile. `scripts/04_reconcile_kpis.py` compares the five headline KPIs between the pandas route and the DuckDB route. They agree exactly, and the comparison sits in `outputs/kpi_reconciliation.csv`.

## The population decision

The analysis population is the set of students listed as Active in the student table: 110 of the 117 students. The seven Withdrawn students are excluded.

The reasoning: a Withdrawn student record covers a part year. Their attendance covers fewer enrolled days, and any assessment they took happened before they left. Mixing those records into the averages would treat part year students as if they had been present for the full period.

The alternative was to include all 117 students and let each average rest on whatever rows exist. That choice is defensible for a simple headcount report. It was not taken here because the project aim is a consistent population that every tool describes in the same way.

The effect of the decision is documented rather than hidden. `docs/data_quality_report.md` shows the headline figures under the rebuilt population next to the figures the original README published, and the differences are small: the average attendance rate moves from 91.8 to 91.84 under a stricter base, the average score from 78.1 to 78.48, and the count of students below 85 percent attendance from 22 to 21.

## Cleaning rules

The cleaning rules follow the principle set in the original version of this project: correct a value only when the data or a documented rule supports the correction, and flag rather than guess otherwise.

1. Category casing is standardized with a fixed mapping for Program and Benchmark. These are safe corrections because the intended values are unambiguous.
2. Rows outside the population are excluded, never edited into the population. Each exclusion carries its reason in the cleaning log.
3. Missing fact rows stay missing. Two students have no attendance row, three have no assessment row, and one has no discipline row. No values are filled in for them, because an invented attendance rate or score would flow into every average downstream.
4. No outliers were removed. The lowest attendance rate of 75 percent and the lowest score of 43 are unusual values, not impossible ones, and each rests on a full record that passes the arithmetic checks. They stay in the data and are visible in the distributions.
5. Name columns are dropped from every processed output. The analysis never uses a name. The source layer keeps the names because the source layer is preserved as received.

## Definitions written by this project

Two definitions in the analysis are project choices, and both are labeled wherever they appear. The attendance bands (below 85 At Risk, 85 to 89.9 Needs Monitoring, 90 to 94.9 On Track, 95 and above Strong) are analysis categories kept from the original version of the project. The chronic absence flag marks an attendance rate below 90 percent. Neither matches an official school or district threshold, and neither should be quoted as one.

## Limitations

1. Attendance is a period summary. The data holds days enrolled, present, and absent per student for one period. It holds no daily records, so absence patterns inside the year, such as absences clustering on particular days or growing over time, cannot be examined.
2. One assessment per student. Each student took one assessment in one subject. Subject comparisons compare different groups of students, growth over time cannot be measured, and the month view describes the testing window rather than progress.
3. No causal reading is supported. The data records no teaching, prior achievement, or home circumstances. The near zero correlation between attendance and score in this data is an observation about this dataset. It does not show that attendance has no effect on learning, and it does not show the opposite either.
4. Small groups. MTSS Tier 3 holds nine students and the smallest grade by assessment count holds 22. Averages on groups this size move when a single student changes, so group results are always reported with their counts.
5. One school, one year, simulated data. Nothing here generalizes to other schools or other years, and nothing here describes a real school at all.
6. Grade comes from the fact tables. The student table carries no grade, so grade is taken from the attendance, assessment, and discipline tables. Those tables agree with each other on grade for every shared student, verified in the audit, so the risk is low, but the source of the field is worth knowing.

## Privacy and handling

The processed tables, the model tables, and the workbook carry no student names. Student identifiers are project codes. Anyone adapting this workflow to real data should apply the same rule with more force: real student records belong in access controlled systems, never in a public repository, and extracts should carry the minimum fields the analysis needs.
