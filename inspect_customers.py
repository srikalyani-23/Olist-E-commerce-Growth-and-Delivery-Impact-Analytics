
import pandas as pd

# Load customers dataset
customers = pd.read_csv("data/raw/olist_customers_dataset.csv")

# First 5 records
print(customers.head())

# Dataset information
print(customers.info())

# Statistical summary
print(customers.describe(include="all"))

# Missing values
print("\nMissing Values:")
print(customers.isnull().sum())

# Check unique customer records
print("Unique customer_id:",
      customers["customer_id"].nunique())

# Check actual unique customers
print("Unique customer_unique_id:",
      customers["customer_unique_id"].nunique())

# Check duplicate customer IDs
print("Duplicate customer_id:",
      customers["customer_id"].duplicated().sum())

# Check unique states
print("Unique states:",
      customers["customer_state"].nunique())

# Top 10 customer states
print("\nTop 10 states:")
print(customers["customer_state"].value_counts().head(10))
