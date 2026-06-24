SELECT

customer_state,

COUNT(DISTINCT customer_id) customers

FROM marketplace_mart

GROUP BY customer_state;