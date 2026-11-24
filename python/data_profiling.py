
import pandas as pd
from pathlib import Path

# checking all the files:rows, columns, missing values, duplicates.
folder = Path(__file__).resolve().parent
for file in sorted(folder.glob("*.csv")):
    df = pd.read_csv(file)

    # print("\nFile:", file.name)
    # print("Rows:", df.shape[0])
    # print("Columns:", df.shape[1])
    # print("Missing Values:", df.isnull().sum().sum())
    # print("Duplicates:", df.duplicated().sum())


df = pd.read_csv("olist_orders_dataset.csv")

# print(df.isnull().sum())
# print(df.duplicated().sum())

# print(df["order_status"].value_counts())


# print(
#     df[df["order_status"] == "delivered"]
#     ["order_delivered_customer_date"]
#     .isnull()
#     .sum()
# )
# # 8
# missing_deliveries = df[
#     (df["order_status"] == "delivered") &
#     (df["order_delivered_customer_date"].isnull())
# ]
# print(missing_deliveries)

# print(
#     df[
#         (df["order_status"] == "delivered") &
#         (df["order_approved_at"].isnull())
#     ].shape[0]
# )
# 14

# print(
#     df[
#         (df["order_status"] == "delivered") &
#         (df["order_delivered_carrier_date"].isnull())
#     ].shape[0]
# )
# 2




# checking types and converting into date datatype in 5 columns
# print(df.dtypes)

# print(df[[
#     "order_purchase_timestamp",
#     "order_approved_at",
#     "order_delivered_carrier_date",
#     "order_delivered_customer_date",
#     "order_estimated_delivery_date"
# ]].head())

# converting datatype to datetime
date_columns = [
    "order_purchase_timestamp",
    "order_approved_at",
    "order_delivered_carrier_date",
    "order_delivered_customer_date",
    "order_estimated_delivery_date"
]

for col in date_columns:
    df[col] = pd.to_datetime(df[col], errors="coerce")

# print(df.dtypes)

# print(df[date_columns].isnull().sum())

invalid_dates = df[
    df["order_delivered_customer_date"]
    < df["order_purchase_timestamp"]
]

# print(invalid_dates.shape[0])

invalid_carrier_dates = df[
    df["order_delivered_carrier_date"]
    > df["order_delivered_customer_date"]
]

# print(invalid_carrier_dates.shape[0])

invalid_carrier_dates = invalid_carrier_dates.copy()

invalid_carrier_dates["difference"] = (
    invalid_carrier_dates["order_delivered_carrier_date"]
    - invalid_carrier_dates["order_delivered_customer_date"]
)

# print(invalid_carrier_dates[[
#     "order_delivered_carrier_date",
#     "order_delivered_customer_date",
#     "difference"
# ]].head(10))


invalid_approval_dates = df[
    df["order_approved_at"] < df["order_purchase_timestamp"]
]
# print(invalid_approval_dates.shape[0])


invalid_handover = df[
    df["order_delivered_carrier_date"] < df["order_approved_at"]
]
# print(invalid_handover.shape[0])


invalid_handover = invalid_handover.copy()

invalid_handover["difference"] = (
    invalid_handover["order_approved_at"]
    - invalid_handover["order_delivered_carrier_date"]
)

# print(invalid_handover[[
#     "order_approved_at",
#     "order_delivered_carrier_date",
#     "difference"
# ]].head(10))


df["invalid_handover_flag"] = (
    df["order_delivered_carrier_date"] < df["order_approved_at"]
)
df["invalid_shipping_flag"] = (
    df["order_delivered_carrier_date"] > df["order_delivered_customer_date"]
)
# print(df[[
#     "invalid_handover_flag",
#     "invalid_shipping_flag"
# ]].sum())




# ### 2nd csv : olist_order_items_dataset.csv

df_items = pd.read_csv("olist_order_items_dataset.csv")

# print(df_items.head())
# print(df_items.shape)
# print(df_items.dtypes)
# print(df_items.isnull().sum())
# print("Duplicates:", df_items.duplicated().sum())


# print(
#     df_items.duplicated(
#         subset=["order_id", "order_item_id"]
#     ).sum()
# )


# print("Negative Prices:", (df_items["price"] < 0).sum())
# print("Negative Freight:", (df_items["freight_value"] < 0).sum())

# print(df_items["shipping_limit_date"].head())


df_items["shipping_limit_date"] = pd.to_datetime(
    df_items["shipping_limit_date"],
    errors="coerce"
)

# print(df_items["shipping_limit_date"].dtype)
# print(df_items["shipping_limit_date"].isnull().sum())



# ##3
df_customers = pd.read_csv("olist_customers_dataset.csv")

# print(df_customers.head())
# print(df_customers.shape)
# print(df_customers.dtypes)
# print(df_customers.isnull().sum())
# print("Duplicates:", df_customers.duplicated().sum())


# print("Unique Customer IDs:", df_customers["customer_id"].nunique())
# print("Unique Actual Customers:", df_customers["customer_unique_id"].nunique())

# counts = df_customers["customer_unique_id"].value_counts()
# print("Repeat Customers:", (counts > 1).sum())


# print(df_customers["customer_zip_code_prefix"].astype(str).str.len().value_counts())

#### 4 "olist_products_dataset.csv"


df_products = pd.read_csv("olist_products_dataset.csv")

# print(df_products.head())
# print(df_products.shape)
# print(df_products.dtypes)
# print(df_products.isnull().sum())
# print("Duplicates:", df_products.duplicated().sum())


cols = [
    "product_category_name",
    "product_name_lenght",
    "product_description_lenght",
    "product_photos_qty"
]

# print(df_products[cols].isnull().all(axis=1).sum())



#### 5. olist_sellers_dataset.csv

df_sellers = pd.read_csv("olist_sellers_dataset.csv")

# print(df_sellers.shape)
# print(df_sellers.dtypes)
# print(df_sellers.isnull().sum())
# print("Duplicates:", df_sellers.duplicated().sum())
# print("Duplicate Seller IDs:", df_sellers["seller_id"].duplicated().sum())

# print(
#     df_sellers["seller_zip_code_prefix"]
#     .astype(str)
#     .str.len()
#     .value_counts()
# )



#### 6

df_payments = pd.read_csv("olist_order_payments_dataset.csv")

# print(df_payments.shape)
# print(df_payments.dtypes)
# print(df_payments.isnull().sum())
# print("Duplicates:", df_payments.duplicated().sum())

# print("Negative payments:", (df_payments["payment_value"] < 0).sum())
# print("Zero payments:", (df_payments["payment_value"] == 0).sum())

# print(
#     df_payments[df_payments["payment_value"] == 0]
#     [["order_id", "payment_type", "payment_installments", "payment_value"]]
#     .to_string(index=False)
# )

# print(
#     "Duplicate payment keys:",
#     df_payments.duplicated(
#         subset=["order_id", "payment_sequential"]
#     ).sum()
# )



# 7

df_reviews = pd.read_csv("olist_order_reviews_dataset.csv")

# print(df_reviews.shape)
# print(df_reviews.dtypes)
# print(df_reviews.isnull().sum())
# print("Duplicates:", df_reviews.duplicated().sum())

# print(df_reviews["review_score"].value_counts().sort_index())

# print("Duplicate Review IDs:", df_reviews["review_id"].duplicated().sum())
# print("Duplicate Order IDs:", df_reviews["order_id"].duplicated().sum())

duplicate_reviews = df_reviews[
    df_reviews["review_id"].duplicated(keep=False)
]

# print(
#     duplicate_reviews.sort_values("review_id")
#     .head(10)
#     .to_string(index=False)
# )

# print(
#     df_reviews.groupby("review_id")["order_id"]
#     .nunique()
#     .value_counts()
#     .sort_index()
# )
# print(
#     df_reviews.groupby("order_id")["review_score"]
#     .nunique()
#     .value_counts()
#     .sort_index()
# )


#### 8

df_geo = pd.read_csv("olist_geolocation_dataset.csv")

# print(df_geo.shape)
# print(df_geo.dtypes)
# print(df_geo.isnull().sum())
# print("Duplicates:", df_geo.duplicated().sum())

# print("Unique ZIP prefixes:", df_geo["geolocation_zip_code_prefix"].nunique())


### 9 
df_translation = pd.read_csv("product_category_name_translation.csv")

print(df_translation.shape)
print(df_translation.dtypes)
print(df_translation.isnull().sum())
print("Duplicates:", df_translation.duplicated().sum())
print(
    "Duplicate Categories:",
    df_translation["product_category_name"].duplicated().sum()
)