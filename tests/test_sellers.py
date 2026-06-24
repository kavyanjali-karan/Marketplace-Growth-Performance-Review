def test_sellers(df):

    assert df.seller_id.duplicated().sum()==0