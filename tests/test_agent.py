import pytest

from app.agent.agent import BusinessWorkflowAgent


def test_agent_initializes():
    agent = BusinessWorkflowAgent()

    assert agent.client is not None
    assert agent.registry is not None
    assert agent.registry.get("analyze_sales") is not None





def test_agent_rejects_file_outside_sample_directory():
    agent = BusinessWorkflowAgent()

    arguments = {
        "file_path": "../.env"
    }

    with pytest.raises(ValueError, match="restricted"):
        agent._validate_file_path(arguments)

def test_agent_rejects_absolute_path_outside_sample_directory():
    agent = BusinessWorkflowAgent()

    arguments = {
        "file_path": str(
            __import__("pathlib").Path.cwd() / ".env"
        )
    }

    with pytest.raises(ValueError, match="restricted"):
        agent._validate_file_path(arguments)