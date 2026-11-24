# 🛒 Olist E-Commerce Data Analysis

An end-to-end exploratory data analysis project using the **Brazilian E-Commerce Public Dataset by Olist** to investigate customer behavior, order performance, product categories, seller activity, payment patterns, and delivery operations.

## 📌 Project Overview

This project focuses on exploring and understanding a real-world e-commerce dataset containing information about customers, orders, products, sellers, payments, reviews, and geographical locations.

The objective is to inspect raw datasets, understand their structure, identify data quality issues, validate relationships between datasets, and prepare reliable data for further business analysis.

## 🎯 Project Objectives

- Explore and understand multiple interconnected e-commerce datasets.
- Perform data quality checks and identify inconsistencies.
- Analyze customer, order, product, seller, and payment data.
- Investigate customer reviews and delivery performance.
- Validate primary and foreign key relationships.
- Clean and prepare datasets for downstream analysis.
- Extract meaningful business insights from e-commerce data.

## 🗂️ Project Structure

```text
olist-ecommerce-analysis/
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
│
├── data_dictionary.md
└── README.md
```

## 📊 Dataset Description

The project uses nine CSV files from the Olist Brazilian E-Commerce Public Dataset.

| Dataset | Description |
|---|---|
| Customers | Customer details and location IDs |
| Geolocation | Brazilian ZIP code geographical information |
| Order Items | Products purchased within each order |
| Order Payments | Payment methods and transaction values |
| Order Reviews | Customer ratings and review comments |
| Orders | Order status and important timestamps |
| Products | Product attributes and category information |
| Sellers | Seller details and location IDs |
| Category Translation | Portuguese-to-English category mapping |

## 🛠️ Technologies Used

- **Python** – Data exploration and cleaning
- **Pandas** – Data manipulation and processing
- **NumPy** – Numerical operations
- **Git & GitHub** – Version control and project management

## 🔍 Project Workflow

### 1. Dataset Inspection
- Examine dataset dimensions and column names.
- Understand data types and structures.
- Identify missing values and duplicate records.
- Inspect individual datasets.

### 2. Data Quality Assessment
- Investigate missing and inconsistent values.
- Examine duplicate records.
- Check data integrity and consistency.
- Investigate customer review data.

### 3. Data Cleaning
- Clean order-related records.
- Handle data quality issues.
- Prepare datasets for further analysis.

### 4. Data Validation
- Validate primary key uniqueness.
- Check foreign key relationships.
- Investigate relationships between interconnected datasets.

### 5. Business Analysis
Prepare the cleaned datasets for analysis of:
- Customer purchasing behavior
- Order and revenue performance
- Product category performance
- Seller performance
- Payment distribution
- Delivery efficiency
- Customer satisfaction

## 📁 Documentation

The repository includes:

- `data_dictionary.md` – Dataset and column-level documentation.
- `README.md` – Project overview, structure, and workflow.

## 🚀 Getting Started

### Prerequisites

- Python 3.x
- Pandas
- NumPy

### Installation

**1. Clone the repository**

```bash
git clone <YOUR_REPOSITORY_URL>
```

**2. Navigate to the project directory**

```bash
cd olist-ecommerce-analysis
```

**3. Install dependencies**

```bash
pip install pandas numpy
```

**4. Run the inspection scripts**

```bash
python check_dataset.py
python inspect_customers.py
python inspect_orders.py
python validate_keys.py
```

Other inspection and cleaning scripts can be executed individually.

## 💡 Expected Business Value

The analysis aims to support better business understanding through:

- Identifying customer purchasing patterns.
- Evaluating revenue and order performance.
- Understanding payment preferences.
- Monitoring delivery performance.
- Examining customer satisfaction.
- Identifying potential data quality issues.

## 📌 Dataset Source

Brazilian E-Commerce Public Dataset by Olist.

Source: Kaggle – Brazilian E-Commerce Public Dataset by Olist.

## 👩‍💻 Author

**Kalyani**

B.Tech – Information Technology | Aspiring Data Analyst

GitHub: [Your GitHub Profile](https://github.com/)

---

*This project is developed for practical learning and portfolio demonstration, focusing on real-world e-commerce data exploration, data quality assessment, and business analysis.*
