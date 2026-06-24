def validate(df):

    assert df["customer_id"].isnull().sum()==0

    assert df["customer_id"].duplicated().sum()==0