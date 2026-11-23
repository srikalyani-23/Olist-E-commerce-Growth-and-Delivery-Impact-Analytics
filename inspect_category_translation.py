
import pandas as pd

# Load category translation dataset
translation = pd.read_csv(
    "data/raw/product_category_name_translation.csv"
)

# First 5 records
print(translation.head())

# Dataset information
print(translation.info())

# Statistical summary
print(translation.describe(include="all"))

# Missing values
print("\nMissing Values:")
print(translation.isnull().sum())

# Missing percentage
print("\nMissing Percentage:")
print((translation.isnull().sum() / len(translation)) * 100)

# Total unique Portuguese categories
print(
    "\nUnique Portuguese Categories:",
    translation["product_category_name"].nunique()
)

# Total unique English categories
print(
    "Unique English Categories:",
    translation["product_category_name_english"].nunique()
)
