SELECT * FROM orders;
SELECT * FROM order_items;

CREATE TABLE orders (
    order_id VARCHAR(50) PRIMARY KEY,
    customer_id VARCHAR(50),
    order_status VARCHAR(30),
    order_purchase_timestamp TIMESTAMP,
    order_approved_at TIMESTAMP,
    order_delivered_carrier_date TIMESTAMP,
    order_delivered_customer_date TIMESTAMP,
    order_estimated_delivery_date TIMESTAMP,
    invalid_handover_flag BOOLEAN,
    invalid_shipping_flag BOOLEAN
);

SELECT COUNT(*) AS total_orders
FROM orders;


CREATE TABLE order_items (
    order_id VARCHAR(50),
    order_item_id INTEGER,
    product_id VARCHAR(50),
    seller_id VARCHAR(50),
    shipping_limit_date TIMESTAMP,
    price NUMERIC(10,2),
    freight_value NUMERIC(10,2),
    PRIMARY KEY (order_id, order_item_id)
);
SELECT COUNT(*) AS total_orders
FROM product_category_translation;


CREATE TABLE customers (
    customer_id VARCHAR(50) PRIMARY KEY,
    customer_unique_id VARCHAR(50),
    customer_zip_code_prefix VARCHAR(5),
    customer_city VARCHAR(100),
    customer_state VARCHAR(10)
);

CREATE TABLE products (
    product_id VARCHAR(50) PRIMARY KEY,
    product_category_name VARCHAR(100),
    product_name_lenght DOUBLE PRECISION,
    product_description_lenght DOUBLE PRECISION,
    product_photos_qty DOUBLE PRECISION,
    product_weight_g DOUBLE PRECISION,
    product_length_cm DOUBLE PRECISION,
    product_height_cm DOUBLE PRECISION,
    product_width_cm DOUBLE PRECISION
);


CREATE TABLE sellers (
    seller_id VARCHAR(50) PRIMARY KEY,
    seller_zip_code_prefix VARCHAR(5),
    seller_city VARCHAR(100),
    seller_state VARCHAR(10)
);


CREATE TABLE order_payments (
    order_id VARCHAR(50),
    payment_sequential INTEGER,
    payment_type VARCHAR(30),
    payment_installments INTEGER,
    payment_value NUMERIC(12,2),
    PRIMARY KEY (order_id, payment_sequential)
);

CREATE TABLE order_reviews (
    review_id VARCHAR(50),
    order_id VARCHAR(50),
    review_score INTEGER,
    review_comment_title TEXT,
    review_comment_message TEXT,
    review_creation_date TIMESTAMP,
    review_answer_timestamp TIMESTAMP
);

CREATE TABLE geolocation (
    geolocation_zip_code_prefix VARCHAR(5) PRIMARY KEY,
    geolocation_lat DOUBLE PRECISION,
    geolocation_lng DOUBLE PRECISION,
    geolocation_city VARCHAR(100),
    geolocation_state VARCHAR(10)
);


CREATE TABLE product_category_translation (
    product_category_name VARCHAR(100) PRIMARY KEY,
    product_category_name_english VARCHAR(100)
);

SELECT
    order_status,
    COUNT(*) AS total_orders
FROM orders
GROUP BY order_status
ORDER BY total_orders DESC;

-- 2
SELECT
    DATE_TRUNC('month', order_purchase_timestamp)::DATE AS order_month,
    COUNT(*) AS total_orders
FROM orders
GROUP BY order_month
ORDER BY order_month;

-- 3
SELECT
    ROUND(
        AVG(
            EXTRACT(EPOCH FROM (
                order_delivered_customer_date - order_purchase_timestamp
            )) / 86400
        )::NUMERIC,
        2
    ) AS avg_delivery_days
FROM orders
WHERE order_status = 'delivered'
  AND order_delivered_customer_date IS NOT NULL;


-- 4 late delivery percentage
SELECT
    COUNT(*) AS total_delivered_orders,

    COUNT(*) FILTER (
        WHERE order_delivered_customer_date::DATE >
              order_estimated_delivery_date::DATE
    ) AS late_orders,

    ROUND(
        100.0 * COUNT(*) FILTER (
            WHERE order_delivered_customer_date::DATE >
                  order_estimated_delivery_date::DATE
        ) / COUNT(*),
        2
    ) AS late_delivery_percentage

FROM orders
WHERE order_status = 'delivered'
  AND order_delivered_customer_date IS NOT NULL
  AND order_estimated_delivery_date IS NOT NULL;


-- 5 avg delay days
SELECT
    ROUND(
        AVG(
            order_delivered_customer_date::DATE -
            order_estimated_delivery_date::DATE
        ),
        2
    ) AS avg_delay_days
FROM orders
WHERE order_status = 'delivered'
  AND order_delivered_customer_date::DATE >
      order_estimated_delivery_date::DATE;

-- 2. 1 late vs ontime delivery ratings. customer satisfaction

WITH order_ratings AS (
    SELECT
        order_id,
        AVG(review_score) AS avg_review_score
    FROM order_reviews
    GROUP BY order_id
)
SELECT
    CASE
        WHEN o.order_delivered_customer_date::DATE >
             o.order_estimated_delivery_date::DATE
        THEN 'Late'
        ELSE 'On Time'
    END AS delivery_status,

    COUNT(*) AS total_orders,

    ROUND(AVG(r.avg_review_score), 2) AS avg_rating

FROM orders o
JOIN order_ratings r
    ON o.order_id = r.order_id

WHERE o.order_status = 'delivered'
  AND o.order_delivered_customer_date IS NOT NULL
  AND o.order_estimated_delivery_date IS NOT NULL

GROUP BY delivery_status;

-- 2.2 low rating percentage
WITH order_ratings AS (
    SELECT
        order_id,
        AVG(review_score) AS avg_review_score
    FROM order_reviews
    GROUP BY order_id
),
delivery_reviews AS (
    SELECT
        CASE
            WHEN o.order_delivered_customer_date::DATE >
                 o.order_estimated_delivery_date::DATE
            THEN 'Late'
            ELSE 'On Time'
        END AS delivery_status,
        r.avg_review_score
    FROM orders o
    JOIN order_ratings r
        ON o.order_id = r.order_id
    WHERE o.order_status = 'delivered'
      AND o.order_delivered_customer_date IS NOT NULL
      AND o.order_estimated_delivery_date IS NOT NULL
)
SELECT
    delivery_status,
    COUNT(*) AS total_orders,
    COUNT(*) FILTER (
        WHERE avg_review_score <= 2
    ) AS low_rated_orders,
    ROUND(
        100.0 * COUNT(*) FILTER (
            WHERE avg_review_score <= 2
        ) / COUNT(*),
        2
    ) AS low_rating_percentage
FROM delivery_reviews
GROUP BY delivery_status;



-- 3 seller performance
-- Seller Shipping Deadline Performance
SELECT
    COUNT(*) AS total_items,

    COUNT(*) FILTER (
        WHERE o.order_delivered_carrier_date >
              oi.shipping_limit_date
    ) AS late_handover_items,

    ROUND(
        100.0 * COUNT(*) FILTER (
            WHERE o.order_delivered_carrier_date >
                  oi.shipping_limit_date
        ) / COUNT(*),
        2
    ) AS late_handover_percentage

FROM order_items oi
JOIN orders o
    ON oi.order_id = o.order_id

WHERE o.order_delivered_carrier_date IS NOT NULL
  AND oi.shipping_limit_date IS NOT NULL;

-- 2 Seller-wise Performance
  SELECT
    oi.seller_id,
    COUNT(*) AS total_items,
    COUNT(*) FILTER (
        WHERE o.order_delivered_carrier_date >
              oi.shipping_limit_date
    ) AS late_items,
    ROUND(
        100.0 * COUNT(*) FILTER (
            WHERE o.order_delivered_carrier_date >
                  oi.shipping_limit_date
        ) / COUNT(*),
        2
    ) AS late_percentage
FROM order_items oi
JOIN orders o
    ON oi.order_id = o.order_id
WHERE o.order_delivered_carrier_date IS NOT NULL
  AND oi.shipping_limit_date IS NOT NULL
GROUP BY oi.seller_id
HAVING COUNT(*) >= 30
ORDER BY late_percentage DESC, total_items DESC
LIMIT 10;

-- 3 Seller Processing Time
SELECT
    ROUND(
        AVG(
            EXTRACT(EPOCH FROM (
                order_delivered_carrier_date - order_approved_at
            )) / 86400
        )::NUMERIC,
        2
    ) AS avg_processing_days
FROM orders
WHERE order_approved_at IS NOT NULL
  AND order_delivered_carrier_date IS NOT NULL
  AND invalid_handover_flag = FALSE;


  -- 4 late delivery in which state of brazil is highest

  SELECT
    c.customer_state,
    COUNT(*) AS total_orders,
    COUNT(*) FILTER (
        WHERE o.order_delivered_customer_date::DATE >
              o.order_estimated_delivery_date::DATE
    ) AS late_orders,
    ROUND(
        100.0 * COUNT(*) FILTER (
            WHERE o.order_delivered_customer_date::DATE >
                  o.order_estimated_delivery_date::DATE
        ) / COUNT(*),
        2
    ) AS late_percentage
FROM orders o
JOIN customers c
    ON o.customer_id = c.customer_id
WHERE o.order_status = 'delivered'
  AND o.order_delivered_customer_date IS NOT NULL
  AND o.order_estimated_delivery_date IS NOT NULL
GROUP BY c.customer_state
ORDER BY late_percentage DESC;



-- 5 product category wise delivery performance
WITH category_orders AS (
    SELECT DISTINCT
        oi.order_id,
        p.product_category_name
    FROM order_items oi
    JOIN products p
        ON oi.product_id = p.product_id
)
SELECT
    COALESCE(t.product_category_name_english,
             co.product_category_name) AS category,
    COUNT(*) AS total_orders,
    COUNT(*) FILTER (
        WHERE o.order_delivered_customer_date::DATE >
              o.order_estimated_delivery_date::DATE
    ) AS late_orders,
    ROUND(
        100.0 * COUNT(*) FILTER (
            WHERE o.order_delivered_customer_date::DATE >
                  o.order_estimated_delivery_date::DATE
        ) / COUNT(*),
        2
    ) AS late_percentage
FROM category_orders co
JOIN orders o
    ON co.order_id = o.order_id
LEFT JOIN product_category_translation t
    ON co.product_category_name = t.product_category_name
WHERE o.order_status = 'delivered'
  AND o.order_delivered_customer_date IS NOT NULL
  AND o.order_estimated_delivery_date IS NOT NULL
GROUP BY 1
HAVING COUNT(*) >= 100
ORDER BY late_percentage DESC
LIMIT 10;


-- monthly late deliver trend
SELECT
    DATE_TRUNC('month', order_delivered_customer_date)::DATE AS delivery_month,
    COUNT(*) AS total_delivered_orders,

    COUNT(*) FILTER (
        WHERE order_delivered_customer_date::DATE >
              order_estimated_delivery_date::DATE
    ) AS late_orders,

    ROUND(
        100.0 * COUNT(*) FILTER (
            WHERE order_delivered_customer_date::DATE >
                  order_estimated_delivery_date::DATE
        ) / COUNT(*),
        2
    ) AS late_percentage

FROM orders
WHERE order_status = 'delivered'
  AND order_delivered_customer_date IS NOT NULL
  AND order_estimated_delivery_date IS NOT NULL

GROUP BY delivery_month
ORDER BY delivery_month;


WITH order_locations AS (
    SELECT DISTINCT
        o.order_id,
        o.order_purchase_timestamp,
        o.order_delivered_customer_date,
        CASE
            WHEN s.seller_state = c.customer_state
            THEN 'Same State'
            ELSE 'Different State'
        END AS location_type
    FROM orders o
    JOIN customers c
        ON o.customer_id = c.customer_id
    JOIN order_items oi
        ON o.order_id = oi.order_id
    JOIN sellers s
        ON oi.seller_id = s.seller_id
    WHERE o.order_status = 'delivered'
      AND o.order_delivered_customer_date IS NOT NULL
)
SELECT
    location_type,
    COUNT(*) AS total_orders,
    ROUND(
        AVG(
            EXTRACT(EPOCH FROM (
                order_delivered_customer_date -
                order_purchase_timestamp
            )) / 86400
        )::NUMERIC,
        2
    ) AS avg_delivery_days
FROM order_locations
GROUP BY location_type;


