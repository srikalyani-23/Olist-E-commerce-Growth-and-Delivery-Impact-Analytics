import pandas as pd 

orders =pd.read_csv("data/raw/olist_orders_dataset.csv")
print(orders.head())
print(orders.info())
print(orders.describe(include="all"))
print(orders.columns.tolist())
print("\nMissing Values:")
print(orders.isnull().sum())
print("\nMissing Percentage:")
print((orders.isnull().sum() / len(orders)) * 100)

# Check distribution of order statuses
print("\nOrder Status Distribution:")
print(orders["order_status"].value_counts())

# Compare missing delivery dates with order status
print("\nMissing Delivery Dates by Order Status:")

print(
    orders.groupby("order_status")[
        "order_delivered_customer_date"
    ].apply(lambda x: x.isnull().sum())
)
