
from pydantic import BaseModel, Field

from app.tools.sales_analyzer import analyze_sales


class SalesAnalysisInput(BaseModel):
    file_path: str = Field(
        description="Path to the sales CSV file."
    )


def analyze_sales_tool(file_path: str) -> dict:
    """Analyze a sales CSV and return business metrics."""

    return analyze_sales(file_path)
