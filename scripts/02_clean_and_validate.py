"""
Script 02: Clean the source extracts, build the analysis tables, validate.

Purpose
    Turn the four source extracts into a small set of analysis tables that
    all describe the same group of students, and write a log of every
    change so another analyst can follow each decision.

Analysis population (the key decision in this project)
    A student is in the analysis population when the student appears in
    the student table with Enrollment_Status equal to Active.
    The student table holds 117 students. Seven are Withdrawn, so the
    analysis population is 110 students.
    Attendance, assessment, and discipline rows are kept only when their
    Student_ID belongs to the analysis population. Every removed row is
    listed in the cleaning log with its reason.
    The alternative would be to include Withdrawn students. That choice
    was not taken because their attendance and assessment records cover
    a part year and would sit inside averages as if the students had
    stayed for the full period. The counts change slightly under the
    alternative; the direction of the findings does not.

Cleaning rules
    1. Program values are standardized with a fixed mapping, so the one
       lowercase value "MTSS tier 2" becomes "MTSS Tier 2".
    2. Benchmark values are standardized the same way, so "met" becomes
       "Met".
    3. Name columns are dropped from every processed output. The analysis
       never needs a student name, and the portfolio copy should not
       carry one.
    4. Attendance_Band is derived from Attendance_Rate with the project
       bands: below 85 is At Risk, 85 to 89.9 is Needs Monitoring,
       90 to 94.9 is On Track, 95 and above is Strong.
    5. Is_Chronic_Absence is Yes when Attendance_Rate is below 90.
       This is a project definition written for this analysis. It is not
       an official school or district definition.
    6. Nothing is deleted quietly. Source files stay unchanged, and each
       change is written to outputs/cleaning_log.csv.

Outputs
    data/processed/dim_student.csv
    data/processed/fact_attendance.csv
    data/processed/fact_assessment.csv
    data/processed/fact_discipline.csv
    data/processed/fact_student_summary.csv (one row per student)
    outputs/cleaning_log.csv
    outputs/validation_results.csv

Run order
    Run 01_profile_data.py first, then this script.
"""

from pathlib import Path

import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
SOURCE_DIR = BASE_DIR / "data" / "source"
PROCESSED_DIR = BASE_DIR / "data" / "processed"
OUTPUT_DIR = BASE_DIR / "outputs"
PROCESSED_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)

PROGRAM_MAP = {
    "core": "Core",
    "mtss tier 1": "MTSS Tier 1",
    "mtss tier 2": "MTSS Tier 2",
    "mtss tier 3": "MTSS Tier 3",
}
BENCHMARK_MAP = {"below": "Below", "met": "Met"}

cleaning_log = []


def log_change(step, table, student_id, field, original, new, rule, reason):
    cleaning_log.append(
        {
            "step": step,
            "table": table,
            "student_id": student_id,
            "field": field,
            "original_value": original,
            "new_value": new,
            "rule": rule,
            "reason": reason,
        }
    )


def attendance_band(rate):
    """Map an attendance rate to the project attendance band."""
    if pd.isna(rate):
        return None
    if rate < 85:
        return "At Risk"
    if rate < 90:
        return "Needs Monitoring"
    if rate < 95:
        return "On Track"
    return "Strong"


def keep_population_rows(frame, table_name, all_student_ids, population_ids):
    """Keep only rows for students in the analysis population, and log
    every row that is removed with the reason it was removed."""
    kept = []
    for _, row in frame.iterrows():
        student_id = row["Student_ID"]
        if student_id in population_ids:
            kept.append(row)
        elif student_id not in all_student_ids:
            log_change(
                "exclude rows", table_name, student_id, "row", "present",
                "removed", "row level exclusion",
                "Student_ID does not appear in the student table, so the "
                "record cannot be linked to a known student.",
            )
        else:
            log_change(
                "exclude rows", table_name, student_id, "row", "present",
                "removed", "row level exclusion",
                "Student is Withdrawn and sits outside the analysis "
                "population of Active students.",
            )
    return pd.DataFrame(kept).reset_index(drop=True)


def main():
    students = pd.read_csv(SOURCE_DIR / "students.csv")
    attendance = pd.read_csv(SOURCE_DIR / "attendance.csv")
    assessments = pd.read_csv(SOURCE_DIR / "assessments.csv")
    discipline = pd.read_csv(SOURCE_DIR / "discipline.csv")

    # Step 1: standardize the Program casing with a fixed mapping.
    for index, row in students.iterrows():
        standard = PROGRAM_MAP.get(str(row["Program"]).strip().lower())
        if standard is not None and standard != row["Program"]:
            log_change(
                "standardize values", "students", row["Student_ID"],
                "Program", row["Program"], standard, "fixed casing mapping",
                "The same program was written with two different casings, "
                "which splits one group into two in any summary.",
            )
            students.at[index, "Program"] = standard

    # Step 2: standardize the Benchmark casing the same way.
    for index, row in assessments.iterrows():
        standard = BENCHMARK_MAP.get(str(row["Benchmark"]).strip().lower())
        if standard is not None and standard != row["Benchmark"]:
            log_change(
                "standardize values", "assessments", row["Student_ID"],
                "Benchmark", row["Benchmark"], standard,
                "fixed casing mapping",
                "The same benchmark level was written with two different "
                "casings, which splits one group into two in any summary.",
            )
            assessments.at[index, "Benchmark"] = standard

    # Step 3: define the analysis population and build the student table.
    students["Enrollment_Date"] = pd.to_datetime(
        students["Enrollment_Date"]
    ).dt.date
    all_student_ids = set(students["Student_ID"])
    population = students[students["Enrollment_Status"] == "Active"].copy()
    population_ids = set(population["Student_ID"])
    withdrawn_count = int((students["Enrollment_Status"] == "Withdrawn").sum())
    log_change(
        "define population", "students", "all rows", "Enrollment_Status",
        f"{len(students)} students in source",
        f"{len(population)} students in analysis population",
        "population filter",
        f"{withdrawn_count} Withdrawn students are excluded from the "
        "analysis population. Their records cover a part year.",
    )
    log_change(
        "drop columns", "students", "all rows", "Last_Name and Full Name",
        "present in source", "removed from processed outputs",
        "privacy and relevance",
        "The analysis never uses a student name, so name columns are not "
        "carried into any processed table.",
    )
    dim_student = population[
        ["Student_ID", "Enrollment_Status", "Program", "Enrollment_Date"]
    ].reset_index(drop=True)
    dim_student.to_csv(PROCESSED_DIR / "dim_student.csv", index=False)

    # Step 4: keep fact rows for the population only, and log removals.
    fact_attendance = keep_population_rows(
        attendance, "attendance", all_student_ids, population_ids
    )
    fact_assessment = keep_population_rows(
        assessments, "assessments", all_student_ids, population_ids
    )
    fact_discipline = keep_population_rows(
        discipline, "discipline", all_student_ids, population_ids
    )

    # Step 5: derive the attendance band and the chronic absence flag.
    fact_attendance["Attendance_Band"] = fact_attendance["Attendance_Rate"].apply(
        attendance_band
    )
    fact_attendance["Is_Chronic_Absence"] = fact_attendance["Attendance_Rate"].apply(
        lambda rate: "Yes" if rate < 90 else "No"
    )
    log_change(
        "derive fields", "attendance", "all rows",
        "Attendance_Band and Is_Chronic_Absence", "not present in source",
        "derived from Attendance_Rate", "documented project definitions",
        "Bands make attendance groups easier to compare. The chronic "
        "absence flag uses the project definition of a rate below 90 "
        "percent.",
    )
    fact_assessment["Assessment_Date"] = pd.to_datetime(
        fact_assessment["Assessment_Date"]
    ).dt.date
    fact_attendance.to_csv(PROCESSED_DIR / "fact_attendance.csv", index=False)
    fact_assessment.to_csv(PROCESSED_DIR / "fact_assessment.csv", index=False)
    fact_discipline.to_csv(PROCESSED_DIR / "fact_discipline.csv", index=False)

    # Step 6: build one combined row per student for Excel and quick checks.
    grade = (
        pd.concat(
            [
                fact_attendance[["Student_ID", "Grade"]],
                fact_assessment[["Student_ID", "Grade"]],
                fact_discipline[["Student_ID", "Grade"]],
            ]
        )
        .drop_duplicates("Student_ID")
        .rename(columns={"Grade": "Grade"})
    )
    summary = dim_student.merge(grade, on="Student_ID", how="left")
    summary = summary.merge(
        fact_attendance[
            [
                "Student_ID", "Days_Enrolled", "Days_Present", "Days_Absent",
                "Attendance_Rate", "Attendance_Band", "Is_Chronic_Absence",
            ]
        ],
        on="Student_ID", how="left",
    )
    summary = summary.merge(
        fact_assessment[
            ["Student_ID", "Assessment", "Assessment_Date", "Score", "Benchmark"]
        ],
        on="Student_ID", how="left",
    )
    summary = summary.merge(
        fact_discipline[["Student_ID", "Incidents", "Major_Incidents"]],
        on="Student_ID", how="left",
    )
    summary = summary[
        [
            "Student_ID", "Grade", "Program", "Enrollment_Date",
            "Days_Enrolled", "Days_Present", "Days_Absent", "Attendance_Rate",
            "Attendance_Band", "Is_Chronic_Absence", "Assessment",
            "Assessment_Date", "Score", "Benchmark", "Incidents",
            "Major_Incidents",
        ]
    ].sort_values("Student_ID").reset_index(drop=True)
    summary.to_csv(PROCESSED_DIR / "fact_student_summary.csv", index=False)

    # Step 7: validation checks. Each check records what was expected and
    # what was found, so a failure is visible instead of silent.
    checks = []

    def record_check(name, expected, actual):
        checks.append(
            {
                "check": name,
                "expected": expected,
                "actual": actual,
                "result": "Pass" if str(expected) == str(actual) else "Fail",
            }
        )

    record_check("Students in source table", 117, len(students))
    record_check("Students in analysis population", 110, len(dim_student))
    record_check("Attendance rows after cleaning", 108, len(fact_attendance))
    record_check("Assessment rows after cleaning", 107, len(fact_assessment))
    record_check("Discipline rows after cleaning", 109, len(fact_discipline))
    record_check("Summary rows, one per student", 110, len(summary))

    orphan_total = 0
    for frame in (fact_attendance, fact_assessment, fact_discipline):
        orphan_total += int((~frame["Student_ID"].isin(population_ids)).sum())
    record_check("Fact rows with no matching student after cleaning", 0, orphan_total)

    arithmetic_breaks = int(
        (
            fact_attendance["Days_Present"] + fact_attendance["Days_Absent"]
            != fact_attendance["Days_Enrolled"]
        ).sum()
    )
    record_check(
        "Attendance rows where present plus absent differs from enrolled",
        0, arithmetic_breaks,
    )
    present_over = int(
        (fact_attendance["Days_Present"] > fact_attendance["Days_Enrolled"]).sum()
    )
    record_check("Attendance rows where present exceeds enrolled", 0, present_over)

    rule_breaks = int(
        (
            (fact_assessment["Score"] < 70)
            != (fact_assessment["Benchmark"] == "Below")
        ).sum()
    )
    record_check(
        "Assessment rows breaking the rule Below means score under 70",
        0, rule_breaks,
    )
    record_check(
        "Program values outside the standard list", 0,
        int((~dim_student["Program"].isin(PROGRAM_MAP.values())).sum()),
    )
    record_check(
        "Benchmark values outside Met and Below", 0,
        int((~fact_assessment["Benchmark"].isin(["Met", "Below"])).sum()),
    )
    record_check(
        "Duplicated Student_ID in summary table", 0,
        int(summary["Student_ID"].duplicated().sum()),
    )
    record_check(
        "Attendance rates outside 0 to 100", 0,
        int((~fact_attendance["Attendance_Rate"].between(0, 100)).sum()),
    )
    record_check(
        "Students in summary with no grade from any table", 0,
        int(summary["Grade"].isna().sum()),
    )

    validation = pd.DataFrame(checks)
    validation.to_csv(OUTPUT_DIR / "validation_results.csv", index=False)
    pd.DataFrame(cleaning_log).to_csv(OUTPUT_DIR / "cleaning_log.csv", index=False)

    print(validation.to_string(index=False))
    print(f"Cleaning log entries: {len(cleaning_log)}")
    print("Wrote processed tables to data/processed")
    print("Wrote outputs/cleaning_log.csv and outputs/validation_results.csv")


if __name__ == "__main__":
    main()
