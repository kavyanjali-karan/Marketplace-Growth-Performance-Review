def test_orders(orders):
    assert len(orders) == 75000

def test_no_null_order_ids(orders):
    assert orders["order_id"].isnull().sum() == 0

def test_unique_composite_key(orders):
    key_cols = ["order_id"]
    assert orders.duplicated(subset=key_cols).sum() == 0

def test_valid_statuses(orders):
    valid = {"Delivered", "Returned", "Cancelled"}
    assert set(orders["order_status"].unique()).issubset(valid)