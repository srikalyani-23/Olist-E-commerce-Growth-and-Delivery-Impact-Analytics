
import pandas as pd

# Load sellers dataset
sellers = pd.read_csv("data/raw/olist_sellers_dataset.csv")

# First 5 records
print(sellers.head())

# Dataset information
print(sellers.info())

# Statistical summary
print(sellers.describe(include="all"))

# Missing values
print("\nMissing Values:")
print(sellers.isnull().sum())

# Check unique sellers
print("Unique sellers:",
      sellers["seller_id"].nunique())

# Check duplicate seller IDs
print("Duplicate seller IDs:",
      sellers["seller_id"].duplicated().sum())

# Check unique seller states
print("Unique seller states:",
      sellers["seller_state"].nunique())

# Top 10 seller states
print("\nTop seller states:")
print(sellers["seller_state"].value_counts().head(10))
