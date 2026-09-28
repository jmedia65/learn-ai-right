"""
TOOL CALLING - OPENAI GPT (Responses API)

Same core concept as Anthropic:
AI decides -> You execute -> Return results -> AI responds.
"""

import os
from openai import OpenAI
from dotenv import load_dotenv
import json

load_dotenv()
MODEL = os.getenv("OPENAI_MODEL", "gpt-6-luna")
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# =============================================================================
# STEP 1: YOUR PYTHON FUNCTIONS
# =============================================================================


def get_weather(location: str) -> dict:
    """Get weather for a location."""
    fake_weather_data = {
        "Miami": {"temp": 75, "condition": "Sunny", "humidity": 65},
        "New York": {"temp": 45, "condition": "Cloudy", "humidity": 70},
        "London": {"temp": 50, "condition": "Rainy", "humidity": 85},
    }
    return fake_weather_data.get(
        location, {"temp": 70, "condition": "Unknown", "humidity": 50}
    )


def get_user_info(user_id: str) -> dict:
    """Get user information from database."""
    fake_users = {
        "user_123": {"name": "Max", "age": 35, "city": "Miami"},
        "user_456": {"name": "Alex", "age": 28, "city": "New York"},
    }
    return fake_users.get(user_id, {"error": "User not found"})


# =============================================================================
# STEP 2: TOOL SCHEMAS (Responses API format)
# =============================================================================

tools = [
    {
        "type": "function",
        "name": "get_weather",
        "strict": True,
        "description": "Get the current weather for a specific location. Returns temperature, condition, and humidity.",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "The city name, e.g., 'Miami' or 'New York'",
                }
            },
            "required": ["location"],
            "additionalProperties": False,
        },
    },
    {
        "type": "function",
        "name": "get_user_info",
        "strict": True,
        "description": "Get information about a user by their user ID.",
        "parameters": {
            "type": "object",
            "properties": {
                "user_id": {
                    "type": "string",
                    "description": "The user's ID, e.g., 'user_123'",
                }
            },
            "required": ["user_id"],
            "additionalProperties": False,
        },
    },
]


# =============================================================================
# STEP 3: TOOL ROUTER
# =============================================================================


def execute_tool(tool_name: str, tool_input: dict):
    """Route tool calls to the correct Python function."""
    if not isinstance(tool_input, dict):
        return {"error": "Tool input must be an object"}
    if tool_name == "get_weather":
        location = tool_input.get("location")
        if not isinstance(location, str):
            return {"error": "location must be a string"}
        return get_weather(location)
    if tool_name == "get_user_info":
        user_id = tool_input.get("user_id")
        if not isinstance(user_id, str):
            return {"error": "user_id must be a string"}
        return get_user_info(user_id)
    return {"error": f"Unknown tool: {tool_name}"}


# =============================================================================
# STEP 4: CHAT WITH TOOLS LOOP (Responses API)
# =============================================================================


def chat_with_tools(user_message: str, tools: list):
    """
    Handle tool use with Responses API.

    Loop:
    1. Send user message + tools
    2. If model emits function_call items, execute them
    3. Send function_call_output items back
    4. Repeat until final text response
    """
    print(f"\n{'='*80}")
    print(f"USER: {user_message}")
    print(f"{'='*80}\n")

    iteration = 0
    response = client.responses.create(
        model=MODEL,
        tools=tools,
        input=user_message,
    )

    while iteration < 5:
        iteration += 1

        if response.status != "completed":
            raise RuntimeError(f"Response did not complete: {response.status}")

        # Responses can include multiple output item types.
        # We care about function_call items during the tool loop.
        function_calls = [item for item in response.output if item.type == "function_call"]

        if function_calls:
            print(f"🔄 ITERATION {iteration}: GPT wants to use tools")

            tool_outputs = []
            for call in function_calls:
                function_name = call.name

                # Arguments arrive as a JSON string
                try:
                    function_args = json.loads(call.arguments)
                except json.JSONDecodeError:
                    function_args = {}

                print(f"   📞 Calling: {function_name}({json.dumps(function_args)})")

                result = execute_tool(function_name, function_args)

                print(f"   ✅ Result: {json.dumps(result)}\n")

                tool_outputs.append(
                    {
                        "type": "function_call_output",
                        "call_id": call.call_id,
                        "output": json.dumps(result),
                    }
                )

            # Continue the same reasoning thread using previous_response_id
            response = client.responses.create(
                model=MODEL,
                tools=tools,
                input=tool_outputs,
                previous_response_id=response.id,
            )

        else:
            print(f"✨ ITERATION {iteration}: GPT has final answer\n")

            final_answer = response.output_text

            print(f"{'='*80}")
            print("GPT'S FINAL ANSWER:")
            print(f"{'='*80}")
            print(final_answer)
            print(f"{'='*80}\n")

            return final_answer

    raise RuntimeError("Tool call limit reached before a final answer")


# =============================================================================
# USAGE EXAMPLE
# =============================================================================

chat_with_tools(
    "Get info for user_123 and tell me about their city's weather",
    tools,
)

"""
WHAT YOU JUST LEARNED:

1. Tool calling with Responses API
   - Model emits function_call items
   - You execute Python functions
   - You send back function_call_output items

2. previous_response_id keeps the chain connected
   - Each follow-up call continues the same reasoning thread
   - You don't need to resend the original user message every iteration

3. The pattern is still identical to Anthropic
   - Define tools
   - AI decides what to call
   - You execute and return results
   - Repeat until final answer

NEXT STEP: Learn RAG (making AI answer from your documents)
"""
