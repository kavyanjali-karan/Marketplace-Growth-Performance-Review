"""Rewrite every file in outputs/ from the raw data.

The outputs/ folder mirrors the Power BI report exports. They are derived,
not hand-made: run this script after data/generate_data.py and the CSVs
will match the data exactly.

Usage:
    python python/reporting/export_outputs.py
Output:
    outputs/*.csv
"""

from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "data" / "raw"
OUT = ROOT / "outputs"


def main() -> None:
    OUT.mkdir(exist_ok=True)

    orders = pd.read_csv(RAW / "orders.csv", parse_dates=["order_date"])
    customers = pd.read_csv(RAW / "customers.csv")
    products = pd.read_csv(RAW / "products.csv")
    sellers = pd.read_csv(RAW / "sellers.csv")

    # market_overview.csv - row counts behind the overview card
    overview = pd.DataFrame(
        [
            {
                "Count of order_id": len(orders),
                "Count of seller_key": orders["seller_id"].nunique(),
                "Count of product_key": orders["product_id"].nunique(),
                "Count of customer_key": orders["customer_id"].nunique(),
            }
        ]
    )
    overview.to_csv(OUT / "market_overview.csv", index=False, encoding="utf-8-sig")

    # customer_analysis.csv - orders per customer segment
    orders.merge(customers[["customer_id", "segment"]], on="customer_id") \
        .groupby("segment").size().rename("Count of order_id").reset_index() \
        .rename(columns={"segment": "segment"}) \
        [["segment", "Count of order_id"]] \
        .sort_values(["Count of order_id", "segment"], ascending=[False, True]) \
        .to_csv(OUT / "customer_analysis.csv", index=False, encoding="utf-8-sig")

    # product_analysis.csv - orders per product
    orders.merge(products[["product_id", "product_name"]], on="product_id") \
        .groupby("product_name").size().rename("Count of order_id").reset_index() \
        [["Count of order_id", "product_name"]] \
        .sort_values(["Count of order_id", "product_name"], ascending=[False, True]) \
        .to_csv(OUT / "product_analysis.csv", index=False, encoding="utf-8-sig")

    # seller_performance.csv - orders per seller (grouped by seller_id so
    # two sellers sharing a display name still count separately)
    seller_orders = (
        orders.groupby("seller_id").size().rename("Count of order_id").reset_index()
        .merge(sellers[["seller_id", "seller_name"]], on="seller_id")
        [["seller_name", "Count of order_id"]]
        .sort_values(["Count of order_id", "seller_name"], ascending=[False, True])
    )
    seller_orders.to_csv(OUT / "seller_performance.csv", index=False, encoding="utf-8-sig")

    # order_trends.csv - daily order volume with the date hierarchy
    trends = orders.groupby(orders["order_date"].dt.date).size().rename(
        "Count of order_id"
    ).reset_index().rename(columns={"order_date": "order_date"})
    trends["order_date"] = pd.to_datetime(trends["order_date"])
    trends.insert(0, "Day", trends["order_date"].dt.day)
    trends.insert(0, "Month", trends["order_date"].dt.month_name())
    trends.insert(0, "Quarter", trends["order_date"].dt.quarter.map(lambda q: f"Qtr {q}"))
    trends.insert(0, "Year", trends["order_date"].dt.year)
    trends.drop(columns=["order_date"])[
        ["Year", "Quarter", "Month", "Day", "Count of order_id"]
    ].to_csv(OUT / "order_trends.csv", index=False, encoding="utf-8-sig")

    for name in sorted(OUT.glob("*.csv")):
        rows = sum(1 for _ in name.open(encoding="utf-8-sig")) - 1
        print(f"OK {name.name} ({rows} rows)")
    print(f"\nAll outputs written to {OUT}")


if __name__ == "__main__":
    main()
