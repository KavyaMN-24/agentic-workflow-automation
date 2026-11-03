import json

from app.tools.sales_analyzer import analyze_sales


if __name__ == "__main__":
    results = analyze_sales("data/sample/sales.csv")

    print("\nBUSINESS SALES ANALYSIS")
    print("=" * 40)
    print(json.dumps(results, indent=4))