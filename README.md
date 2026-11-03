# Agentic Business Workflow Automation

An AI-powered business assistant that analyzes sales data and generates business reports using an AI agent.

## Features

- AI agent powered by Groq
- Sales data analysis using Python and Pandas
- Automatic revenue and performance calculations
- Tool calling through a registered tool system
- Human approval before simulated report delivery
- FastAPI backend
- Streamlit web interface
- Application logging
- Automated tests using Pytest

## Technology Stack

- Python
- Groq API
- FastAPI
- Streamlit
- Pandas
- Pydantic
- Pytest
- Ruff

## How It Works

1. A user submits a business request.
2. The AI agent understands the request.
3. The agent selects the appropriate registered tool.
4. The sales analysis tool processes the CSV data.
5. The agent generates a business report.
6. The CLI workflow requests human approval before simulated delivery.

## Sample Results

The included sample dataset contains 12 synthetic sales transactions.

- Total revenue: 48,550
- Total units sold: 95
- Transactions: 12
- Top product by revenue: Phone
- Top region by revenue: East

The dataset does not specify a currency.

## Run the Project

Install dependencies:

```powershell
python -m pip install -r requirements.txt
```

Start the API:

```powershell
python -m uvicorn app.api.main:app --reload
```

Open API documentation:

http://127.0.0.1:8000/docs

Start the frontend in another terminal:

```powershell
streamlit run streamlit_app.py
```

Run the agent:

```powershell
python run_agent.py
```

## Testing

Run automated tests:

```powershell
python -m pytest -v
```

Current result: 20 tests passing.

Run code quality checks:

```powershell
python -m ruff check app tests run_agent.py run_tool.py streamlit_app.py test_groq_config.py
```

## Safety

- The agent can only access registered tools.
- Tool inputs are validated.
- File access is restricted to sample data.
- Human approval is required for simulated report delivery.
- No actual emails are sent.
- The API generates reports without triggering delivery.
- AI-generated reports should be reviewed before business decisions.

## Project Status

Core agent, sales analysis, API, Streamlit interface, approval workflow, logging, tests, and lint checks are implemented.
