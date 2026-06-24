def test_customer_unique(df):

    assert df.customer_id.duplicated().sum()==0