import numpy as np
import pandas as pd


def clean_transactions(df):
    df = df.copy()
    df = df.drop_duplicates(subset="transaction_id", keep="first")
    df["region"] = df["region"].astype(str).str.strip().str.title()
    amount = (df["amount"].astype(str)
                          .str.replace("$", "", regex=False)
                          .str.replace(",", "", regex=False)
                          .str.strip())
    df["amount"] = pd.to_numeric(amount, errors="coerce")
    df = df.dropna(subset=["amount"])
    return df.reset_index(drop=True)


def region_summary(df):
    clean = clean_transactions(df)
    regions = sorted(clean["region"].unique())
    completed = clean[clean["status"] == "completed"]
    agg = completed.groupby("region")["amount"].agg(total="sum", cnt="count")
    out = pd.DataFrame({"region": regions}).merge(
        agg, left_on="region", right_index=True, how="left")
    out["total_amount"] = out["total"].fillna(0.0).round(2)
    out["transaction_count"] = out["cnt"].fillna(0).astype(int)
    out["average_amount"] = np.where(
        out["transaction_count"] > 0,
        (out["total_amount"] / out["transaction_count"].replace(0, 1)).round(2),
        0.0)
    return out[["region", "total_amount", "transaction_count",
                "average_amount"]].reset_index(drop=True)
