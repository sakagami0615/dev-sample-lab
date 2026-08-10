from datetime import date

import pandas as pd

from samples.dashboard.app.dashboard_logic import filter_sales


def _sample_df():
    return pd.DataFrame(
        [
            {"date": date(2025, 2, 1), "category": "Electronics", "region": "East", "sales": 100, "profit": 10},
            {"date": date(2025, 2, 2), "category": "Clothing", "region": "West", "sales": 200, "profit": 20},
            {"date": date(2025, 3, 1), "category": "Electronics", "region": "West", "sales": 300, "profit": 30},
        ]
    )


def test_filter_sales_by_date_range():
    df = _sample_df()
    result = filter_sales(df, date(2025, 2, 1), date(2025, 2, 28), [], [])
    assert list(result["date"]) == [date(2025, 2, 1), date(2025, 2, 2)]


def test_filter_sales_by_category():
    df = _sample_df()
    result = filter_sales(df, date(2025, 2, 1), date(2025, 3, 31), ["Electronics"], [])
    assert set(result["category"]) == {"Electronics"}


def test_filter_sales_by_region():
    df = _sample_df()
    result = filter_sales(df, date(2025, 2, 1), date(2025, 3, 31), [], ["West"])
    assert set(result["region"]) == {"West"}


def test_filter_sales_empty_selection_means_no_filter():
    df = _sample_df()
    result = filter_sales(df, date(2025, 2, 1), date(2025, 3, 31), [], [])
    assert len(result) == 3
