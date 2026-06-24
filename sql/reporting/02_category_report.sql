SELECT

category,

SUM(revenue) revenue

FROM category_mart

GROUP BY category

ORDER BY revenue DESC;