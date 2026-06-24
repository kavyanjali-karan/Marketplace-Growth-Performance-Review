SELECT

d.full_date,

SUM(f.revenue) revenue,

COUNT(*) orders,

SUM(quantity) units

FROM fact_orders f

JOIN dim_date d

ON f.date_key=d.date_key

GROUP BY d.full_date;