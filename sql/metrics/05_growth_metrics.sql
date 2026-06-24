SELECT

month,

SUM(revenue) revenue,

COUNT(*) orders

FROM marketplace_mart

GROUP BY month;