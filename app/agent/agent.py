
import json
from pathlib import Path

from app.agent.registry_setup import build_registry
from app.core.config import GROQ_MODEL
from app.core.llm_client import get_groq_client
from app.core.logger import logger

MAX_TOOL_ROUNDS = 3


class BusinessWorkflowAgent:
    def __init__(self):
        self.client = get_groq_client()
        self.registry = build_registry()

        self.system_prompt = """
You are a business workflow assistant.

Understand the user's business request.
Use registered tools when data analysis is required.
Never invent numerical results.
Explain findings clearly and professionally.
Only use the tools provided to you.

Do not assume or invent a currency symbol.
If the dataset does not specify a currency,
report monetary values without a currency symbol.
"""

    def _get_tool_definitions(self):
        registered_tools = self.registry.list_tools()

        return [
            {
                "type": "function",
                "function": {
                    "name": tool["name"],
                    "description": tool["description"],
                    "parameters": tool["parameters"],
                },
            }
            for tool in registered_tools
        ]

    def _validate_file_path(self, arguments):
        if "file_path" not in arguments:
            raise ValueError("Missing file_path argument.")

        sample_dir = Path("data/sample").resolve()
        requested_path = Path(arguments["file_path"])

        if not requested_path.is_absolute():
            requested_path = Path.cwd() / requested_path

        resolved_path = requested_path.resolve()

        if not resolved_path.is_relative_to(sample_dir):
            raise ValueError(
                "File access is restricted to the data/sample directory."
            )

        arguments["file_path"] = str(resolved_path)

    def run(self, user_request: str) -> str:
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": user_request},
        ]

        tools = self._get_tool_definitions()

        for _ in range(MAX_TOOL_ROUNDS):
            response = self.client.chat.completions.create(
                model=GROQ_MODEL,
                messages=messages,
                tools=tools,
                tool_choice="auto",
                parallel_tool_calls=False,
                temperature=0,
                max_completion_tokens=2048,
            )

            assistant_message = response.choices[0].message
            tool_calls = assistant_message.tool_calls

            if not tool_calls:
                return assistant_message.content or "No response generated."

            messages.append(
                assistant_message.model_dump(exclude_none=True)
            )

            for tool_call in tool_calls:
                tool_name = tool_call.function.name
                logger.info("Executing tool: %s", tool_call.function.name)
                try:
                    arguments = json.loads(
                        tool_call.function.arguments
                    )

                    if not isinstance(arguments, dict):
                        raise TypeError("Tool arguments must be an object.")

                    if tool_name == "analyze_sales":
                        self._validate_file_path(arguments)

                    result = self.registry.execute(
                        tool_name,
                        arguments,
                    )
                    logger.info("Tool executed successfully: %s", tool_name)

                    tool_result = {
                        "success": True,
                        "result": result,
                    }

                except (ValueError, TypeError, OSError) as error:
                    tool_result = {
                        "success": False,
                        "error": str(error),
                    }
                    logger.exception("Tool execution failed: %s", tool_name)

                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "name": tool_name,
                        "content": json.dumps(tool_result),
                    }
                )

        # After the tool-call limit, request a final response
        # without permitting additional tool calls.
        response = self.client.chat.completions.create(
            model=GROQ_MODEL,
            messages=messages,
            tools=tools,
            tool_choice="none",
            temperature=0,
            max_completion_tokens=2048,
        )

        return (
            response.choices[0].message.content
            or "The agent could not generate a final response."
        )
