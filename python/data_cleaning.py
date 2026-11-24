import pandas as pd

# 1. Read original CSV
df = pd.read_csv("olist_orders_dataset.csv")

# 2. Convert date columns to datetime
date_columns = [
    "order_purchase_timestamp",
    "order_approved_at",
    "order_delivered_carrier_date",
    "order_delivered_customer_date",
    "order_estimated_delivery_date"
]

for col in date_columns:
    df[col] = pd.to_datetime(df[col], errors="coerce")

# 3. Flag invalid seller handover dates
df["invalid_handover_flag"] = (
    df["order_delivered_carrier_date"] < df["order_approved_at"]
)

# 4. Flag invalid shipping dates
df["invalid_shipping_flag"] = (
    df["order_delivered_carrier_date"] > df["order_delivered_customer_date"]
)

# 5. Save cleaned CSV
df.to_csv("olist_orders_cleaned.csv", index=False)

# 6. Verify
print(df.shape)
print(df.columns.tolist())


df_items = pd.read_csv("olist_order_items_dataset.csv")

df_items["shipping_limit_date"] = pd.to_datetime(
    df_items["shipping_limit_date"],
    errors="coerce"
)

# print(df_items["shipping_limit_date"].dtype)
# print(df_items["shipping_limit_date"].isnull().sum())

# df_items.to_csv("olist_order_items_cleaned.csv", index=False)



# ### 3. 

df_customers = pd.read_csv("olist_customers_dataset.csv")

df_customers["customer_zip_code_prefix"] = (
    df_customers["customer_zip_code_prefix"]
    .astype(str)
    .str.zfill(5)
)

# print(
#     df_customers["customer_zip_code_prefix"]
#     .str.len()
#     .value_counts()
# )
# df_customers.to_csv("olist_customers_cleaned.csv", index=False)


#### 4
df_products = pd.read_csv("olist_products_dataset.csv")

df_products["product_category_name"] = (
    df_products["product_category_name"].fillna("unknown")
)


# print(
#     df_products[
#         df_products["product_weight_g"].isnull()
#     ].to_string(index=False)
# )
# df_products.to_csv("olist_products_cleaned.csv", index=False)


#### 5 
df_sellers = pd.read_csv("olist_sellers_dataset.csv")
df_sellers["seller_zip_code_prefix"] = (
    df_sellers["seller_zip_code_prefix"]
    .astype(str)
    .str.zfill(5)
)

# print(df_sellers["seller_zip_code_prefix"].str.len().value_counts())

# df_sellers.to_csv("olist_sellers_cleaned.csv", index=False)


# ###6

df_payments = pd.read_csv("olist_order_payments_dataset.csv")
# df_payments.to_csv("olist_order_payments_cleaned.csv", index=False)


#### 7

df_reviews = pd.read_csv("olist_order_reviews_dataset.csv")

date_cols = [
    "review_creation_date",
    "review_answer_timestamp"
]

for col in date_cols:
    df_reviews[col] = pd.to_datetime(df_reviews[col], errors="coerce")

print(df_reviews[date_cols].dtypes)
print(df_reviews[date_cols].isnull().sum())
df_reviews = pd.read_csv("olist_order_reviews_dataset.csv")

date_cols = [
    "review_creation_date",
    "review_answer_timestamp"
]

for col in date_cols:
    df_reviews[col] = pd.to_datetime(df_reviews[col], errors="coerce")

# df_reviews.to_csv("olist_order_reviews_cleaned.csv", index=False)

###8

df_geo = pd.read_csv("olist_geolocation_dataset.csv")

# Convert ZIP prefix to 5-digit string
df_geo["geolocation_zip_code_prefix"] = (
    df_geo["geolocation_zip_code_prefix"]
    .astype(str)
    .str.zfill(5)
)

# Keep one representative location per ZIP prefix
df_geo_cleaned = df_geo.groupby(
    "geolocation_zip_code_prefix",
    as_index=False
).agg({
    "geolocation_lat": "mean",
    "geolocation_lng": "mean",
    "geolocation_city": "first",
    "geolocation_state": "first"
})

print(df_geo_cleaned.shape)
# df_geo_cleaned.to_csv("olist_geolocation_cleaned.csv", index=False)


## 9
df_translation = pd.read_csv("product_category_name_translation.csv")

df_translation.to_csv(
    "product_category_translation_cleaned.csv",
    index=False
)