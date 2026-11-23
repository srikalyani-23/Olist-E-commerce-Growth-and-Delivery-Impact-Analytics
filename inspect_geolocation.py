
import pandas as pd

# Load geolocation dataset
geolocation = pd.read_csv("data/raw/olist_geolocation_dataset.csv")

# First 5 records
print(geolocation.head())

# Dataset information
print(geolocation.info())

# Statistical summary
print(geolocation.describe(include="all"))

# Missing values
print("\nMissing Values:")
print(geolocation.isnull().sum())

# Missing percentage
print("\nMissing Percentage:")
print((geolocation.isnull().sum() / len(geolocation)) * 100)

print("Shape:", geolocation.shape)

print("\nColumns:")
print(geolocation.columns.tolist())

print("\nData Types:")
print(geolocation.dtypes)

print("\nUnique ZIP Code Prefixes:")
print(geolocation["geolocation_zip_code_prefix"].nunique())

print("\nDuplicate ZIP Code Prefix Rows:")
print(
    geolocation["geolocation_zip_code_prefix"].duplicated().sum()
)

# 1. Check completely duplicate rows
print("\nCompletely Duplicate Rows:")
print(geolocation.duplicated().sum())

# 2. Check unique ZIP + coordinate combinations
print("\nUnique ZIP + Coordinates:")
print(
    geolocation[
        [
            "geolocation_zip_code_prefix",
            "geolocation_lat",
            "geolocation_lng"
        ]
    ].drop_duplicates().shape[0]
)

# 3. Inspect one frequently occurring ZIP prefix
sample_zip = (
    geolocation["geolocation_zip_code_prefix"]
    .value_counts()
    .index[0]
)

print("\nSample ZIP Prefix:", sample_zip)

print(
    geolocation[
        geolocation["geolocation_zip_code_prefix"] == sample_zip
    ].head(10)
)

sample = geolocation[
    geolocation["geolocation_zip_code_prefix"] == 24220
]

print("Total records:", len(sample))

print(
    "\nUnique coordinates:",
    sample[
        ["geolocation_lat", "geolocation_lng"]
    ].drop_duplicates().shape[0]
)

print("\nDistinct coordinate samples:")
print(
    sample[
        [
            "geolocation_zip_code_prefix",
            "geolocation_lat",
            "geolocation_lng",
            "geolocation_city",
            "geolocation_state"
        ]
    ].drop_duplicates().head(10)
)
