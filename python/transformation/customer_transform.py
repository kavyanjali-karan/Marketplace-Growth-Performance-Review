def transform_customer(df):

    df.columns=df.columns.str.lower()

    df["customer_state"]=df["customer_state"].str.upper()

    return df