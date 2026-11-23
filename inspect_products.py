
import pandas as pd

# Load products dataset
products = pd.read_csv("data/raw/olist_products_dataset.csv")

# First 5 records
print(products.head())

# Dataset information
print(products.info())

# Statistical summary
print(products.describe(include="all"))

# Missing values
print("\nMissing Values:")
print(products.isnull().sum())

# Missing percentage
print("\nMissing Percentage:")
print((products.isnull().sum() / len(products)) * 100)


# Check whether 610 missing values belong to same products
missing_category = products[
    products["product_category_name"].isnull()
]

print("Products missing category:", len(missing_category))

print("\nMissing category + name + description + photos:")
print(
    missing_category[
        [
            "product_category_name",
            "product_name_length",
            "product_description_length",
            "product_photos_qty"
        ]
    ].isnull().all(axis=1).sum()
)

# Check records missing physical attributes
missing_dimensions = products[
    products["product_weight_g"].isnull()
]

print("\nProducts missing physical attributes:")
print(missing_dimensions)
