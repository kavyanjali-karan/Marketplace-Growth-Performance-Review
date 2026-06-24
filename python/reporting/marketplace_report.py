import pandas as pd


def marketplace(df):

    return df.groupby("category")["revenue"].sum()