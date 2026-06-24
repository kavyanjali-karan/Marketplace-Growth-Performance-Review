SELECT

seller_state,

SUM(revenue) revenue,

COUNT(*) orders

FROM fact_orders f

JOIN dim_seller s

ON f.seller_key=s.seller_key

GROUP BY seller_state;