-- RFM Customer Segmentation

SELECT
customer_unique_id,
MAX(order_purchase_timestamp) AS last_order_date,
COUNT(order_id) AS frequency,
SUM(payment_value) AS monetary
FROM customer_orders
GROUP BY customer_unique_id;