def validate(df):

    assert df["order_id"].duplicated().sum()==0