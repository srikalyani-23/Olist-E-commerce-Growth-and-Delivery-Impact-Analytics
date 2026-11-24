
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

# STEP 25: Filter only late orders

late_orders = delivery_analysis[
    delivery_analysis["delivery_status"] == "Late"
].copy()

# STEP 26: Calculate delay statistics

print("\nLate Delivery Statistics:")

print(
    late_orders["delivery_delay_days"].describe()
)

# STEP 27: Calculate average and median delay

print("\nAverage Days Late:")
print(late_orders["delivery_delay_days"].mean())

print("\nMedian Days Late:")
print(late_orders["delivery_delay_days"].median())

# STEP 28: Find maximum delay

print("\nMaximum Days Late:")
print(late_orders["delivery_delay_days"].max())

# STEP 29: Calculate total late orders

print("\nTotal Late Orders:")
print(len(late_orders))

# STEP 30: Extract purchase month

delivery_analysis["order_month"] = (
    delivery_analysis["order_purchase_timestamp"]
    .dt.to_period("M")
    .astype(str)
)

# STEP 31: Group data month-wise

monthly_delivery = (
    delivery_analysis
    .groupby("order_month")
    .agg(
        total_orders=("order_id", "nunique"),
        late_orders=(
            "delivery_status",
            lambda x: (x == "Late").sum()
        ),
        early_orders=(
            "delivery_status",
            lambda x: (x == "Early").sum()
        ),
        on_time_orders=(
            "delivery_status",
            lambda x: (x == "On Time").sum()
        )
    )
    .reset_index()
)

# STEP 32: Calculate monthly late delivery rate

monthly_delivery["late_delivery_rate"] = (
    monthly_delivery["late_orders"]
    / monthly_delivery["total_orders"]
    * 100
).round(2)

# STEP 33: Display results

print("\nMonthly Delivery Performance:")
print(monthly_delivery.to_string(index=False))


# STEP 40: Load order items and sellers

order_items = pd.read_csv(
    "data/raw/olist_order_items_dataset.csv"
)

sellers = pd.read_csv(
    "data/raw/olist_sellers_dataset.csv"
)

# STEP 41: Keep unique order-seller combinations

order_seller = order_items[
    ["order_id", "seller_id"]
].drop_duplicates()

# STEP 42: Add seller location

order_seller = order_seller.merge(
    sellers[["seller_id", "seller_state"]],
    on="seller_id",
    how="left"
)

# STEP 43: Join with delivery analysis

seller_delivery = delivery_analysis.merge(
    order_seller,
    on="order_id",
    how="inner"
)

# STEP 44: Calculate seller-wise performance

seller_performance = (
    seller_delivery
    .groupby(["seller_id", "seller_state"])
    .agg(
        total_orders=("order_id", "nunique"),
        late_orders=(
            "delivery_status",
            lambda x: (x == "Late").sum()
        ),
        early_orders=(
            "delivery_status",
            lambda x: (x == "Early").sum()
        ),
        on_time_orders=(
            "delivery_status",
            lambda x: (x == "On Time").sum()
        )
    )
    .reset_index()
)

# STEP 45: Calculate late delivery rate

seller_performance["late_delivery_rate"] = (
    seller_performance["late_orders"]
    / seller_performance["total_orders"]
    * 100
).round(2)

# STEP 46: Sort by highest late delivery rate

seller_performance = seller_performance.sort_values(
    "late_delivery_rate",
    ascending=False
)

print("\nTop 15 Sellers by Late Delivery Rate:")
print(seller_performance.head(15).to_string(index=False))

# STEP 47: Load reviews dataset

reviews = pd.read_csv(
    "data/raw/olist_order_reviews_dataset.csv"
)

# STEP 48: Aggregate review scores at order level

order_reviews = (
    reviews
    .groupby("order_id")
    .agg(
        average_review_score=("review_score", "mean"),
        review_count=("review_score", "count")
    )
    .reset_index()
)

# STEP 49: Merge reviews with delivery analysis

delivery_reviews = delivery_analysis.merge(
    order_reviews,
    on="order_id",
    how="inner"
)

# STEP 50: Classify orders into Late and Non-Late

delivery_reviews["delivery_group"] = (
    delivery_reviews["delivery_status"]
    .apply(
        lambda x: "Late" if x == "Late" else "Non-Late"
    )
)

# STEP 51: Compare average review scores

review_comparison = (
    delivery_reviews
    .groupby("delivery_group")
    .agg(
        total_orders=("order_id", "nunique"),
        average_review_score=("average_review_score", "mean"),
        median_review_score=("average_review_score", "median")
    )
    .round(2)
)

print("\nReview Score Comparison:")
print(review_comparison)

# STEP 52: Calculate review score difference

late_score = review_comparison.loc[
    "Late", "average_review_score"
]

non_late_score = review_comparison.loc[
    "Non-Late", "average_review_score"
]

print("\nReview Score Difference:")
print(round(non_late_score - late_score, 2))


# STEP 53: Import statistical libraries

from scipy import stats
import numpy as np

# STEP 54: Separate review scores into two groups

late_scores = delivery_reviews.loc[
    delivery_reviews["delivery_group"] == "Late",
    "average_review_score"
].dropna()

non_late_scores = delivery_reviews.loc[
    delivery_reviews["delivery_group"] == "Non-Late",
    "average_review_score"
].dropna()

# STEP 55: Perform Welch's independent t-test

t_statistic, p_value = stats.ttest_ind(
    late_scores,
    non_late_scores,
    equal_var=False
)

# STEP 56: Calculate difference in means

mean_difference = (
    late_scores.mean() - non_late_scores.mean()
)

# STEP 57: Calculate 95% confidence interval

n1 = len(late_scores)
n2 = len(non_late_scores)

var1 = late_scores.var(ddof=1)
var2 = non_late_scores.var(ddof=1)

standard_error = np.sqrt(
    (var1 / n1) + (var2 / n2)
)

degrees_freedom = (
    (var1 / n1 + var2 / n2) ** 2
    /
    (
        (var1 / n1) ** 2 / (n1 - 1)
        +
        (var2 / n2) ** 2 / (n2 - 1)
    )
)

critical_value = stats.t.ppf(
    0.975,
    degrees_freedom
)

margin_error = critical_value * standard_error

ci_lower = mean_difference - margin_error
ci_upper = mean_difference + margin_error

# STEP 58: Display results

print("\nStatistical Test Results")
print("Late group sample size:", n1)
print("Non-Late group sample size:", n2)
print("Mean difference (Late - Non-Late):", mean_difference)
print("T-statistic:", t_statistic)
print("P-value:", p_value)
print("95% Confidence Interval:", (ci_lower, ci_upper))

if p_value < 0.05:
    print("\nResult: Statistically significant difference.")
else:
    print("\nResult: No statistically significant difference.")

# STEP 59: Load customers dataset

customers = pd.read_csv(
    "data/raw/olist_customers_dataset.csv"
)

# STEP 60: Keep only delivered orders

delivered_orders = clean_orders[
    clean_orders["order_status"] == "delivered"
].copy()

# STEP 61: Connect orders with unique customer identity

customer_orders = delivered_orders.merge(
    customers[["customer_id", "customer_unique_id"]],
    on="customer_id",
    how="left"
)

# STEP 62: Count delivered orders per customer

customer_purchase_frequency = (
    customer_orders
    .groupby("customer_unique_id")
    .agg(
        total_orders=("order_id", "nunique")
    )
    .reset_index()
)

# STEP 63: Classify customers

customer_purchase_frequency["customer_type"] = (
    customer_purchase_frequency["total_orders"]
    .apply(
        lambda x: "Repeat Customer"
        if x > 1 else "One-Time Customer"
    )
)

# STEP 64: Calculate customer metrics

total_customers = len(customer_purchase_frequency)

repeat_customers = (
    customer_purchase_frequency["total_orders"] > 1
).sum()

one_time_customers = total_customers - repeat_customers

repeat_purchase_rate = (
    repeat_customers / total_customers
) * 100

print("\nCustomer Purchase Analysis")
print("Total Unique Customers:", total_customers)
print("Repeat Customers:", repeat_customers)
print("One-Time Customers:", one_time_customers)
print("Repeat Purchase Rate:", round(repeat_purchase_rate, 2), "%")

print(
    "Average Orders per Customer:",
    round(customer_purchase_frequency["total_orders"].mean(), 2)
)
# STEP 65: Load order items dataset

order_items = pd.read_csv(
    "data/raw/olist_order_items_dataset.csv"
)

print("\nOrder Items Shape:")
print(order_items.shape)

print("\nOrder Items Columns:")
print(order_items.columns.tolist())

# STEP 66: Aggregate product revenue at order level

order_revenue = (
    order_items
    .groupby("order_id")
    .agg(
        order_revenue=("price", "sum")
    )
    .reset_index()
)

print("\nOrder Revenue Sample:")
print(order_revenue.head())

print("\nTotal Order Revenue:")
print(round(order_revenue["order_revenue"].sum(), 2))

# STEP 67: Select delivered orders

delivered_orders = clean_orders[
    clean_orders["order_status"] == "delivered"
].copy()

# STEP 68: Add unique customer identity

customer_order_data = delivered_orders.merge(
    customers[
        ["customer_id", "customer_unique_id"]
    ],
    on="customer_id",
    how="left"
)

# STEP 69: Add order revenue

customer_order_data = customer_order_data.merge(
    order_revenue,
    on="order_id",
    how="left"
)

print("\nCustomer Order Data:")
print(customer_order_data.head())

print("\nShape:")
print(customer_order_data.shape)

print("\nMissing Values:")
print(customer_order_data[
    ["customer_unique_id", "order_revenue"]
].isnull().sum())

# STEP 70: Calculate reference date

reference_date = (
    customer_order_data["order_purchase_timestamp"].max()
    + pd.Timedelta(days=1)
)

print("\nRFM Reference Date:")
print(reference_date)

# STEP 71: Calculate customer-level RFM metrics

rfm = (
    customer_order_data
    .groupby("customer_unique_id")
    .agg(
        Recency=(
            "order_purchase_timestamp",
            lambda x: (reference_date - x.max()).days
        ),
        Frequency=(
            "order_id",
            "nunique"
        ),
        Monetary=(
            "order_revenue",
            "sum"
        )
    )
    .reset_index()
)

print("\nRFM Dataset:")
print(rfm.head(10))

print("\nRFM Summary:")
print(rfm[["Recency", "Frequency", "Monetary"]].describe())

# STEP 72: Recency scoring

rfm["R_Score"] = pd.qcut(
    rfm["Recency"],
    q=5,
    labels=[5, 4, 3, 2, 1]
).astype(int)

# STEP 78: Business-based Frequency scoring

rfm["F_Score"] = pd.cut(
    rfm["Frequency"],
    bins=[0, 1, 2, 3, 5, float("inf")],
    labels=[1, 2, 3, 4, 5]
).astype(int)

# STEP 74: Monetary scoring

rfm["M_Score"] = pd.qcut(
    rfm["Monetary"],
    q=5,
    labels=[1, 2, 3, 4, 5]
).astype(int)

# STEP 75: Combine RFM scores

rfm["RFM_Score"] = (
    rfm["R_Score"].astype(str)
    + rfm["F_Score"].astype(str)
    + rfm["M_Score"].astype(str)
)

print("\nRFM Score Distribution:")
print(rfm[
    ["R_Score", "F_Score", "M_Score"]
].describe())

print("\nRFM Sample:")
print(rfm.head(10))

# STEP 76: Create customer segments

def segment_customer(row):

    r = row["R_Score"]
    f = row["F_Score"]
    m = row["M_Score"]

    if r >= 4 and f >= 4 and m >= 4:
        return "Champions"

    elif f >= 4 and r >= 3:
        return "Loyal Customers"

    elif r >= 4 and 2 <= f <= 3:
        return "Potential Loyalists"

    elif r == 5 and f == 1:
        return "New Customers"

    elif r <= 2 and f >= 3:
        return "At Risk"

    elif r <= 2 and f <= 2:
        return "Hibernating"

    else:
        return "Others"


rfm["Customer_Segment"] = rfm.apply(
    segment_customer,
    axis=1
)

# STEP 77: Segment distribution

segment_summary = (
    rfm.groupby("Customer_Segment")
    .agg(
        total_customers=("customer_unique_id", "count"),
        avg_recency=("Recency", "mean"),
        avg_frequency=("Frequency", "mean"),
        avg_monetary=("Monetary", "mean")
    )
    .reset_index()
)

segment_summary["customer_percentage"] = (
    segment_summary["total_customers"]
    / len(rfm) * 100
).round(2)

segment_summary = segment_summary.sort_values(
    "total_customers",
    ascending=False
)

print("\nCustomer Segment Summary:")
print(segment_summary.round(2).to_string(index=False))

import matplotlib.pyplot as plt

plt.figure(figsize=(12, 6))

plt.bar(
    segment_summary["Customer_Segment"],
    segment_summary["total_customers"]
)

plt.title("Customer Segmentation Distribution")
plt.xlabel("Customer Segment")
plt.ylabel("Number of Customers")

plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# STEP 80: Calculate revenue contribution by segment

segment_revenue = (
    rfm.groupby("Customer_Segment")
    .agg(
        total_customers=("customer_unique_id", "count"),
        total_revenue=("Monetary", "sum"),
        avg_customer_revenue=("Monetary", "mean")
    )
    .reset_index()
)

# Calculate revenue percentage

total_revenue = segment_revenue["total_revenue"].sum()

segment_revenue["revenue_percentage"] = (
    segment_revenue["total_revenue"] / total_revenue
) * 100

# Sort by revenue contribution

segment_revenue = segment_revenue.sort_values(
    "total_revenue",
    ascending=False
)

print("\nSegment-wise Revenue Contribution:")

print(
    segment_revenue.round(2).to_string(index=False)
)

import matplotlib.pyplot as plt

plt.figure(figsize=(12, 6))

plt.bar(
    segment_revenue["Customer_Segment"],
    segment_revenue["revenue_percentage"]
)

plt.title("Revenue Contribution by Customer Segment")
plt.xlabel("Customer Segment")
plt.ylabel("Revenue Contribution (%)")

plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# STEP 82: Extract purchase month

cohort_data = customer_order_data[
    ["customer_unique_id", "order_id", "order_purchase_timestamp"]
].copy()

cohort_data["order_month"] = (
    cohort_data["order_purchase_timestamp"]
    .dt.to_period("M")
)

print(cohort_data.head())

# STEP 83: Find first purchase month

cohort_data["cohort_month"] = (
    cohort_data.groupby("customer_unique_id")["order_month"]
    .transform("min")
)

print(cohort_data.head(10))

# STEP 84: Calculate cohort index

cohort_data["cohort_index"] = (
    (cohort_data["order_month"].dt.year -
     cohort_data["cohort_month"].dt.year) * 12
    +
    (cohort_data["order_month"].dt.month -
     cohort_data["cohort_month"].dt.month)
    + 1
)

print(cohort_data.head(10))

# STEP 85: Count unique active customers

cohort_counts = (
    cohort_data.groupby(
        ["cohort_month", "cohort_index"]
    )["customer_unique_id"]
    .nunique()
    .reset_index()
)

cohort_counts = cohort_counts.rename(
    columns={"customer_unique_id": "customers"}
)

print(cohort_counts.head(15))

# STEP 86: Pivot cohort data

cohort_pivot = cohort_counts.pivot(
    index="cohort_month",
    columns="cohort_index",
    values="customers"
)

print("\nCohort Customer Matrix:")
print(cohort_pivot)

# STEP 87: Calculate retention percentage

cohort_size = cohort_pivot.iloc[:, 0]

retention_matrix = cohort_pivot.divide(
    cohort_size,
    axis=0
) * 100

print("\nMonthly Cohort Retention (%):")
print(retention_matrix.round(2))

import seaborn as sns
import matplotlib.pyplot as plt

plt.figure(figsize=(16, 10))

sns.heatmap(
    retention_matrix,
    annot=True,
    fmt=".1f",
    cmap="YlGnBu",
    vmin=0,
    vmax=100
)

plt.title("Monthly Customer Cohort Retention")
plt.xlabel("Months Since First Purchase")
plt.ylabel("Customer Acquisition Cohort")

plt.tight_layout()
plt.show()

import seaborn as sns
import matplotlib.pyplot as plt

plt.figure(figsize=(16, 10))

sns.heatmap(
    retention_matrix,
    annot=True,
    fmt=".1f",
    cmap="YlGnBu",
    vmin=0,
    vmax=100
)

plt.title("Monthly Customer Cohort Retention")
plt.xlabel("Months Since First Purchase")
plt.ylabel("Customer Acquisition Cohort")

plt.tight_layout()
plt.show()

# STEP 89: Select delivered orders

business_data = clean_orders[
    clean_orders["order_status"] == "delivered"
].copy()

print("Delivered Orders:", len(business_data))

# STEP 90: Merge order-level revenue

business_data = business_data.merge(
    order_revenue,
    on="order_id",
    how="left",
    validate="one_to_one"
)

print("\nBusiness Dataset:")
print(business_data.head())

print("\nMissing Revenue:")
print(business_data["order_revenue"].isna().sum())

# STEP 91: Extract purchase month

business_data["order_month"] = (
    business_data["order_purchase_timestamp"]
    .dt.to_period("M")
)

print(business_data[
    ["order_id", "order_month", "order_revenue"]
].head())

# STEP 92: Calculate monthly performance

monthly_performance = (
    business_data
    .groupby("order_month")
    .agg(
        total_orders=("order_id", "nunique"),
        total_revenue=("order_revenue", "sum")
    )
    .reset_index()
)

# Calculate Average Order Value

monthly_performance["AOV"] = (
    monthly_performance["total_revenue"]
    / monthly_performance["total_orders"]
)

print("\nMonthly Business Performance:")

print(
    monthly_performance.round(2).to_string(index=False)
)

# STEP 93: Calculate month-over-month growth

monthly_performance["revenue_growth_pct"] = (
    monthly_performance["total_revenue"]
    .pct_change() * 100
)

monthly_performance["order_growth_pct"] = (
    monthly_performance["total_orders"]
    .pct_change() * 100
)

print("\nMonthly Growth Analysis:")

print(
    monthly_performance.round(2).to_string(index=False)
)

import matplotlib.pyplot as plt

plt.figure(figsize=(14, 6))

plt.plot(
    monthly_performance["order_month"].astype(str),
    monthly_performance["total_revenue"],
    marker="o"
)

plt.title("Monthly Revenue Trend")
plt.xlabel("Month")
plt.ylabel("Revenue (R$)")

plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
plt.show()

fig, ax1 = plt.subplots(figsize=(14, 6))

ax1.bar(
    monthly_performance["order_month"].astype(str),
    monthly_performance["total_orders"],
    alpha=0.7
)

ax1.set_xlabel("Month")
ax1.set_ylabel("Total Orders")

ax2 = ax1.twinx()

ax2.plot(
    monthly_performance["order_month"].astype(str),
    monthly_performance["AOV"],
    marker="o"
)

ax2.set_ylabel("AOV (R$)")

plt.title("Monthly Orders vs Average Order Value")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# STEP 96: Load datasets

products = pd.read_csv(
    "data/raw/olist_products_dataset.csv"
)

category_translation = pd.read_csv(
    "data/raw/product_category_name_translation.csv"
)

print("Products Shape:", products.shape)
print("Category Translation Shape:", category_translation.shape)

# STEP 97: Add English category names

products = products.merge(
    category_translation,
    on="product_category_name",
    how="left",
    validate="many_to_one"
)

products["product_category_name_english"] = (
    products["product_category_name_english"]
    .fillna("Unknown")
)

print(products[
    ["product_id", "product_category_name",
     "product_category_name_english"]
].head(10))

# STEP 98: Select delivered order IDs

delivered_order_ids = clean_orders.loc[
    clean_orders["order_status"] == "delivered",
    "order_id"
]

delivered_items = order_items[
    order_items["order_id"].isin(delivered_order_ids)
].copy()

print("Delivered Order Items:", len(delivered_items))

# STEP 99: Add product category to order items

category_sales = delivered_items.merge(
    products[
        ["product_id", "product_category_name_english"]
    ],
    on="product_id",
    how="left",
    validate="many_to_one"
)

print(category_sales.head())

# STEP 100: Calculate revenue by category

category_revenue = (
    category_sales
    .groupby("product_category_name_english")
    .agg(
        total_revenue=("price", "sum"),
        total_items=("order_item_id", "count"),
        unique_orders=("order_id", "nunique")
    )
    .reset_index()
)

category_revenue = category_revenue.sort_values(
    "total_revenue",
    ascending=False
)

top_10_categories = category_revenue.head(10)

print("\nTop 10 Product Categories by Revenue:")
print(top_10_categories.round(2).to_string(index=False))

import matplotlib.pyplot as plt

plt.figure(figsize=(12, 6))

plt.barh(
    top_10_categories["product_category_name_english"],
    top_10_categories["total_revenue"]
)

plt.title("Top 10 Product Categories by Revenue")
plt.xlabel("Revenue (R$)")
plt.ylabel("Product Category")
plt.gca().invert_yaxis()

plt.tight_layout()
plt.show()

# STEP 102: Load customer data

customers = pd.read_csv(
    "data/raw/olist_customers_dataset.csv"
)

# Keep delivered orders

state_orders = clean_orders[
    clean_orders["order_status"] == "delivered"
].copy()

# Add order-level revenue

state_orders = state_orders.merge(
    order_revenue,
    on="order_id",
    how="left",
    validate="one_to_one"
)

# Add customer state

state_orders = state_orders.merge(
    customers[["customer_id", "customer_state"]],
    on="customer_id",
    how="left",
    validate="many_to_one"
)

print(state_orders.head())

# STEP 103: Aggregate revenue by customer state


# Attach actual unique customer IDs
state_orders_with_unique_id = state_orders.merge(
    customers[["customer_id", "customer_unique_id"]],
    on="customer_id",
    how="left",
    validate="many_to_one"
)

# State-wise revenue analysis
state_revenue = (
    state_orders_with_unique_id
    .groupby("customer_state")
    .agg(
        total_revenue=("order_revenue", "sum"),
        total_orders=("order_id", "nunique"),
        unique_customers=("customer_unique_id", "nunique")
    )
    .reset_index()
)

state_revenue = state_revenue.sort_values(
    "total_revenue",
    ascending=False
)

print("\nCorrected State Revenue:")
print(state_revenue.to_string(index=False))

top_10_states = state_revenue.head(10)

print("\nTop 10 States by Revenue:")
print(top_10_states.round(2).to_string(index=False))

plt.figure(figsize=(12, 6))

plt.bar(
    top_10_states["customer_state"],
    top_10_states["total_revenue"]
)

plt.title("Top 10 Brazilian States by Revenue")
plt.xlabel("Customer State")
plt.ylabel("Revenue (R$)")

plt.tight_layout()
plt.show()

# STEP 105: Create primary delivery analysis dataset

delivery_scenario = clean_orders[
    (clean_orders["order_status"] == "delivered") &
    (clean_orders["order_delivered_customer_date"].notna()) &
    (clean_orders["order_estimated_delivery_date"].notna())
].copy()

# Calculate delay in calendar days

delivery_scenario["delivery_delay_days"] = (
    delivery_scenario["order_delivered_customer_date"].dt.normalize()
    - delivery_scenario["order_estimated_delivery_date"].dt.normalize()
).dt.days

delivery_scenario["delivery_status"] = (
    delivery_scenario["delivery_delay_days"]
    .gt(0)
    .map({True: "Late", False: "Non-Late"})
)

print("Total eligible delivered orders:", len(delivery_scenario))
print("\nDelivery status:")
print(delivery_scenario["delivery_status"].value_counts())

# STEP 106: Baseline late delivery metrics

total_orders = len(delivery_scenario)

late_orders = (
    delivery_scenario["delivery_status"] == "Late"
).sum()

baseline_late_rate = late_orders / total_orders * 100

# Reduce late orders by 20% (relative reduction)

late_orders_reduced = round(late_orders * 0.20)

projected_late_orders = late_orders - late_orders_reduced

projected_late_rate = (
    projected_late_orders / total_orders
) * 100

print("\nDelivery Reduction Scenario")
print("Baseline late orders:", late_orders)
print("Late orders converted:", late_orders_reduced)
print("Projected late orders:", projected_late_orders)
print("Baseline late rate:", round(baseline_late_rate, 2), "%")
print("Projected late rate:", round(projected_late_rate, 2), "%")

# STEP 107: Load reviews

reviews = pd.read_csv(
    "data/raw/olist_order_reviews_dataset.csv"
)

# Aggregate reviews at order level

order_reviews = (
    reviews.groupby("order_id")
    .agg(
        avg_review_score=("review_score", "mean")
    )
    .reset_index()
)

# Merge with delivery data

review_scenario = delivery_scenario.merge(
    order_reviews,
    on="order_id",
    how="inner",
    validate="one_to_one"
)

print("Orders with review scores:", len(review_scenario))
print("\nAverage review score by delivery status:")

print(
    review_scenario.groupby("delivery_status")["avg_review_score"]
    .agg(["count", "mean", "median"])
)

# STEP 108: Compare review scores

late_review_mean = review_scenario.loc[
    review_scenario["delivery_status"] == "Late",
    "avg_review_score"
].mean()

nonlate_review_mean = review_scenario.loc[
    review_scenario["delivery_status"] == "Non-Late",
    "avg_review_score"
].mean()

review_gap = nonlate_review_mean - late_review_mean

# Calculate scenario on the reviewed-order population

reviewed_late_count = (
    review_scenario["delivery_status"] == "Late"
).sum()

reviewed_total = len(review_scenario)

converted_review_orders = round(
    reviewed_late_count * 0.20
)

baseline_average_review = (
    review_scenario["avg_review_score"].mean()
)

projected_average_review = (
    baseline_average_review
    + (
        converted_review_orders
        * review_gap
        / reviewed_total
    )
)

print("\nReview Score Impact Scenario")
print("Late group average:", round(late_review_mean, 2))
print("Non-late group average:", round(nonlate_review_mean, 2))
print("Observed review score gap:", round(review_gap, 2))
print("Potential converted reviewed orders:", converted_review_orders)
print("Baseline overall average:", round(baseline_average_review, 3))
print("Projected overall average:", round(projected_average_review, 3))
print("Potential improvement:", round(
    projected_average_review - baseline_average_review, 3
))

# STEP 109: Load customer identity

customers = pd.read_csv(
    "data/raw/olist_customers_dataset.csv"
)

customer_delivery = delivery_scenario.merge(
    customers[["customer_id", "customer_unique_id"]],
    on="customer_id",
    how="left",
    validate="many_to_one"
)

print(customer_delivery.head())

# STEP 110: Customer-level delivery and purchase history

customer_delivery_summary = (
    customer_delivery
    .groupby("customer_unique_id")
    .agg(
        total_orders=("order_id", "nunique"),
        had_late_delivery=(
            "delivery_status",
            lambda x: (x == "Late").any()
        )
    )
    .reset_index()
)

customer_delivery_summary["customer_type"] = (
    customer_delivery_summary["total_orders"]
    .gt(1)
    .map({True: "Repeat", False: "One-Time"})
)

print(customer_delivery_summary.head())

# STEP 111: Compare repeat purchase by delivery experience

repeat_comparison = (
    customer_delivery_summary
    .groupby("had_late_delivery")
    .agg(
        total_customers=("customer_unique_id", "count"),
        repeat_customers=(
            "customer_type",
            lambda x: (x == "Repeat").sum()
        )
    )
    .reset_index()
)

repeat_comparison["repeat_rate"] = (
    repeat_comparison["repeat_customers"]
    / repeat_comparison["total_customers"]
    * 100
)

print("\nRepeat Purchase by Delivery Experience:")
print(repeat_comparison.round(2).to_string(index=False))

# STEP 112: Illustrative customer recovery scenario

late_group = customer_delivery_summary[
    customer_delivery_summary["had_late_delivery"]
]

nonlate_group = customer_delivery_summary[
    ~customer_delivery_summary["had_late_delivery"]
]

late_customer_count = len(late_group)
nonlate_customer_count = len(nonlate_group)

late_repeat_rate = (
    (late_group["customer_type"] == "Repeat").mean()
)

nonlate_repeat_rate = (
    (nonlate_group["customer_type"] == "Repeat").mean()
)

# Assume 20% of late-exposed customers are fully recovered

recovered_customers = round(
    late_customer_count * 0.20
)

additional_repeat_customers = (
    recovered_customers
    * (nonlate_repeat_rate - late_repeat_rate)
)

baseline_repeat_customers = (
    customer_delivery_summary["customer_type"] == "Repeat"
).sum()

projected_repeat_customers = (
    baseline_repeat_customers + additional_repeat_customers
)

baseline_customer_count = len(customer_delivery_summary)

projected_repeat_rate = (
    projected_repeat_customers / baseline_customer_count
) * 100

print("\nIllustrative Repeat Purchase Scenario")
print("Late-exposed customers:", late_customer_count)
print("Recovered customers assumed:", recovered_customers)
print("Baseline repeat customers:", baseline_repeat_customers)
print("Estimated additional repeat customers:",
      round(additional_repeat_customers, 2))
print("Projected repeat customers:",
      round(projected_repeat_customers, 2))
print("Projected repeat rate:",
      round(projected_repeat_rate, 2), "%")

# STEP 113: Identify each customer's first delivered order

first_order_data = customer_delivery.sort_values(
    ["customer_unique_id", "order_purchase_timestamp"]
).drop_duplicates(
    subset="customer_unique_id",
    keep="first"
).copy()

# Convert delivery status into Late / Non-Late

first_order_data["first_order_experience"] = (
    first_order_data["delivery_status"]
    .apply(lambda x: "Late" if x == "Late" else "Non-Late")
)

print("\nFirst Order Delivery Experience:")
print(first_order_data[
    ["customer_unique_id", "order_id",
     "delivery_status", "first_order_experience"]
].head(10))

# STEP 114: Count delivered orders per customer

customer_order_counts = (
    customer_delivery.groupby("customer_unique_id")
    .agg(
        total_delivered_orders=("order_id", "nunique")
    )
    .reset_index()
)

first_order_repeat = first_order_data[
    ["customer_unique_id", "first_order_experience"]
].merge(
    customer_order_counts,
    on="customer_unique_id",
    how="inner",
    validate="one_to_one"
)

first_order_repeat["is_repeat"] = (
    first_order_repeat["total_delivered_orders"] > 1
)

print(first_order_repeat.head(10))

first_order_comparison = (
    first_order_repeat.groupby("first_order_experience")
    .agg(
        total_customers=("customer_unique_id", "count"),
        repeat_customers=("is_repeat", "sum")
    )
    .reset_index()
)

first_order_comparison["repeat_rate"] = (
    first_order_comparison["repeat_customers"]
    / first_order_comparison["total_customers"]
    * 100
)

print("\nRepeat Purchase Based on First Order Experience:")
print(first_order_comparison.round(2).to_string(index=False))

# STEP 116: Chi-Square Test for Repeat Purchase

from scipy.stats import chi2_contingency

contingency_table = pd.crosstab(
    first_order_repeat["first_order_experience"],
    first_order_repeat["is_repeat"]
)

print("Contingency Table:")
print(contingency_table)

chi2_stat, p_value, dof, expected = chi2_contingency(
    contingency_table
)

print("\nChi-Square Test Results")
print("Chi-Square Statistic:", chi2_stat)
print("Degrees of Freedom:", dof)
print("P-value:", p_value)

if p_value < 0.05:
    print("Result: Statistically significant difference.")
else:
    print("Result: No statistically significant difference.")

    import numpy as np

total_observations = contingency_table.to_numpy().sum()

cramers_v = np.sqrt(
    chi2_stat / total_observations
)

print("Cramer's V:", round(cramers_v, 4))

# STEP 118: Prepare customers for 90-day analysis

# Sort customer orders by purchase date
customer_delivery = customer_delivery.sort_values(
    ["customer_unique_id", "order_purchase_timestamp"]
)

# Identify each customer's first delivered order
first_order_data = customer_delivery.drop_duplicates(
    subset="customer_unique_id",
    keep="first"
).copy()

# Create first order delivery experience
first_order_data["first_order_experience"] = (
    first_order_data["delivery_status"]
    .apply(lambda x: "Late" if x == "Late" else "Non-Late")
)

# Get actual dataset end date
dataset_end_date = customer_delivery[
    "order_purchase_timestamp"
].max()

# Calculate follow-up days
first_order_data["followup_days"] = (
    dataset_end_date -
    first_order_data["order_purchase_timestamp"]
).dt.days

# Keep customers with at least 90 days of follow-up
eligible_customers = first_order_data[
    first_order_data["followup_days"] >= 90
].copy()

print("Customers eligible for 90-day analysis:",
      len(eligible_customers))

print("\nSample eligible customers:")

print(eligible_customers[
    [
        "customer_unique_id",
        "first_order_experience",
        "followup_days"
    ]
].head())

# Get the actual last purchase date in the dataset
dataset_end_date = customer_delivery["order_purchase_timestamp"].max()

# Get eligible customer IDs
eligible_customer_ids = eligible_customers["customer_unique_id"]

# Keep all delivered orders of eligible customers
eligible_orders = customer_delivery[
    customer_delivery["customer_unique_id"].isin(
        eligible_customer_ids
    )
].copy()

# Sort orders customer-wise and date-wise
eligible_orders = eligible_orders.sort_values(
    ["customer_unique_id", "order_purchase_timestamp"]
)

# Get each eligible customer's first purchase date
first_purchase_dates = (
    eligible_orders.groupby("customer_unique_id")
    ["order_purchase_timestamp"]
    .min()
)

# Calculate days elapsed since first purchase
eligible_orders["days_since_first_order"] = (
    eligible_orders["order_purchase_timestamp"]
    - eligible_orders["customer_unique_id"].map(first_purchase_dates)
).dt.days

# Count repeat purchases within 90 days
repeat_90_days = (
    eligible_orders[
        eligible_orders["days_since_first_order"].between(1, 90)
    ]
    .groupby("customer_unique_id")
    .size()
)

# Add repeat status to eligible customers
eligible_customers["repeat_within_90_days"] = (
    eligible_customers["customer_unique_id"]
    .isin(repeat_90_days.index)
)

# Calculate repeat purchase rate
repeat_count_90 = eligible_customers[
    "repeat_within_90_days"
].sum()

total_eligible = len(eligible_customers)

repeat_rate_90 = (
    repeat_count_90 / total_eligible
) * 100

print("90-Day Customer Retention Analysis")
print("----------------------------------")
print("Eligible customers:", total_eligible)
print("Repeat customers within 90 days:", repeat_count_90)
print("Non-repeat customers:", total_eligible - repeat_count_90)
print("90-Day Repeat Purchase Rate:", round(repeat_rate_90, 2), "%")

# Group customers by their first delivery experience
repeat_90_comparison = (
    eligible_customers
    .groupby("first_order_experience")
    ["repeat_within_90_days"]
    .agg(
        total_customers="count",
        repeat_customers="sum"
    )
)

# Calculate repeat purchase rate
repeat_90_comparison["repeat_rate"] = (
    repeat_90_comparison["repeat_customers"]
    / repeat_90_comparison["total_customers"]
) * 100

print(repeat_90_comparison.round(2))

late_rate = repeat_90_comparison.loc["Late", "repeat_rate"]
nonlate_rate = repeat_90_comparison.loc["Non-Late", "repeat_rate"]

print("Late group repeat rate:", round(late_rate, 2), "%")
print("Non-Late group repeat rate:", round(nonlate_rate, 2), "%")

print(
    "Difference:",
    round(nonlate_rate - late_rate, 2),
    "percentage points"
)

from scipy.stats import chi2_contingency
import numpy as np

# Create contingency table
contingency_90 = pd.crosstab(
    eligible_customers["first_order_experience"],
    eligible_customers["repeat_within_90_days"]
)

print("Contingency Table:")
print(contingency_90)

# Chi-square test
chi2, p_value, dof, expected = chi2_contingency(contingency_90)

# Cramer's V
n = contingency_90.to_numpy().sum()
cramers_v = np.sqrt(
    chi2 / (n * min(contingency_90.shape[0] - 1,
                    contingency_90.shape[1] - 1))
)

print("\nChi-square:", round(chi2, 4))
print("P-value:", p_value)
print("Cramer's V:", round(cramers_v, 4))

import matplotlib.pyplot as plt

# Extract values for plotting
labels = ["Late", "Non-Late"]

rates = [
    repeat_90_comparison.loc["Late", "repeat_rate"],
    repeat_90_comparison.loc["Non-Late", "repeat_rate"]
]

# Create bar chart
plt.figure(figsize=(8, 5))

bars = plt.bar(labels, rates)

# Add percentage labels
for bar, rate in zip(bars, rates):
    plt.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height(),
        f"{rate:.2f}%",
        ha="center",
        va="bottom"
    )

plt.title("90-Day Repeat Purchase Rate by First Delivery Experience")
plt.xlabel("First Delivery Experience")
plt.ylabel("Repeat Purchase Rate (%)")
plt.ylim(0, max(rates) * 1.2)

plt.tight_layout()
plt.show()

# Use delivered orders with valid actual and estimated delivery dates
# Use all delivered orders with valid actual and estimated dates
delivery_kpi = delivery_scenario.copy()

total_delivered = len(delivery_kpi)

late_orders = (
    delivery_kpi["delivery_status"] == "Late"
).sum()

non_late_orders = (
    delivery_kpi["delivery_status"] == "Non-Late"
).sum()

late_rate = (late_orders / total_delivered) * 100

avg_delay_all = delivery_kpi["delivery_delay_days"].mean()

avg_late_delay = delivery_kpi.loc[
    delivery_kpi["delivery_status"] == "Late",
    "delivery_delay_days"
].mean()

median_late_delay = delivery_kpi.loc[
    delivery_kpi["delivery_status"] == "Late",
    "delivery_delay_days"
].median()

delivery_kpi_summary = pd.DataFrame({
    "Metric": [
        "Eligible Delivered Orders",
        "Late Orders",
        "Non-Late Orders",
        "Late Delivery Rate (%)",
        "Average Delay Across All Orders (Days)",
        "Average Delay Among Late Orders (Days)",
        "Median Delay Among Late Orders (Days)"
    ],
    "Value": [
        total_delivered,
        late_orders,
        non_late_orders,
        round(late_rate, 2),
        round(avg_delay_all, 2),
        round(avg_late_delay, 2),
        round(median_late_delay, 2)
    ]
})

print(delivery_kpi_summary.to_string(index=False))

# Create a copy of the primary delivery dataset
monthly_delivery_data = delivery_scenario.copy()

# Extract month from purchase timestamp
monthly_delivery_data["order_month"] = (
    monthly_delivery_data["order_purchase_timestamp"]
    .dt.to_period("M")
)

monthly_delivery_trend = (
    monthly_delivery_data
    .groupby("order_month")
    .agg(
        total_orders=("order_id", "nunique"),

        late_orders=(
            "delivery_status",
            lambda x: (x == "Late").sum()
        ),

        non_late_orders=(
            "delivery_status",
            lambda x: (x == "Non-Late").sum()
        )
    )
    .reset_index()
)

# Calculate late delivery percentage
monthly_delivery_trend["late_delivery_rate"] = (
    monthly_delivery_trend["late_orders"]
    / monthly_delivery_trend["total_orders"]
) * 100

print("\nMonthly Delivery Trend:")
print(monthly_delivery_trend.round(2).to_string(index=False))

# Sort months by highest late delivery rate
worst_delivery_months = monthly_delivery_trend.sort_values(
    "late_delivery_rate",
    ascending=False
)

print("\nTop 5 Months with Highest Late Delivery Rate:")

print(
    worst_delivery_months[
        [
            "order_month",
            "total_orders",
            "late_orders",
            "late_delivery_rate"
        ]
    ].head(5).round(2).to_string(index=False)
)

import matplotlib.pyplot as plt

plt.figure(figsize=(14, 6))

plt.plot(
    monthly_delivery_trend["order_month"].astype(str),
    monthly_delivery_trend["late_delivery_rate"],
    marker="o"
)

plt.title("Monthly Late Delivery Rate Trend")
plt.xlabel("Purchase Month")
plt.ylabel("Late Delivery Rate (%)")

plt.xticks(rotation=45)
plt.grid(True)

plt.tight_layout()
plt.show()

# Calculate 3-month rolling average
monthly_delivery_trend["rolling_3m_late_rate"] = (
    monthly_delivery_trend["late_delivery_rate"]
    .rolling(window=3, min_periods=3)
    .mean()
)

print("\nMonthly Late Delivery Rate with 3-Month Average:")

print(
    monthly_delivery_trend[
        [
            "order_month",
            "late_delivery_rate",
            "rolling_3m_late_rate"
        ]
    ].round(2).to_string(index=False)
)

import matplotlib.pyplot as plt

plt.figure(figsize=(14, 6))

plt.plot(
    monthly_delivery_trend["order_month"].astype(str),
    monthly_delivery_trend["late_delivery_rate"],
    marker="o",
    label="Monthly Late Delivery Rate"
)

plt.plot(
    monthly_delivery_trend["order_month"].astype(str),
    monthly_delivery_trend["rolling_3m_late_rate"],
    marker="s",
    label="3-Month Rolling Average"
)

plt.title("Monthly Late Delivery Rate vs 3-Month Rolling Average")
plt.xlabel("Month")
plt.ylabel("Late Delivery Rate (%)")

plt.xticks(rotation=45)
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# Keep unique order-seller combinations
order_seller = order_items[
    ["order_id", "seller_id"]
].drop_duplicates()

# Add seller location
order_seller = order_seller.merge(
    sellers[["seller_id", "seller_state"]],
    on="seller_id",
    how="left",
    validate="many_to_one"
)

# Join with the primary delivery dataset
seller_delivery_primary = delivery_scenario.merge(
    order_seller,
    on="order_id",
    how="inner"
)

print("Seller Delivery Dataset:")
print(seller_delivery_primary.shape)

print(seller_delivery_primary.head())

seller_performance = (
    seller_delivery_primary
    .groupby(["seller_id", "seller_state"])
    .agg(
        total_orders=("order_id", "nunique"),

        late_orders=(
            "delivery_status",
            lambda x: (x == "Late").sum()
        ),

        non_late_orders=(
            "delivery_status",
            lambda x: (x == "Non-Late").sum()
        )
    )
    .reset_index()
)

# Calculate late delivery rate
seller_performance["late_delivery_rate"] = (
    seller_performance["late_orders"]
    / seller_performance["total_orders"]
) * 100

print(seller_performance.head())

# Consider sellers with at least 30 delivered orders
qualified_sellers = seller_performance[
    seller_performance["total_orders"] >= 30
].copy()

# Rank sellers by late delivery rate
qualified_sellers = qualified_sellers.sort_values(
    "late_delivery_rate",
    ascending=False
)

print("Total Qualified Sellers:", len(qualified_sellers))

print("\nTop 15 Sellers with Highest Late Delivery Rate:")

print(
    qualified_sellers[
        [
            "seller_id",
            "seller_state",
            "total_orders",
            "late_orders",
            "late_delivery_rate"
        ]
    ].head(15).round(2).to_string(index=False)
)

import matplotlib.pyplot as plt

top_10_sellers = qualified_sellers.head(10).copy()

plt.figure(figsize=(12, 6))

plt.barh(
    top_10_sellers["seller_id"].astype(str).str[:8],
    top_10_sellers["late_delivery_rate"]
)

plt.title("Top 10 Sellers by Late Delivery Rate (Minimum 30 Orders)")
plt.xlabel("Late Delivery Rate (%)")
plt.ylabel("Seller ID")

plt.gca().invert_yaxis()
plt.tight_layout()
plt.show()

# Load customers dataset
customers = pd.read_csv(
    "data/raw/olist_customers_dataset.csv"
)

# Add customer state to delivery dataset
state_delivery = delivery_scenario.merge(
    customers[["customer_id", "customer_state"]],
    on="customer_id",
    how="left",
    validate="many_to_one"
)

print("State Delivery Dataset:")
print(state_delivery.shape)

print(state_delivery.head())

state_delivery_performance = (
    state_delivery
    .groupby("customer_state")
    .agg(
        total_orders=("order_id", "nunique"),

        late_orders=(
            "delivery_status",
            lambda x: (x == "Late").sum()
        ),

        non_late_orders=(
            "delivery_status",
            lambda x: (x == "Non-Late").sum()
        )
    )
    .reset_index()
)

# Calculate late delivery rate
state_delivery_performance["late_delivery_rate"] = (
    state_delivery_performance["late_orders"]
    / state_delivery_performance["total_orders"]
) * 100

print(state_delivery_performance.head())

qualified_states = state_delivery_performance[
    state_delivery_performance["total_orders"] >= 100
].copy()

# Sort by highest late delivery rate
qualified_states = qualified_states.sort_values(
    "late_delivery_rate",
    ascending=False
)

print("State-wise Delivery Performance:")

print(
    qualified_states[
        [
            "customer_state",
            "total_orders",
            "late_orders",
            "late_delivery_rate"
        ]
    ].round(2).to_string(index=False)
)

import matplotlib.pyplot as plt

top_10_states_delay = qualified_states.head(10)

plt.figure(figsize=(12, 6))

plt.barh(
    top_10_states_delay["customer_state"],
    top_10_states_delay["late_delivery_rate"]
)

plt.title("Top 10 States by Late Delivery Rate")
plt.xlabel("Late Delivery Rate (%)")
plt.ylabel("Customer State")

plt.gca().invert_yaxis()
plt.tight_layout()
plt.show()

# Select top 10 sellers by late delivery rate

# STEP 128: Identify High-Risk Sellers

# Top 10 sellers by late delivery rate
top_10_sellers = qualified_sellers.head(10).copy()

print("\nTop 10 Sellers with Highest Late Delivery Rate:")

print(
    top_10_sellers[
        [
            "seller_id",
            "seller_state",
            "total_orders",
            "late_orders",
            "late_delivery_rate"
        ]
    ].round(2).to_string(index=False)
)

# Top 10 sellers by absolute number of late orders
top_sellers_by_late_count = (
    qualified_sellers
    .sort_values("late_orders", ascending=False)
    .head(10)
)

print("\nTop 10 Sellers by Number of Late Orders:")

print(
    top_sellers_by_late_count[
        [
            "seller_id",
            "seller_state",
            "total_orders",
            "late_orders",
            "late_delivery_rate"
        ]
    ].round(2).to_string(index=False)
)


# Keep only the required delivery columns
review_delivery = delivery_scenario[
    ["order_id", "delivery_status"]
].copy()

print("Delivery Dataset:", review_delivery.shape)
print("Unique Orders:", review_delivery["order_id"].nunique())

reviews = pd.read_csv(
    "data/raw/olist_order_reviews_dataset.csv"
)

order_reviews = (
    reviews
    .groupby("order_id")
    .agg(
        review_score=("review_score", "mean"),
        review_count=("review_id", "count")
    )
    .reset_index()
)

print("Order-level Review Dataset:", order_reviews.shape)
print("Unique Review Orders:", order_reviews["order_id"].nunique())

review_analysis = review_delivery.merge(
    order_reviews,
    on="order_id",
    how="inner",
    validate="one_to_one"
)

print("Final Review Analysis Shape:", review_analysis.shape)

print(
    "Unique Orders:",
    review_analysis["order_id"].nunique()
)

print("Missing Review Scores:")
print(review_analysis["review_score"].isna().sum())

review_comparison = (
    review_analysis
    .groupby("delivery_status")
    .agg(
        total_orders=("order_id", "nunique"),
        average_review_score=("review_score", "mean"),
        median_review_score=("review_score", "median")
    )
    .reset_index()
)

print(review_comparison.round(2).to_string(index=False))

from scipy.stats import ttest_ind

late_scores = review_analysis.loc[
    review_analysis["delivery_status"] == "Late",
    "review_score"
].dropna()

non_late_scores = review_analysis.loc[
    review_analysis["delivery_status"] == "Non-Late",
    "review_score"
].dropna()

t_stat, p_value = ttest_ind(
    late_scores,
    non_late_scores,
    equal_var=False
)

print("Late Mean Score:", late_scores.mean())
print("Non-Late Mean Score:", non_late_scores.mean())
print("Difference:", late_scores.mean() - non_late_scores.mean())
print("T-statistic:", t_stat)
print("P-value:", p_value)

from scipy import stats
import numpy as np

late_mean = late_scores.mean()
non_late_mean = non_late_scores.mean()

difference = late_mean - non_late_mean

se = np.sqrt(
    late_scores.var(ddof=1) / len(late_scores)
    + non_late_scores.var(ddof=1) / len(non_late_scores)
)

df = (
    late_scores.var(ddof=1) / len(late_scores)
    + non_late_scores.var(ddof=1) / len(non_late_scores)
) ** 2 / (
    (late_scores.var(ddof=1) / len(late_scores)) ** 2
    / (len(late_scores) - 1)
    +
    (non_late_scores.var(ddof=1) / len(non_late_scores)) ** 2
    / (len(non_late_scores) - 1)
)

critical_value = stats.t.ppf(0.975, df)

ci_lower = difference - critical_value * se
ci_upper = difference + critical_value * se

print("Difference (Late - Non-Late):", round(difference, 4))
print("95% Confidence Interval:", (round(ci_lower, 4), round(ci_upper, 4)))

# Total eligible delivered orders
total_orders = delivery_scenario["order_id"].nunique()

# Late and non-late orders
late_orders = (
    delivery_scenario["delivery_status"] == "Late"
).sum()

non_late_orders = total_orders - late_orders

# Baseline late delivery rate
baseline_late_rate = (late_orders / total_orders) * 100

print("BASELINE DELIVERY PERFORMANCE")
print("------------------------------")
print("Total Orders:", total_orders)
print("Late Orders:", late_orders)
print("Non-Late Orders:", non_late_orders)
print("Late Delivery Rate:", round(baseline_late_rate, 2), "%")

# Target reduction
reduction_percentage = 20

# Number of late orders converted
converted_orders = round(
    late_orders * reduction_percentage / 100
)

# Projected late orders
projected_late_orders = late_orders - converted_orders

# Projected late delivery rate
projected_late_rate = (
    projected_late_orders / total_orders
) * 100

print("20% REDUCTION SCENARIO")
print("----------------------")
print("Converted Orders:", converted_orders)
print("Projected Late Orders:", projected_late_orders)
print("Projected Late Rate:", round(projected_late_rate, 2), "%")

print(
    "Improvement:",
    round(baseline_late_rate - projected_late_rate, 2),
    "percentage points"
)

# Separate review scores
late_scores = review_analysis.loc[
    review_analysis["delivery_status"] == "Late",
    "review_score"
].dropna()

non_late_scores = review_analysis.loc[
    review_analysis["delivery_status"] == "Non-Late",
    "review_score"
].dropna()

# Baseline review metrics
baseline_review_mean = review_analysis["review_score"].mean()

late_mean = late_scores.mean()
non_late_mean = non_late_scores.mean()

# Count reviewed late orders
reviewed_late_orders = len(late_scores)

# Estimate converted reviewed orders proportionally
converted_reviewed_orders = (
    reviewed_late_orders * reduction_percentage / 100
)

# Projected review score
projected_review_mean = (
    baseline_review_mean
    + (
        converted_reviewed_orders
        * (non_late_mean - late_mean)
        / len(review_analysis)
    )
)

print("REVIEW SCORE SCENARIO")
print("---------------------")
print("Baseline Average Review:", round(baseline_review_mean, 3))
print("Late Group Average:", round(late_mean, 3))
print("Non-Late Group Average:", round(non_late_mean, 3))
print("Projected Average Review:", round(projected_review_mean, 3))

print(
    "Potential Improvement:",
    round(projected_review_mean - baseline_review_mean, 3)
)

scenario_comparison = pd.DataFrame({
    "Metric": [
        "Total Delivered Orders",
        "Late Orders",
        "Late Delivery Rate",
        "Average Review Score"
    ],
    "Baseline": [
        total_orders,
        late_orders,
        round(baseline_late_rate, 2),
        round(baseline_review_mean, 3)
    ],
    "Projected": [
        total_orders,
        projected_late_orders,
        round(projected_late_rate, 2),
        round(projected_review_mean, 3)
    ]
})

print(scenario_comparison.to_string(index=False))

fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# Late delivery rate comparison
axes[0].bar(
    ["Baseline", "Projected"],
    [baseline_late_rate, projected_late_rate]
)
axes[0].set_title("Late Delivery Rate")
axes[0].set_ylabel("Rate (%)")

# Review score comparison
axes[1].bar(
    ["Baseline", "Projected"],
    [baseline_review_mean, projected_review_mean]
)
axes[1].set_title("Average Customer Review Score")
axes[1].set_ylabel("Average Score (out of 5)")

plt.tight_layout()
plt.show()

# Overall delivery metrics
total_orders = delivery_scenario["order_id"].nunique()

late_orders = (
    delivery_scenario["delivery_status"] == "Late"
).sum()

late_rate = (late_orders / total_orders) * 100

# Review metrics
late_mean_review = review_analysis.loc[
    review_analysis["delivery_status"] == "Late",
    "review_score"
].mean()

non_late_mean_review = review_analysis.loc[
    review_analysis["delivery_status"] == "Non-Late",
    "review_score"
].mean()

review_gap = non_late_mean_review - late_mean_review

# 90-day repeat purchase metrics from your earlier analysis
late_repeat_rate = (58 / 5697) * 100
non_late_repeat_rate = (906 / 69621) * 100

# Scenario improvement
scenario_improvement = late_rate - projected_late_rate

key_findings = {
    "Total Delivered Orders": total_orders,
    "Late Orders": late_orders,
    "Late Delivery Rate (%)": round(late_rate, 2),
    "Late Group Average Review": round(late_mean_review, 2),
    "Non-Late Group Average Review": round(non_late_mean_review, 2),
    "Review Score Gap": round(review_gap, 2),
    "Late First-Order Group 90-Day Repeat Rate (%)": round(late_repeat_rate, 2),
    "Non-Late First-Order Group 90-Day Repeat Rate (%)": round(non_late_repeat_rate, 2),
    "Projected Late Rate (%)": round(projected_late_rate, 2),
    "Scenario Improvement (percentage points)": round(scenario_improvement, 2)
}

for metric, value in key_findings.items():
    print(f"{metric}: {value}")

print("MONTHS WITH HIGHEST LATE DELIVERY RATES")

print(
    monthly_delivery_trend
    .sort_values("late_delivery_rate", ascending=False)
    .head(5)
    .round(2)
    .to_string(index=False)
)

print("TOP 5 HIGH-RISK STATES")

print(
    qualified_states[
        [
            "customer_state",
            "total_orders",
            "late_orders",
            "late_delivery_rate"
        ]
    ].head(5).round(2).to_string(index=False)
)

print("\nTOP 5 HIGH-RISK SELLERS")

print(
    qualified_sellers[
        [
            "seller_id",
            "seller_state",
            "total_orders",
            "late_orders",
            "late_delivery_rate"
        ]
    ].head(5).round(2).to_string(index=False)
)

print("========== DATASET VALIDATION ==========")

datasets_to_check = {
    "Orders": clean_orders,
    "Order Items": order_items,
    "Customers": customers,
    "Delivery Scenario": delivery_scenario,
    "Review Analysis": review_analysis
}

for name, df in datasets_to_check.items():
    print(f"\n{name}")
    print("Rows:", len(df))
    print("Columns:", len(df.columns))
    print("Duplicate rows:", df.duplicated().sum())

print("\n========== DELIVERY KPI VALIDATION ==========")

total_orders = delivery_scenario["order_id"].nunique()

late_orders = (
    delivery_scenario["delivery_status"] == "Late"
).sum()

non_late_orders = (
    delivery_scenario["delivery_status"] == "Non-Late"
).sum()

print("Total unique orders:", total_orders)
print("Late orders:", late_orders)
print("Non-late orders:", non_late_orders)

print("Category count check:", late_orders + non_late_orders)

print(
    "Late delivery rate:",
    round((late_orders / total_orders) * 100, 2),
    "%"
)

print(
    "Non-late delivery rate:",
    round((non_late_orders / total_orders) * 100, 2),
    "%"
)

print("\n========== REVIEW KPI VALIDATION ==========")

print("Review analysis rows:", len(review_analysis))

print(
    "Unique reviewed orders:",
    review_analysis["order_id"].nunique()
)

print(
    "Missing review scores:",
    review_analysis["review_score"].isna().sum()
)

print(
    "Review score minimum:",
    review_analysis["review_score"].min()
)

print(
    "Review score maximum:",
    review_analysis["review_score"].max()
)

print("\n========== REVENUE VALIDATION ==========")

delivered_order_ids = delivery_scenario["order_id"].unique()

delivered_items = order_items[
    order_items["order_id"].isin(delivered_order_ids)
].copy()

calculated_revenue = delivered_items["price"].sum()

print(
    "Delivered product revenue:",
    round(calculated_revenue, 2)
)

print(
    "Delivered item rows:",
    len(delivered_items)
)

print(
    "Unique delivered orders in items:",
    delivered_items["order_id"].nunique()
)

print("\n========== DATE QUALITY VALIDATION ==========")

print(
    "Delivered orders missing actual delivery date:",
    clean_orders.loc[
        clean_orders["order_status"] == "delivered",
        "order_delivered_customer_date"
    ].isna().sum()
)

print(
    "Delivery before carrier date:",
    (
        clean_orders["order_delivered_customer_date"]
        < clean_orders["order_delivered_carrier_date"]
    ).sum()
)

print(
    "Carrier before approval date:",
    (
        clean_orders["order_delivered_carrier_date"]
        < clean_orders["order_approved_at"]
    ).sum()
)

# STEP 134: REVENUE RECONCILIATION

# All delivered orders
all_delivered_ids = set(delivered_orders["order_id"])

# Orders eligible for delivery analysis
eligible_delivery_ids = set(delivery_scenario["order_id"])

# Delivered orders excluded due to missing delivery dates
excluded_order_ids = all_delivered_ids - eligible_delivery_ids

# Items belonging to excluded orders
excluded_items = order_items[
    order_items["order_id"].isin(excluded_order_ids)
].copy()

# Items belonging to all delivered orders
all_delivered_items = order_items[
    order_items["order_id"].isin(all_delivered_ids)
].copy()

# Items belonging to eligible delivery orders
eligible_items = order_items[
    order_items["order_id"].isin(eligible_delivery_ids)
].copy()

# Revenue calculations
excluded_revenue = excluded_items["price"].sum()
all_delivered_revenue = all_delivered_items["price"].sum()
eligible_revenue = eligible_items["price"].sum()

print("\n========== REVENUE RECONCILIATION ==========")

print("All delivered orders:", len(all_delivered_ids))
print("Eligible delivery orders:", len(eligible_delivery_ids))
print("Excluded delivered orders:", len(excluded_order_ids))

print("All delivered revenue:",
      round(all_delivered_revenue, 2))

print("Eligible delivery revenue:",
      round(eligible_revenue, 2))

print("Excluded orders revenue:",
      round(excluded_revenue, 2))

print("Revenue difference:",
      round(all_delivered_revenue - eligible_revenue, 2))


# STEP 135: FINAL VALIDATION SUMMARY

validation_summary = pd.DataFrame({
    "Check": [
        "Delivery order count",
        "Late + Non-Late count",
        "Unique orders in delivery dataset",
        "Review score range",
        "Revenue is non-negative",
        "Delivery rate total",
        "Revenue reconciliation"
    ],

    "Result": [
        total_orders > 0,

        late_orders + non_late_orders == total_orders,

        delivery_scenario["order_id"].nunique()
        == len(delivery_scenario),

        review_analysis["review_score"].between(1, 5).all(),

        (delivered_items["price"] >= 0).all(),

        round(
            (late_orders + non_late_orders) / total_orders * 100,
            2
        ) == 100,

        round(all_delivered_revenue, 2)
        == round(eligible_revenue + excluded_revenue, 2)
    ]
})

print("\n========== FINAL VALIDATION SUMMARY ==========")
print(validation_summary.to_string(index=False))

print("\nAll checks passed:",
      validation_summary["Result"].all())


# STEP 136: EXPORT PROCESSED DATASETS

import os

os.makedirs("data/processed", exist_ok=True)

processed_datasets = {
    "clean_orders": clean_orders,
    "delivery_scenario": delivery_scenario,
    "review_analysis": review_analysis,
    "rfm": rfm,
    "customer_delivery_summary": customer_delivery_summary,
    "monthly_performance": monthly_performance,
    "category_revenue": category_revenue,
    "state_revenue": state_revenue,
    "qualified_sellers": qualified_sellers,
    "state_delivery_performance": state_delivery_performance,
    "monthly_delivery_trend": monthly_delivery_trend,
    "validation_summary": validation_summary
}

print("\n========== EXPORTING PROCESSED DATASETS ==========")

for name, df in processed_datasets.items():

    file_path = f"data/processed/{name}.csv"

    df.to_csv(file_path, index=False)

    print(f"Exported: {name}.csv | Rows: {len(df)}")


# Verify exported files
processed_files = os.listdir("data/processed")

print("\n========== EXPORTED FILES ==========")

for file in processed_files:
    print(file)

print("\nTotal files exported:", len(processed_files))
