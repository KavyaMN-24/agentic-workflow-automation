from app.agent.tool_registry import Tool, ToolRegistry
from app.tools.sales_tool import SalesAnalysisInput, analyze_sales_tool


def build_registry() -> ToolRegistry:
    registry = ToolRegistry()

    sales_tool = Tool(
        name="analyze_sales",
        description=(
            "Analyze a sales CSV file and return total revenue, "
            "units sold, and product and regional performance."
        ),
        args_schema=SalesAnalysisInput,
        function=analyze_sales_tool,
    )

    registry.register(sales_tool)

    return registry