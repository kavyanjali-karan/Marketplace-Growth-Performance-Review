def validate(df):

    assert df["product_id"].duplicated().sum()==0