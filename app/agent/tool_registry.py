
from collections.abc import Callable
from typing import Any

from pydantic import BaseModel, ValidationError


class Tool:
    """Represents a callable agent tool."""

    def __init__(
        self,
        name: str,
        description: str,
        args_schema: type[BaseModel],
        function: Callable[..., Any],
    ):
        self.name = name
        self.description = description
        self.args_schema = args_schema
        self.function = function

    def execute(self, arguments: dict) -> Any:
        """Validate arguments and execute the tool."""

        try:
            validated = self.args_schema.model_validate(arguments)
            return self.function(**validated.model_dump())
        except ValidationError as exc:
            raise ValueError(
                f"Invalid arguments for tool '{self.name}': {exc}"
            ) from exc


class ToolRegistry:
    """Stores and manages available agent tools."""

    def __init__(self):
        self._tools: dict[str, Tool] = {}

    def register(self, tool: Tool) -> None:
        if tool.name in self._tools:
            raise ValueError(f"Tool already registered: {tool.name}")

        self._tools[tool.name] = tool

    def get(self, name: str) -> Tool:
        if name not in self._tools:
            raise ValueError(f"Unknown tool: {name}")

        return self._tools[name]

    def list_tools(self) -> list[dict]:
        return [
            {
                "name": tool.name,
                "description": tool.description,
                "parameters": tool.args_schema.model_json_schema(),
            }
            for tool in self._tools.values()
        ]

    def execute(self, name: str, arguments: dict) -> Any:
        tool = self.get(name)
        return tool.execute(arguments)
