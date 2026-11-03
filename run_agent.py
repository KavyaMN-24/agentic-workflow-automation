from app.agent.agent import BusinessWorkflowAgent
from app.tools.report_sender import send_report

agent = BusinessWorkflowAgent()

request = (
    "Analyze the sales data in data/sample/sales.csv. "
    "Tell me which product and region performed best "
    "and summarize the overall business performance."
)

print("\nBUSINESS WORKFLOW AGENT")
print("=" * 50)

# Generate the business report
result = agent.run(request)

print("\nGENERATED BUSINESS REPORT")
print("=" * 50)
print(result)

# Request human approval before simulated delivery
print("\nREPORT DELIVERY")
print("=" * 50)

delivery_result = send_report(result)

print("\nDELIVERY STATUS")
print(delivery_result)