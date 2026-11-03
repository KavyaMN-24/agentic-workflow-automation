
import pytest
from pydantic import BaseModel, Field

from app.agent.tool_registry import Tool, ToolRegistry


class AddInput(BaseModel):
    a: int = Field(description="First number")
    b: int = Field(description="Second number")


def add_numbers(a: int, b: int) -> int:
    return a + b


def create_registry():
    registry = ToolRegistry()

    registry.register(
        Tool(
            name="add_numbers",
            description="Add two numbers.",
            args_schema=AddInput,
            function=add_numbers,
        )
    )

    return registry


def test_register_and_list_tools():
    registry = create_registry()

    tools = registry.list_tools()

    assert len(tools) == 1
    assert tools[0]["name"] == "add_numbers"


def test_execute_registered_tool():
    registry = create_registry()

    result = registry.execute(
        "add_numbers",
        {"a": 10, "b": 20},
    )

    assert result == 30


def test_unknown_tool_is_rejected():
    registry = create_registry()

    with pytest.raises(ValueError, match="Unknown tool"):
        registry.execute("unknown_tool", {})


def test_invalid_arguments_are_rejected():
    registry = create_registry()

    with pytest.raises(ValueError, match="Invalid arguments"):
        registry.execute("add_numbers", {"a": "invalid"})


def test_duplicate_tool_registration_is_rejected():
    registry = create_registry()

    with pytest.raises(ValueError, match="already registered"):
        registry.register(
            Tool(
                name="add_numbers",
                description="Duplicate tool.",
                args_schema=AddInput,
                function=add_numbers,
            )
        )
