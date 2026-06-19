-- Repeat Purchase Analysis

SELECT
customer_unique_id,
COUNT(order_id) AS total_orders
FROM customer_orders
GROUP BY customer_unique_id
HAVING COUNT(order_id) > 1;