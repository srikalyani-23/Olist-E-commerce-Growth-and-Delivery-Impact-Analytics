
import pandas as pd

# Load datasets
orders = pd.read_csv("data/raw/olist_orders_dataset.csv")
items = pd.read_csv("data/raw/olist_order_items_dataset.csv")
customers = pd.read_csv("data/raw/olist_customers_dataset.csv")
sellers = pd.read_csv("data/raw/olist_sellers_dataset.csv")
products = pd.read_csv("data/raw/olist_products_dataset.csv")
payments = pd.read_csv("data/raw/olist_order_payments_dataset.csv")
reviews = pd.read_csv("data/raw/olist_order_reviews_dataset.csv")
translation = pd.read_csv(
    "data/raw/product_category_name_translation.csv"
)

print("All datasets loaded successfully!")

print("\n--- PRIMARY KEY VALIDATION ---")

# Orders
print("Orders duplicate IDs:",
      orders["order_id"].duplicated().sum())

# Customers
print("Customers duplicate IDs:",
      customers["customer_id"].duplicated().sum())

# Sellers
print("Sellers duplicate IDs:",
      sellers["seller_id"].duplicated().sum())

# Products
print("Products duplicate IDs:",
      products["product_id"].duplicated().sum())

# Order Items: composite key
print("Order Items duplicate combinations:",
      items.duplicated(
          subset=["order_id", "order_item_id"]
      ).sum())

# Payments: composite key candidate
print("Payments duplicate combinations:",
      payments.duplicated(
          subset=["order_id", "payment_sequential"]
      ).sum())

# Reviews
print("Reviews duplicate IDs:",
      reviews["review_id"].duplicated().sum())

# Category Translation
print("Translation duplicate categories:",
      translation["product_category_name"].duplicated().sum())

print("\n--- FOREIGN KEY VALIDATION ---")

# Order Items -> Orders
print("Items with missing Orders:",
      (~items["order_id"].isin(orders["order_id"])).sum())

# Orders -> Customers
print("Orders with missing Customers:",
      (~orders["customer_id"].isin(customers["customer_id"])).sum())

# Order Items -> Products
print("Items with missing Products:",
      (~items["product_id"].isin(products["product_id"])).sum())

# Order Items -> Sellers
print("Items with missing Sellers:",
      (~items["seller_id"].isin(sellers["seller_id"])).sum())

# Payments -> Orders
print("Payments with missing Orders:",
      (~payments["order_id"].isin(orders["order_id"])).sum())

# Reviews -> Orders
print("Reviews with missing Orders:",
      (~reviews["order_id"].isin(orders["order_id"])).sum())
