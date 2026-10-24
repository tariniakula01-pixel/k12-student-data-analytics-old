"""
Run every SQL file in this folder with DuckDB and save the results.

Each SQL file creates the views it needs and ends with one query. This
runner opens each file in number order, runs the view statements, runs
the final query, and writes the result to outputs/sql_results with the
same file name and a csv ending.

Run from the repository root so the data paths inside the SQL files
resolve correctly:

    python sql/run_all.py
"""

from pathlib import Path

import duckdb

BASE_DIR = Path(__file__).resolve().parent.parent
SQL_DIR = BASE_DIR / "sql"
RESULTS_DIR = BASE_DIR / "outputs" / "sql_results"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)


def split_statements(sql_text):
    """Split a SQL file into statements on semicolons. The files in this
    project keep semicolons out of comments and text values, so a plain
    split is safe here."""
    parts = [part.strip() for part in sql_text.split(";")]
    return [part for part in parts if part]


def main():
    connection = duckdb.connect()
    sql_files = sorted(SQL_DIR.glob("*.sql"))
    for sql_file in sql_files:
        statements = split_statements(sql_file.read_text())
        result = None
        for statement in statements[:-1]:
            connection.execute(statement)
        result = connection.execute(statements[-1]).fetchdf()
        output_path = RESULTS_DIR / (sql_file.stem + ".csv")
        result.to_csv(output_path, index=False)
        print(f"{sql_file.name}: wrote {len(result)} rows to {output_path}")
        print(result.to_string(index=False))
        print()
    connection.close()


if __name__ == "__main__":
    main()
