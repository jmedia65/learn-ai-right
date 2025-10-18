###############################
# ANTHROPIC API TOOL CALLING
###############################

import os
from anthropic import Anthropic
from dotenv import load_dotenv
import json

load_dotenv()
client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# ============================================================================
# YOUR PYTHON FUNCTIONS
# ============================================================================


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


# ============================================================================
# TOOL SCHEMAS
# ============================================================================

tools = [
    {
        "name": "get_weather",
        "description": "Get the current weather for a specific location. Returns temperature, condition, and humidity.",
        "input_schema": {
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
    {
        "name": "get_user_info",
        "description": "Get information about a user by their user ID.",
        "input_schema": {
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
]

# ============================================================================
# TOOL ROUTER
# ============================================================================


def execute_tool(tool_name: str, tool_input: dict):
    """Route tool calls to the correct Python function."""
    if tool_name == "get_weather":
        return get_weather(tool_input["location"])
    elif tool_name == "get_user_info":
        return get_user_info(tool_input["user_id"])
    else:
        return {"error": f"Unknown tool: {tool_name}"}


# ============================================================================
# CHAT WITH TOOLS (with visibility)
# ============================================================================


def chat_with_tools(user_message: str, tools: list, conversation_history: list):
    """
    Handle a conversation with tool use.

    Returns Claude's final answer after executing all necessary tools.
    """
    print(f"\n{'='*80}")
    print(f"USER: {user_message}")
    print(f"{'='*80}\n")

    # Add user message
    conversation_history.append({"role": "user", "content": user_message})

    iteration = 0
    # Loop until Claude stops using tools
    while True:
        iteration += 1
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1024,
            tools=tools,
            messages=conversation_history,
        )

        if response.stop_reason == "tool_use":
            print(f"🔄 ITERATION {iteration}: Claude wants to use tools")

            # Add Claude's tool request to history
            conversation_history.append(
                {"role": "assistant", "content": response.content}
            )

            # Execute tools and collect results
            tool_results = []
            for block in response.content:
                if block.type == "tool_use":
                    print(f"   📞 Calling: {block.name}({json.dumps(block.input)})")
                    result = execute_tool(block.name, block.input)
                    print(f"   ✅ Result: {json.dumps(result)}\n")
                    tool_results.append(
                        {
                            "type": "tool_result",
                            "tool_use_id": block.id,
                            "content": json.dumps(result),
                        }
                    )

            # Add results to history
            conversation_history.append({"role": "user", "content": tool_results})

        else:  # "end_turn" or "max_tokens"
            # Claude is done
            print(f"✨ ITERATION {iteration}: Claude has final answer\n")
            conversation_history.append(
                {"role": "assistant", "content": response.content}
            )
            final_answer = response.content[0].text

            print(f"{'='*80}")
            print("CLAUDE'S FINAL ANSWER:")
            print(f"{'='*80}")
            print(final_answer)
            print(f"{'='*80}\n")

            return final_answer


# ============================================================================
# USAGE
# ============================================================================

conversation_history = []

chat_with_tools(
    "Get info for user_123 and tell me about their city's weather",
    tools,
    conversation_history,
)


###############################
# OPENAI API TOOL CALLING
###############################

import os
from openai import OpenAI
from dotenv import load_dotenv
import json

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ============================================================================
# YOUR PYTHON FUNCTIONS
# ============================================================================


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


# ============================================================================
# TOOL SCHEMAS (OpenAI format)
# ============================================================================

tools = [
    {
        "type": "function",  # OpenAI requires this wrapper
        "function": {
            "name": "get_weather",
            "description": "Get the current weather for a specific location. Returns temperature, condition, and humidity.",
            "parameters": {  # "parameters" not "input_schema"
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

# ============================================================================
# TOOL ROUTER
# ============================================================================


def execute_tool(tool_name: str, tool_input: dict):
    """Route tool calls to the correct Python function."""
    if tool_name == "get_weather":
        return get_weather(tool_input["location"])
    elif tool_name == "get_user_info":
        return get_user_info(tool_input["user_id"])
    else:
        return {"error": f"Unknown tool: {tool_name}"}


# ============================================================================
# CHAT WITH TOOLS (OpenAI version with visibility)
# ============================================================================


def chat_with_tools(user_message: str, tools: list, conversation_history: list):
    """
    Handle a conversation with tool use - OpenAI version.

    Returns GPT's final answer after executing all necessary tools.
    """
    print(f"\n{'='*80}")
    print(f"USER: {user_message}")
    print(f"{'='*80}\n")

    # Add user message
    conversation_history.append({"role": "user", "content": user_message})

    iteration = 0
    # Loop until GPT stops using tools
    while True:
        iteration += 1
        response = client.chat.completions.create(
            model="gpt-4o",
            max_tokens=1024,
            tools=tools,
            messages=conversation_history,
        )

        finish_reason = response.choices[0].finish_reason

        if finish_reason == "tool_calls":  # OpenAI uses "tool_calls" not "tool_use"
            print(f"🔄 ITERATION {iteration}: GPT wants to use tools")

            # Add GPT's message (includes tool calls)
            conversation_history.append(response.choices[0].message)

            # Execute all requested tools
            tool_calls = response.choices[0].message.tool_calls

            for tool_call in tool_calls:
                function_name = tool_call.function.name

                # CRITICAL: arguments is a JSON STRING, must parse!
                function_args = json.loads(tool_call.function.arguments)

                print(f"   📞 Calling: {function_name}({json.dumps(function_args)})")

                # Execute the tool
                result = execute_tool(function_name, function_args)

                print(f"   ✅ Result: {json.dumps(result)}\n")

                # Add tool result with role="tool"
                conversation_history.append(
                    {
                        "role": "tool",  # OpenAI uses special "tool" role
                        "tool_call_id": tool_call.id,
                        "content": json.dumps(result),
                    }
                )

        else:  # "stop" or "length"
            # GPT is done
            print(f"✨ ITERATION {iteration}: GPT has final answer\n")
            conversation_history.append(response.choices[0].message)
            final_answer = response.choices[0].message.content

            print(f"{'='*80}")
            print("GPT'S FINAL ANSWER:")
            print(f"{'='*80}")
            print(final_answer)
            print(f"{'='*80}\n")

            return final_answer


# ============================================================================
# USAGE
# ============================================================================

conversation_history = []

chat_with_tools(
    "Get info for user_123 and tell me about their city's weather",
    tools,
    conversation_history,
)
