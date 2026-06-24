SELECT

category,

SUM(revenue) revenue,

COUNT(*) orders

FROM fact_orders f

JOIN dim_product p

ON f.product_key=p.product_key

GROUP BY category;