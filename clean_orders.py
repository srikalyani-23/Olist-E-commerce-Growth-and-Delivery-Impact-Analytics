
import pandas as pd
import os

# STEP 1: Load original dataset
orders = pd.read_csv(
    "data/raw/olist_orders_dataset.csv"
)

# STEP 2: Create a separate working copy
clean_orders = orders.copy()

# STEP 3: Identify date columns
date_columns = [
    "order_purchase_timestamp",
    "order_approved_at",
    "order_delivered_carrier_date",
    "order_delivered_customer_date",
    "order_estimated_delivery_date"
]

# STEP 4: Convert date columns into datetime format
for column in date_columns:
    clean_orders[column] = pd.to_datetime(
        clean_orders[column],
        errors="coerce"
    )

# STEP 5: Check updated data types
print("\nUpdated Data Types:")
print(clean_orders.dtypes)

# STEP 6: Check missing values after conversion
print("\nMissing Values:")
print(clean_orders.isnull().sum())

# STEP 7: Check dataset shape
print("\nDataset Shape:")
print(clean_orders.shape)


# STEP 8: Check missing delivery dates by order status

print("\nMissing Delivery Dates by Order Status:")

print(
    clean_orders.groupby("order_status")[
        "order_delivered_customer_date"
    ].apply(lambda x: x.isnull().sum())
)

# STEP 9: Check delivered orders with missing actual delivery date

delivered_missing = clean_orders[
    (clean_orders["order_status"] == "delivered") &
    (clean_orders["order_delivered_customer_date"].isnull())
]

print("\nDelivered Orders with Missing Delivery Date:")
print(len(delivered_missing))

# STEP 10: Check invalid date sequences

purchase_after_approval = (
    clean_orders["order_approved_at"].notna() &
    (clean_orders["order_approved_at"] <
     clean_orders["order_purchase_timestamp"])
)

carrier_before_approval = (
    clean_orders["order_delivered_carrier_date"].notna() &
    clean_orders["order_approved_at"].notna() &
    (clean_orders["order_delivered_carrier_date"] <
     clean_orders["order_approved_at"])
)

delivery_before_carrier = (
    clean_orders["order_delivered_customer_date"].notna() &
    clean_orders["order_delivered_carrier_date"].notna() &
    (clean_orders["order_delivered_customer_date"] <
     clean_orders["order_delivered_carrier_date"])
)

print("\nInvalid Date Sequences:")

print("Approval before Purchase:",
      purchase_after_approval.sum())

print("Carrier before Approval:",
      carrier_before_approval.sum())

print("Delivery before Carrier:",
      delivery_before_carrier.sum())

# STEP 11: Investigate carrier date before approval

carrier_before_approval_records = clean_orders[
    clean_orders["order_delivered_carrier_date"].notna() &
    clean_orders["order_approved_at"].notna() &
    (
        clean_orders["order_delivered_carrier_date"] <
        clean_orders["order_approved_at"]
    )
]

print("\nCarrier Before Approval - Sample Records:")
print(
    carrier_before_approval_records[
        [
            "order_id",
            "order_status",
            "order_approved_at",
            "order_delivered_carrier_date"
        ]
    ].head(10)
)

# STEP 12: Investigate delivery before carrier

delivery_before_carrier_records = clean_orders[
    clean_orders["order_delivered_customer_date"].notna() &
    clean_orders["order_delivered_carrier_date"].notna() &
    (
        clean_orders["order_delivered_customer_date"] <
        clean_orders["order_delivered_carrier_date"]
    )
]

print("\nDelivery Before Carrier - Sample Records:")
print(
    delivery_before_carrier_records[
        [
            "order_id",
            "order_status",
            "order_delivered_carrier_date",
            "order_delivered_customer_date"
        ]
    ].head(10)
)

# STEP 13: Investigate delivered orders with missing dates

print("\nDelivered Orders Missing Delivery Date:")
print(
    delivered_missing[
        [
            "order_id",
            "order_status",
            "order_purchase_timestamp",
            "order_delivered_carrier_date",
            "order_estimated_delivery_date"
        ]
    ]
)

# STEP 14: Check carrier-before-approval anomalies by status

print("\nCarrier Before Approval by Order Status:")

print(
    carrier_before_approval_records[
        "order_status"
    ].value_counts()
)

# STEP 15: Check delivery-before-carrier anomalies by status

print("\nDelivery Before Carrier by Order Status:")

print(
    delivery_before_carrier_records[
        "order_status"
    ].value_counts()
)

# STEP 16: Check missing delivery dates by status

print("\nDelivered Missing Delivery Date Status:")

print(
    delivered_missing["order_status"].value_counts()
)

# STEP 17: Create data quality flags

clean_orders["carrier_before_approval_flag"] = (
    clean_orders["order_approved_at"].notna() &
    clean_orders["order_delivered_carrier_date"].notna() &
    (
        clean_orders["order_delivered_carrier_date"] <
        clean_orders["order_approved_at"]
    )
)

clean_orders["delivery_before_carrier_flag"] = (
    clean_orders["order_delivered_customer_date"].notna() &
    clean_orders["order_delivered_carrier_date"].notna() &
    (
        clean_orders["order_delivered_customer_date"] <
        clean_orders["order_delivered_carrier_date"]
    )
)

clean_orders["missing_delivery_date_flag"] = (
    (clean_orders["order_status"] == "delivered") &
    clean_orders["order_delivered_customer_date"].isna()
)

# STEP 18: Create primary delivery analysis dataset

delivery_analysis = clean_orders[
    (clean_orders["order_status"] == "delivered") &
    clean_orders["order_delivered_customer_date"].notna() &
    clean_orders["order_estimated_delivery_date"].notna() &
    (~clean_orders["delivery_before_carrier_flag"])
].copy()

# STEP 19: Display validation results

print("\nData Quality Flags:")

print(
    clean_orders[
        [
            "carrier_before_approval_flag",
            "delivery_before_carrier_flag",
            "missing_delivery_date_flag"
        ]
    ].sum()
)

print("\nPrimary Delivery Analysis Dataset:")
print("Rows:", len(delivery_analysis))
print("Columns:", len(delivery_analysis.columns))

# STEP 20: Calculate delivery delay in days

delivery_analysis["delivery_delay_days"] = (
    delivery_analysis["order_delivered_customer_date"]
    .dt.normalize()
    -
    delivery_analysis["order_estimated_delivery_date"]
    .dt.normalize()
).dt.days

# STEP 21: Classify delivery performance

delivery_analysis["delivery_status"] = "On Time"

delivery_analysis.loc[
    delivery_analysis["delivery_delay_days"] < 0,
    "delivery_status"
] = "Early"

delivery_analysis.loc[
    delivery_analysis["delivery_delay_days"] > 0,
    "delivery_status"
] = "Late"

# STEP 22: Count delivery categories

print("\nDelivery Performance Distribution:")

print(
    delivery_analysis["delivery_status"].value_counts()
)

# STEP 23: Calculate delivery percentages

print("\nDelivery Performance Percentages:")

print(
    delivery_analysis["delivery_status"]
    .value_counts(normalize=True)
    .mul(100)
    .round(2)
)

# STEP 24: Average delivery delay

print("\nAverage Delivery Delay:")

print(
    delivery_analysis["delivery_delay_days"].mean()
)
