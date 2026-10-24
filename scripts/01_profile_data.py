"""
Script 01: Profile the four source extracts.

Purpose
    Load each file in data/source and describe its shape before any cleaning
    happens. The output is a summary table that the data quality report and
    the data dictionary are built from.

What it does
    1. Reads students.csv, attendance.csv, assessments.csv, discipline.csv.
    2. For every column records the data type, the count of missing values,
       and the count of distinct values.
    3. Checks each table for fully duplicated rows and for repeated
       Student_ID values.
    4. Prints a short summary and saves the detail to
       outputs/data_profile_summary.csv.

Run order
    Run this script first. Run 02_clean_and_validate.py second.
"""

from pathlib import Path

import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
SOURCE_DIR = BASE_DIR / "data" / "source"
OUTPUT_DIR = BASE_DIR / "outputs"
OUTPUT_DIR.mkdir(exist_ok=True)

SOURCE_FILES = {
    "students": "students.csv",
    "attendance": "attendance.csv",
    "assessments": "assessments.csv",
    "discipline": "discipline.csv",
}


def profile_table(name, frame):
    """Return one summary row per column plus table level checks."""
    rows = []
    for column in frame.columns:
        rows.append(
            {
                "dataset": name,
                "column": column,
                "data_type": str(frame[column].dtype),
                "missing_values": int(frame[column].isna().sum()),
                "distinct_values": int(frame[column].nunique()),
                "example_values": "; ".join(
                    str(value) for value in frame[column].dropna().unique()[:5]
                ),
            }
        )
    duplicated_rows = int(frame.duplicated().sum())
    repeated_ids = 0
    if "Student_ID" in frame.columns:
        repeated_ids = int(frame["Student_ID"].duplicated().sum())
    print(f"{name}: {len(frame)} rows, {len(frame.columns)} columns")
    print(f"  fully duplicated rows: {duplicated_rows}")
    print(f"  repeated Student_ID values: {repeated_ids}")
    return rows


def main():
    all_rows = []
    for name, filename in SOURCE_FILES.items():
        frame = pd.read_csv(SOURCE_DIR / filename)
        all_rows.extend(profile_table(name, frame))
    summary = pd.DataFrame(all_rows)
    summary.to_csv(OUTPUT_DIR / "data_profile_summary.csv", index=False)
    print("Saved outputs/data_profile_summary.csv")


if __name__ == "__main__":
    main()
