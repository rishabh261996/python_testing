import pandas as pd


def clean_transactions(df):
    df = df.drop_duplicates()
    df["region"] = df["region"].str.lower()
    return df


def region_summary(df):
    summary = df.groupby("region")["amount"].sum()
    return summary
