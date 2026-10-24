"""
Script 04: Reconcile the headline KPIs between pandas and DuckDB.

Purpose
    The same five KPIs are calculated twice, once in pandas from the
    processed tables and once in DuckDB by sql/01_kpi_summary.sql. If
    the two routes agree, the numbers quoted in the reports and the
    dashboard rest on more than one implementation.

What it does
    1. Calculates Total Students, Average Attendance Rate, Average
       Score, Percent Met Benchmark, and Chronic Absence Rate in
       pandas, rounded the same way the SQL rounds them.
    2. Reads the DuckDB result from outputs/sql_results/01_kpi_summary.csv.
    3. Writes outputs/kpi_reconciliation.csv with both values and a
       match flag for each KPI.

Run order
    Run after 02_clean_and_validate.py and after sql/run_all.py.
"""

from pathlib import Path

import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
PROCESSED_DIR = BASE_DIR / "data" / "processed"
OUTPUT_DIR = BASE_DIR / "outputs"


def main():
    dim_student = pd.read_csv(PROCESSED_DIR / "dim_student.csv")
    fact_attendance = pd.read_csv(PROCESSED_DIR / "fact_attendance.csv")
    fact_assessment = pd.read_csv(PROCESSED_DIR / "fact_assessment.csv")
    sql_kpis = pd.read_csv(OUTPUT_DIR / "sql_results" / "01_kpi_summary.csv").iloc[0]

    pandas_values = {
        "Total Students": float(len(dim_student)),
        "Average Attendance Rate": round(float(fact_attendance["Attendance_Rate"].mean()), 2),
        "Average Score": round(float(fact_assessment["Score"].mean()), 2),
        "Percent Met Benchmark": round(
            100.0 * float((fact_assessment["Benchmark"] == "Met").mean()), 1
        ),
        "Chronic Absence Rate": round(
            100.0 * float((fact_attendance["Is_Chronic_Absence"] == "Yes").mean()), 1
        ),
    }
    sql_columns = {
        "Total Students": "total_students",
        "Average Attendance Rate": "average_attendance_rate",
        "Average Score": "average_score",
        "Percent Met Benchmark": "percent_met_benchmark",
        "Chronic Absence Rate": "chronic_absence_rate",
    }

    rows = []
    for kpi_name, pandas_value in pandas_values.items():
        duckdb_value = float(sql_kpis[sql_columns[kpi_name]])
        rows.append(
            {
                "kpi": kpi_name,
                "pandas_value": pandas_value,
                "duckdb_value": duckdb_value,
                "match": "Yes" if abs(pandas_value - duckdb_value) < 0.005 else "No",
            }
        )
    reconciliation = pd.DataFrame(rows)
    reconciliation.to_csv(OUTPUT_DIR / "kpi_reconciliation.csv", index=False)
    print(reconciliation.to_string(index=False))
    if (reconciliation["match"] == "Yes").all():
        print("All five KPIs agree between pandas and DuckDB.")
    else:
        print("WARNING: at least one KPI differs between pandas and DuckDB.")


if __name__ == "__main__":
    main()
