import pandas as pd


def seller(df):

    return df.groupby("seller_state")["revenue"].sum()