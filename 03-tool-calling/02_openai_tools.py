"""
TOOL CALLING - OPENAI GPT

This is the same tool calling pattern as Anthropic, with OpenAI-specific syntax.
The concept is identical: AI decides → You execute → Return results → AI responds
"""

import os
from openai import OpenAI
from dotenv import load_dotenv
import json

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# =============================================================================
# STEP 1: YOUR PYTHON FUNCTIONS
# =============================================================================
# Same functions as Anthropic example


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
# STEP 2: TOOL SCHEMAS (OpenAI Format)
# =============================================================================
# OpenAI uses a slightly different format than Anthropic

tools = [
    {
        "type": "function",  # OpenAI requires this wrapper
        "function": {
            "name": "get_weather",
            "description": "Get the current weather for a specific location. Returns temperature, condition, and humidity.",
            "parameters": {  # OpenAI uses "parameters" instead of "input_schema"
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The city name, e.g., 'Miami' or 'New York'",
                    }
                },
                "required": ["location"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_user_info",
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
            },
        },
    },
]

# =============================================================================
# STEP 3: TOOL ROUTER
# =============================================================================
# Same as Anthropic - executes the actual Python code


def execute_tool(tool_name: str, tool_input: dict):
    """Route tool calls to the correct Python function."""
    if tool_name == "get_weather":
        return get_weather(tool_input["location"])
    elif tool_name == "get_user_info":
        return get_user_info(tool_input["user_id"])
    else:
        return {"error": f"Unknown tool: {tool_name}"}


# =============================================================================
# STEP 4: CHAT WITH TOOLS LOOP (OpenAI Version)
# =============================================================================


def chat_with_tools(user_message: str, tools: list, conversation_history: list):
    """
    Handle a conversation with tool use - OpenAI version.

    Same pattern as Anthropic, different API details.
    """
    print(f"\n{'='*80}")
    print(f"USER: {user_message}")
    print(f"{'='*80}\n")

    # Add user message to history
    conversation_history.append({"role": "user", "content": user_message})

    iteration = 0

    # Loop until GPT stops using tools
    while True:
        iteration += 1

        # Call GPT with tools available
        response = client.chat.completions.create(
            model="gpt-4o",
            max_tokens=1024,
            tools=tools,  # <-- Provide the tool schemas
            messages=conversation_history,
        )

        finish_reason = response.choices[0].finish_reason

        # Check if GPT wants to use tools
        if finish_reason == "tool_calls":  # OpenAI uses "tool_calls" not "tool_use"
            print(f"🔄 ITERATION {iteration}: GPT wants to use tools")

            # Add GPT's message to history (includes tool call requests)
            conversation_history.append(response.choices[0].message)

            # Execute all requested tools
            tool_calls = response.choices[0].message.tool_calls

            for tool_call in tool_calls:
                function_name = tool_call.function.name

                # IMPORTANT: OpenAI returns arguments as a JSON STRING
                # You must parse it before using
                function_args = json.loads(tool_call.function.arguments)

                print(f"   📞 Calling: {function_name}({json.dumps(function_args)})")

                # YOU execute the actual Python function
                result = execute_tool(function_name, function_args)

                print(f"   ✅ Result: {json.dumps(result)}\n")

                # Add tool result to history
                # OpenAI uses a special "tool" role for results
                conversation_history.append(
                    {
                        "role": "tool",  # Special role for tool results
                        "tool_call_id": tool_call.id,  # Links result to request
                        "content": json.dumps(result),
                    }
                )

            # Loop continues - GPT will see the tool results

        else:  # finish_reason is "stop" or "length"
            # GPT has a final answer
            print(f"✨ ITERATION {iteration}: GPT has final answer\n")

            conversation_history.append(response.choices[0].message)
            final_answer = response.choices[0].message.content

            print(f"{'='*80}")
            print("GPT'S FINAL ANSWER:")
            print(f"{'='*80}")
            print(final_answer)
            print(f"{'='*80}\n")

            return final_answer


# =============================================================================
# USAGE EXAMPLE
# =============================================================================

conversation_history = []

# Ask GPT to use multiple tools in sequence
chat_with_tools(
    "Get info for user_123 and tell me about their city's weather",
    tools,
    conversation_history,
)

"""
WHAT YOU JUST LEARNED:

1. OpenAI vs Anthropic differences for tool calling:

   Schema format:
   - Anthropic: "input_schema"
   - OpenAI: "parameters" wrapped in "function" with "type": "function"

   Stop reasons:
   - Anthropic: stop_reason == "tool_use"
   - OpenAI: finish_reason == "tool_calls"

   Tool results:
   - Anthropic: Add as user message with type "tool_result"
   - OpenAI: Add with special role "tool"

   Arguments format:
   - Anthropic: Comes as a dict (block.input)
   - OpenAI: Comes as JSON string (must parse with json.loads())

2. The PATTERN is identical:
   - Define schemas
   - AI decides what to call
   - You execute the actual code
   - Return results
   - Loop until AI is done

3. This is how real AI systems work:
   - Customer support bots calling ticket systems
   - Code assistants running tests
   - Research agents searching databases
   - All the same pattern

NEXT STEP: Learn RAG (making AI answer from your documents)
"""
