SELECT

month,

SUM(revenue),

COUNT(*) orders

FROM marketplace_mart

GROUP BY month;