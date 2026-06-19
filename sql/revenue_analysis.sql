-- Monthly Revenue Analysis

SELECT
DATE_TRUNC('month', order_purchase_timestamp) AS month,
SUM(payment_value) AS revenue
FROM orders o
JOIN order_payments p
ON o.order_id = p.order_id
GROUP BY 1
ORDER BY 1;