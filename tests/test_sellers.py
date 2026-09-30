def test_seller_unique(sellers):
    assert sellers["seller_id"].duplicated().sum() == 0

def test_200_sellers(sellers):
    assert len(sellers) == 200

def test_all_orders_have_seller(orders):
    assert orders["seller_id"].isnull().sum() == 0