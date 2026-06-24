SELECT

seller_state,

SUM(revenue) revenue

FROM seller_mart

GROUP BY seller_state;