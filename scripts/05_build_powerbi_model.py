"""
Script 05: Build the Power BI model tables.

Purpose
    Copy the processed tables into powerbi/model so the Power BI project
    loads from its own folder, and build a date table that covers the
    enrollment and assessment dates in the data.

What it does
    1. Copies dim_student, fact_attendance, fact_assessment, and
       fact_discipline from data/processed to powerbi/model.
    2. Builds dim_date with one row per day from 1 September 2025 to
       30 April 2026. That range covers the first enrollment date and
       the last assessment date in the data.

Run order
    Run after 02_clean_and_validate.py.
"""

from pathlib import Path

import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
PROCESSED_DIR = BASE_DIR / "data" / "processed"
MODEL_DIR = BASE_DIR / "powerbi" / "model"
MODEL_DIR.mkdir(parents=True, exist_ok=True)

TABLES = ["dim_student", "fact_attendance", "fact_assessment", "fact_discipline"]


def main():
    for table in TABLES:
        frame = pd.read_csv(PROCESSED_DIR / f"{table}.csv")
        frame.to_csv(MODEL_DIR / f"{table}.csv", index=False)
        print(f"{table}: {len(frame)} rows copied to powerbi/model")

    dates = pd.date_range("2025-09-01", "2026-04-30", freq="D")
    dim_date = pd.DataFrame(
        {
            "Date": dates.date,
            "Year": dates.year,
            "Month": dates.month,
            "MonthName": dates.strftime("%B"),
            "YearMonth": dates.strftime("%Y-%m"),
            "MonthLabel": dates.strftime("%b %Y"),
        }
    )
    dim_date.to_csv(MODEL_DIR / "dim_date.csv", index=False)
    print(f"dim_date: {len(dim_date)} rows from 2025-09-01 to 2026-04-30")


if __name__ == "__main__":
    main()
