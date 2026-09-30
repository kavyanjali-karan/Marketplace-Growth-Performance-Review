def test_revenue_non_negative(orders):
    assert (orders["revenue"] >= 0).all()

def test_revenue_positive_sum(orders):
    assert orders["revenue"].sum() > 0

def test_profit_bounded(orders):
    assert (orders["profit"] <= orders["revenue"]).all()

def test_returns_cancellations_8pct(orders):
    total = len(orders)
    bad = orders[orders["order_status"].isin(["Returned", "Cancelled"])].shape[0]
    pct = bad / total * 100
    assert 6.0 < pct < 10.0  # Between 6% and 10%