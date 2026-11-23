
import pandas as pd

# Load payments dataset
payments = pd.read_csv("data/raw/olist_order_payments_dataset.csv")

# First 5 records
print(payments.head())

# Dataset information
print(payments.info())

# Statistical summary
print(payments.describe(include="all"))

# Missing values
print("\nMissing Values:")
print(payments.isnull().sum())

# Missing percentage
print("\nMissing Percentage:")
print((payments.isnull().sum() / len(payments)) * 100)

# 1. Check duplicate composite keys
print("\nDuplicate Order + Payment Sequence:")
print(
    payments.duplicated(
        subset=["order_id", "payment_sequential"]
    ).sum()
)

# 2. Payment type distribution
print("\nPayment Type Distribution:")
print(payments["payment_type"].value_counts())

# 3. Zero payment records
print("\nZero Payment Records:")
print((payments["payment_value"] == 0).sum())

# 4. Negative payment records
print("\nNegative Payment Records:")
print((payments["payment_value"] < 0).sum())

# 5. Orders having multiple payment records
print("\nOrders with Multiple Payments:")
print(
    (payments.groupby("order_id").size() > 1).sum()
)
