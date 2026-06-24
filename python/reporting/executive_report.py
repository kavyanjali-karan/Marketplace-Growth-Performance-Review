import pandas as pd


def generate(df):

    return df.groupby("month")["revenue"].sum()