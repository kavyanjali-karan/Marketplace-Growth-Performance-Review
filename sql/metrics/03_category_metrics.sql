SELECT

category,

SUM(revenue) revenue

FROM category_mart

GROUP BY category;