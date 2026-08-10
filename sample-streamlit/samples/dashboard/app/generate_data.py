"""Generate a reproducible sample sales CSV for the dashboard sample."""
import csv
import random
from datetime import date, timedelta
from pathlib import Path

CATEGORIES = ["Electronics", "Clothing", "Groceries"]
REGIONS = ["East", "West", "North"]
START_DATE = date(2025, 2, 1)
END_DATE = date(2025, 7, 31)
OUTPUT_PATH = Path(__file__).parent / "data" / "sales_sample.csv"


def generate_rows():
    random.seed(42)
    rows = []
    current = START_DATE
    while current <= END_DATE:
        for category in CATEGORIES:
            for region in REGIONS:
                sales = random.randint(1000, 50000)
                margin = random.uniform(0.05, 0.3)
                profit = round(sales * margin, 2)
                rows.append([current.isoformat(), category, region, sales, profit])
        current += timedelta(days=1)
    return rows


def main():
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    rows = generate_rows()
    with OUTPUT_PATH.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["date", "category", "region", "sales", "profit"])
        writer.writerows(rows)
    print(f"Wrote {len(rows)} rows to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
