def test_customer_unique(customers):
    assert customers["customer_id"].duplicated().sum() == 0

def test_no_null_customer_ids(customers):
    assert customers["customer_id"].isnull().sum() == 0

def test_10k_customers(customers):
    assert len(customers) == 10000