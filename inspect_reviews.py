
import pandas as pd

# Load reviews dataset
reviews = pd.read_csv("data/raw/olist_order_reviews_dataset.csv")

# First 5 records
print(reviews.head())

# Dataset information
print(reviews.info())

# Statistical summary
print(reviews.describe(include="all"))

# Missing values
print("\nMissing Values:")
print(reviews.isnull().sum())

# Missing percentage
print("\nMissing Percentage:")
print((reviews.isnull().sum() / len(reviews)) * 100)
