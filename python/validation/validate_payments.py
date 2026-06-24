def validate(df):

    assert (df["payment_value"]>=0).all()