
import os
import pandas as pd

# Step 1: Processed data folder
folder_path = "data/processed"

# Step 2: Get all CSV files
csv_files = [
    file for file in os.listdir(folder_path)
    if file.endswith(".csv")
]

print("=" * 60)
print("PROCESSED DATASET QUALITY CHECK")
print("=" * 60)

print(f"\nTotal CSV files found: {len(csv_files)}")

# Step 3: Store quality results
quality_results = []

# Step 4: Inspect each CSV
for file in sorted(csv_files):

    file_path = os.path.join(folder_path, file)
    df = pd.read_csv(file_path, low_memory=False)

    rows, columns = df.shape

    missing_cells = df.isnull().sum().sum()
    duplicate_rows = df.duplicated().sum()

    print("\n" + "-" * 60)
    print(f"File: {file}")
    print("-" * 60)

    print("Rows:", rows)
    print("Columns:", columns)
    print("Missing cells:", missing_cells)
    print("Duplicate rows:", duplicate_rows)

    print("\nColumn Names:")
    print(df.columns.tolist())

    print("\nData Types:")
    print(df.dtypes.to_string())

    print("\nMissing Values by Column:")
    missing_by_column = df.isnull().sum()
    print(missing_by_column[missing_by_column > 0].to_string()
          if missing_cells > 0 else "No missing values")

    # Step 5: Save summary
    quality_results.append({
        "file_name": file,
        "rows": rows,
        "columns": columns,
        "missing_cells": missing_cells,
        "duplicate_rows": duplicate_rows
    })


# Step 6: Create final quality report
quality_report = pd.DataFrame(quality_results)

print("\n" + "=" * 60)
print("FINAL QUALITY SUMMARY")
print("=" * 60)

print(quality_report.to_string(index=False))

# Step 7: Export quality report
os.makedirs("reports", exist_ok=True)

report_path = "reports/processed_quality_report.csv"
quality_report.to_csv(report_path, index=False)

print("\nQuality report saved successfully!")
print("Location:", report_path)
