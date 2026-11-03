
from pathlib import Path

import pandas as pd

REQUIRED_COLUMNS = {
    "product",
    "region",
    "units_sold",
    "unit_price",
}


def analyze_sales(file_path: str) -> dict:
    """Analyze a sales CSV and return business performance metrics."""

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"Sales file not found: {path}")

    if path.suffix.lower() != ".csv":
        raise ValueError("Only CSV files are supported.")

    df = pd.read_csv(path)

    missing_columns = REQUIRED_COLUMNS - set(df.columns)

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {sorted(missing_columns)}"
        )

    if df.empty:
        raise ValueError("Sales file contains no records.")

    for column in ["units_sold", "unit_price"]:
        df[column] = pd.to_numeric(df[column], errors="coerce")

    if df[["units_sold", "unit_price"]].isna().any().any():
        raise ValueError("Sales quantities and prices must be numeric.")

    if (df["units_sold"] < 0).any():
        raise ValueError("Units sold cannot be negative.")

    if (df["unit_price"] < 0).any():
        raise ValueError("Unit prices cannot be negative.")

    df["revenue"] = df["units_sold"] * df["unit_price"]

    product_revenue = (
        df.groupby("product")["revenue"]
        .sum()
        .sort_values(ascending=False)
    )

    region_revenue = (
        df.groupby("region")["revenue"]
        .sum()
        .sort_values(ascending=False)
    )

    return {
        "total_revenue": round(float(df["revenue"].sum()), 2),
        "total_units_sold": int(df["units_sold"].sum()),
        "transaction_count": len(df),
        "best_performing_product": str(product_revenue.index[0]),
        "best_performing_region": str(region_revenue.index[0]),
        "revenue_by_product": {
            str(k): round(float(v), 2)
            for k, v in product_revenue.items()
        },
        "revenue_by_region": {
            str(k): round(float(v), 2)
            for k, v in region_revenue.items()
        },
    }
