"""Pure data-loading and filtering helpers for the dashboard sample."""
from datetime import date
from pathlib import Path

import pandas as pd

DATA_PATH = Path(__file__).parent / "data" / "sales_sample.csv"


def load_sales_data(path: Path = DATA_PATH) -> pd.DataFrame:
    df = pd.read_csv(path, parse_dates=["date"])
    df["date"] = df["date"].dt.date
    return df


def filter_sales(
    df: pd.DataFrame,
    start_date: date,
    end_date: date,
    categories: list[str],
    regions: list[str],
) -> pd.DataFrame:
    mask = (df["date"] >= start_date) & (df["date"] <= end_date)
    if categories:
        mask &= df["category"].isin(categories)
    if regions:
        mask &= df["region"].isin(regions)
    return df[mask]
