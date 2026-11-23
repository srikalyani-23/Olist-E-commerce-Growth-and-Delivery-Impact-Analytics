
import pandas as pd

reviews = pd.read_csv("data/raw/olist_order_reviews_dataset.csv")

# 1. Find all records with repeated review IDs
duplicate_reviews = reviews[
    reviews["review_id"].duplicated(keep=False)
]

print("Total records with repeated review IDs:",
      len(duplicate_reviews))

# 2. Display sample duplicate records
print("\nDuplicate Review Records:")
print(
    duplicate_reviews.sort_values("review_id").head(20)
)

# 3. Count how many times each review ID occurs
print("\nReview ID Frequency:")
print(
    reviews["review_id"]
    .value_counts()
    .head(10)
)

# 4. Check duplicate review_id and order_id combinations
print("\nDuplicate Review-Order Combinations:")
print(
    reviews.duplicated(
        subset=["review_id", "order_id"]
    ).sum()
)

# 5. Check completely duplicated rows
print("\nCompletely Duplicate Rows:")
print(reviews.duplicated().sum())

# 6. Check duplicate order IDs
print("\nDuplicate Order IDs:")
print(reviews["order_id"].duplicated().sum())

# 7. Check whether review_id + order_id is unique
print("\nUnique Review-Order Combinations:")
print(
    reviews[["review_id", "order_id"]]
    .drop_duplicates()
    .shape[0]
)

print("\nTotal Review Records:")
print(reviews.shape[0])
