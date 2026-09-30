def test_has_orders(orders):
    assert len(orders) > 0

def test_has_date_range(orders):
    assert "order_date" in orders.columns
    assert orders["order_date"].notnull().all()

def test_monthly_coverage(orders):
    orders["month"] = orders["order_date"].str[:7]
    monthly = orders.groupby("month")["order_id"].count()
    assert monthly.min() > 1000  # At least 1K orders per month