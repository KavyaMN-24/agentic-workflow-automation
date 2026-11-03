
import pandas as pd
import pytest

from app.tools.sales_analyzer import analyze_sales


def test_analyze_sales_returns_correct_metrics(tmp_path):
    csv_file = tmp_path / "sales.csv"

    df = pd.DataFrame({
        "product": ["Laptop", "Phone", "Phone"],
        "region": ["North", "South", "East"],
        "units_sold": [2, 3, 4],
        "unit_price": [100, 50, 50],
    })

    df.to_csv(csv_file, index=False)

    result = analyze_sales(str(csv_file))

    assert result["total_revenue"] == 550
    assert result["total_units_sold"] == 9
    assert result["transaction_count"] == 3
    assert result["best_performing_product"] == "Phone"
    assert result["best_performing_region"] == "East"


def test_missing_file_raises_error(tmp_path):
    with pytest.raises(FileNotFoundError):
        analyze_sales(str(tmp_path / "missing.csv"))


def test_non_csv_file_is_rejected(tmp_path):
    file_path = tmp_path / "sales.txt"
    file_path.write_text("some text")

    with pytest.raises(ValueError, match="Only CSV"):
        analyze_sales(str(file_path))


def test_missing_columns_are_rejected(tmp_path):
    csv_file = tmp_path / "sales.csv"
    pd.DataFrame({"product": ["Phone"]}).to_csv(csv_file, index=False)

    with pytest.raises(ValueError, match="Missing required columns"):
        analyze_sales(str(csv_file))


def test_empty_csv_is_rejected(tmp_path):
    csv_file = tmp_path / "sales.csv"
    pd.DataFrame(columns=[
        "product", "region", "units_sold", "unit_price"
    ]).to_csv(csv_file, index=False)

    with pytest.raises(ValueError, match="no records"):
        analyze_sales(str(csv_file))


def test_negative_units_are_rejected(tmp_path):
    csv_file = tmp_path / "sales.csv"
    pd.DataFrame({
        "product": ["Phone"],
        "region": ["North"],
        "units_sold": [-2],
        "unit_price": [50],
    }).to_csv(csv_file, index=False)

    with pytest.raises(ValueError, match="cannot be negative"):
        analyze_sales(str(csv_file))


def test_negative_prices_are_rejected(tmp_path):
    csv_file = tmp_path / "sales.csv"
    pd.DataFrame({
        "product": ["Phone"],
        "region": ["North"],
        "units_sold": [2],
        "unit_price": [-50],
    }).to_csv(csv_file, index=False)

    with pytest.raises(ValueError, match="cannot be negative"):
        analyze_sales(str(csv_file))
