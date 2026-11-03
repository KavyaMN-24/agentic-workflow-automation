import json

from app.agent.registry_setup import build_registry

registry = build_registry()

result = registry.execute(
    "analyze_sales",
    {"file_path": "data/sample/sales.csv"},
)

print("AGENT TOOL EXECUTION")
print("=" * 40)
print(json.dumps(result, indent=4))