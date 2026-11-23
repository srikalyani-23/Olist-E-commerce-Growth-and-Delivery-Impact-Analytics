
# Olist E-commerce Project
## Data Dictionary

### 1. Orders Table
File: olist_orders_dataset.csv

| Column | Description |
|---|---|
| order_id | Unique order identifier |
| customer_id | Customer record identifier |
| order_status | Current/final order status |
| order_purchase_timestamp | Purchase date and time |
| order_approved_at | Order approval timestamp |
| order_delivered_carrier_date | Carrier handover timestamp |
| order_delivered_customer_date | Actual customer delivery timestamp |
| order_estimated_delivery_date | Estimated delivery date |

### 2. Order Items Table
File: olist_order_items_dataset.csv

| Column | Description |
|---|---|
| order_id | Order identifier |
| order_item_id | Item sequence within order |
| product_id | Product identifier |
| seller_id | Seller identifier |
| shipping_limit_date | Seller shipping deadline |
| price | Product price |
| freight_value | Shipping charge |

### 3. Customers Table
File: olist_customers_dataset.csv

| Column | Description |
|---|---|
| customer_id | Customer record identifier |
| customer_unique_id | Actual unique customer identifier |
| customer_zip_code_prefix | Postal code prefix |
| customer_city | Customer city |
| customer_state | Customer state |

### 4. Sellers Table
File: olist_sellers_dataset.csv

| Column | Description |
|---|---|
| seller_id | Seller identifier |
| seller_zip_code_prefix | Seller postal code prefix |
| seller_city | Seller city |
| seller_state | Seller state |

### 5. Products Table
File: olist_products_dataset.csv

| Column | Description |
|---|---|
| product_id | Product identifier |
| product_category_name | Product category |
| product_name_lenght | Product name length |
| product_description_lenght | Description length |
| product_photos_qty | Number of product photos |
| product_weight_g | Product weight |
| product_length_cm | Product length |
| product_height_cm | Product height |
| product_width_cm | Product width |

### 6. Payments Table
File: olist_order_payments_dataset.csv

| Column | Description |
|---|---|
| order_id | Order identifier |
| payment_sequential | Payment sequence |
| payment_type | Payment method |
| payment_installments | Number of installments |
| payment_value | Payment amount |

### 7. Reviews Table
File: olist_order_reviews_dataset.csv

| Column | Description |
|---|---|
| review_id | Review identifier |
| order_id | Associated order |
| review_score | Customer rating |
| review_comment_title | Review title |
| review_comment_message | Review message |
| review_creation_date | Review creation timestamp |
| review_answer_timestamp | Review response timestamp |

### 8. Geolocation Table
File: olist_geolocation_dataset.csv

| Column | Description |
|---|---|
| geolocation_zip_code_prefix | Postal code prefix |
| geolocation_lat | Latitude |
| geolocation_lng | Longitude |
| geolocation_city | City |
| geolocation_state | State |

### 9. Category Translation Table
File: product_category_name_translation.csv

| Column | Description |
|---|---|
| product_category_name | Portuguese category |
| product_category_name_english | English category |
