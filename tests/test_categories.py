def test_categories(orders_with_category):
    assert orders_with_category["category"].isnull().sum() == 0

def test_six_categories(orders_with_category):
    assert orders_with_category["category"].nunique() == 6

def test_electronics_dominates(orders_with_category):
    cat_rev = orders_with_category.groupby("category")["revenue"].sum()
    electronics_share = cat_rev["Electronics"] / cat_rev.sum()
    assert electronics_share > 0.40  # Electronics > 40% of revenue