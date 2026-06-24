def validate(df):

    assert df["seller_id"].duplicated().sum()==0