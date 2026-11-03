

from fastapi import FastAPI, HTTPException
from groq import APIError
from pydantic import BaseModel, Field

from app.agent.agent import BusinessWorkflowAgent
from app.core.logger import logger

app = FastAPI(
    title="Agentic Business Workflow Automation",
    description="An LLM-powered business analysis and workflow automation agent.",
    version="1.0.0",
)


class WorkflowRequest(BaseModel):
    request: str = Field(min_length=5, max_length=2000)


class WorkflowResponse(BaseModel):
    report: str
    status: str


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.post("/workflow", response_model=WorkflowResponse)
def execute_workflow(payload: WorkflowRequest):
    try:
        logger.info("Received workflow request")

        agent = BusinessWorkflowAgent()
        report = agent.run(payload.request)

        logger.info("Workflow completed successfully")

        return WorkflowResponse(
            report=report,
            status="success",
        )

    except (APIError, ValueError, TypeError, OSError, RuntimeError):
        logger.exception("Workflow execution failed")
        raise HTTPException(
            status_code=500,
            detail="Workflow execution failed. Check application logs.",
        )
