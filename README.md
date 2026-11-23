# Olist-E-commerce-Growth-and-Delivery-Impact-Analytics
An end-to-end e-commerce data analysis project exploring customer behavior, sales performance, payment patterns, and delivery operations using the Olist Brazilian E-Commerce dataset.

## Project Overview

The objective of this project is to analyze e-commerce transactional data to understand business performance, identify operational inefficiencies, and uncover opportunities for business growth.

The analysis focuses on customer purchasing behavior, revenue performance, order fulfillment, delivery efficiency, and payment preferences to generate actionable business insights.

## Business Objectives

- Analyze overall e-commerce sales and revenue performance.
- Understand customer purchasing and repeat purchase behavior.
- Evaluate order delivery performance and identify late deliveries.
- Analyze payment method preferences.
- Examine product and seller-related business data.
- Identify opportunities to improve customer experience and operational efficiency.

## Dataset

**Source:** Olist Brazilian E-Commerce Public Dataset

The dataset contains multiple interconnected CSV files covering different aspects of the e-commerce business.

| Dataset | Description |
|---|---|
| Customers | Customer information and locations |
| Geolocation | Geographic coordinates and zip codes |
| Orders | Order status and timestamps |
| Order Items | Products purchased in each order |
| Payments | Payment types and transaction values |
| Reviews | Customer feedback and review scores |
| Products | Product details and categories |
| Sellers | Seller information and locations |
| Category Translation | Portuguese-to-English category mapping |

## Tools & Technologies

- **Python** – Data analysis and processing
- **Pandas** – Data manipulation and cleaning
- **NumPy** – Numerical operations
- **Matplotlib / Seaborn** – Data visualization (where used)
- **Jupyter Notebook / Python Scripts** – Analysis environment

## Project Workflow

1. **Data Inspection:** Examined individual datasets, their structure, columns, and data types.
2. **Data Validation:** Investigated primary keys, relationships, and data consistency.
3. **Data Cleaning:** Prepared datasets for analysis and handled relevant data quality issues.
4. **Exploratory Data Analysis:** Analyzed customer behavior, revenue, payments, and delivery performance.
5. **KPI Development:** Calculated key business performance indicators.
6. **Business Insights:** Interpreted findings and identified areas for improvement.

## Key Business Metrics & Findings

### 1. Customer Analysis

- Total Unique Customers: 96,096
- Repeat Customers: 2,997
- Repeat Customer Rate: 3.12%

**Insight:** The low repeat customer rate indicates an opportunity to strengthen customer retention and encourage repeat purchases.

### 2. Revenue Analysis

- Total Product Revenue: R$13,591,643.70
- Delivered Product Revenue: R$13,221,498.11
- Average Order Value: R$137.75
- Delivered Average Order Value: R$137.04

**Insight:** Revenue analysis provides a baseline for evaluating sales performance and identifying opportunities to improve order value.

### 3. Delivery Performance

- Total Orders: 99,441
- Delivered Orders: 96,478
- Average Delivery Time: 12.56 days
- Late Orders: 7,826
- Late Delivery Rate: 8.11%

**Insight:** Delivery delays represent an opportunity to improve logistics operations, delivery planning, and customer satisfaction.

### 4. Payment Analysis

| Payment Method | Transactions | Share |
|---|---:|---:|
| Credit Card | 76,795 | 73.92% |
| Boleto | 19,784 | 19.04% |
| Voucher | 5,775 | 5.56% |
| Debit Card | 1,529 | 1.47% |

**Insight:** Credit cards dominate customer payment preferences, accounting for approximately 74% of payment records.

## Business Recommendations

Based on the analysis:

- **Customer Retention:** Introduce loyalty programs and targeted campaigns to encourage repeat purchases.
- **Delivery Optimization:** Investigate delayed orders and improve logistics coordination.
- **Revenue Growth:** Explore strategies to increase average order value through product recommendations and cross-selling.
- **Payment Experience:** Continue optimizing the dominant credit card payment experience while supporting alternative payment methods.
- **Customer Experience:** Monitor delivery performance and customer feedback to identify service improvement opportunities.

## Repository Structure

```text
olist_project/
│
├── data/
│   └── raw/
│       ├── olist_customers_dataset.csv
│       ├── olist_geolocation_dataset.csv
│       ├── olist_order_items_dataset.csv
│       ├── olist_order_payments_dataset.csv
│       ├── olist_order_reviews_dataset.csv
│       ├── olist_orders_dataset.csv
│       ├── olist_products_dataset.csv
│       ├── olist_sellers_dataset.csv
│       └── product_category_name_translation.csv
│
├── check_dataset.py
├── clean_orders.py
├── inspect_category_translation.py
├── inspect_customers.py
├── inspect_geolocation.py
├── inspect_order_items.py
├── inspect_orders.py
├── inspect_payments.py
├── inspect_products.py
├── inspect_reviews.py
├── inspect_sellers.py
├── investigate_reviews.py
├── validate_keys.py
├── data_dictionary.md
└── README.md
```

## Key Learnings

Through this project, I gained practical experience in:

- Working with multiple related datasets.
- Data inspection and validation.
- Data cleaning and preprocessing.
- Exploratory Data Analysis (EDA).
- Business KPI calculation and interpretation.
- Translating analytical findings into business recommendations.

## Dataset Source

Olist Brazilian E-Commerce Public Dataset:

https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce

## Author

**Kalyani Srivastava**

B.Tech Information Technology | Aspiring Data Analyst

GitHub: https://github.com/srikalyani-23

