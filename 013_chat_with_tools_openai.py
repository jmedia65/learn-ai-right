"""
CHAT WITH TOOLS - OPENAI VERSION

Same pattern as Anthropic, just different syntax.
Compare this file to the Anthropic version to see the differences.
"""

import os
from openai import OpenAI
from dotenv import load_dotenv
import json

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ============================================================================
# YOUR PYTHON FUNCTIONS (IDENTICAL TO ANTHROPIC VERSION)
# ============================================================================


def get_weather(location: str) -> dict:
    """Get weather for a location (fake data for demo)."""
    fake_weather_data = {
        "Miami": {"temp": 75, "condition": "Sunny", "humidity": 65},
        "New York": {"temp": 45, "condition": "Cloudy", "humidity": 70},
        "London": {"temp": 50, "condition": "Rainy", "humidity": 85},
    }
    return fake_weather_data.get(
        location, {"temp": 70, "condition": "Unknown", "humidity": 50}
    )


def add(a: float, b: float) -> float:
    """Add two numbers."""
    return a + b


def multiply(a: float, b: float) -> float:
    """Multiply two numbers."""
    return a * b


def get_user_info(user_id: str) -> dict:
    """Get user information from database (fake data for demo)."""
    fake_users = {
        "user_123": {"name": "Max", "age": 35, "city": "Miami"},
        "user_456": {"name": "Alex", "age": 28, "city": "New York"},
    }
    return fake_users.get(user_id, {"error": "User not found"})


# ============================================================================
# TOOL SCHEMAS (OpenAI format - DIFFERENT from Anthropic)
# ============================================================================

tools = [
    {
        "type": "function",  # ← OpenAI requires this wrapper
        "function": {
            "name": "get_weather",
            "description": "Get the current weather for a specific location. Returns temperature, condition, and humidity.",
            "parameters": {  # ← "parameters" not "input_schema"
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
            "name": "add",
            "description": "Add two numbers together.",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {"type": "number", "description": "First number"},
                    "b": {"type": "number", "description": "Second number"},
                },
                "required": ["a", "b"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "multiply",
            "description": "Multiply two numbers together.",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {"type": "number", "description": "First number"},
                    "b": {"type": "number", "description": "Second number"},
                },
                "required": ["a", "b"],
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
# TOOL ROUTER (IDENTICAL to Anthropic - same function!)
# ============================================================================


def execute_tool(tool_name: str, tool_input: dict):
    """Route tool calls to the correct Python function."""
    if tool_name == "get_weather":
        return get_weather(tool_input["location"])
    elif tool_name == "add":
        return add(tool_input["a"], tool_input["b"])
    elif tool_name == "multiply":
        return multiply(tool_input["a"], tool_input["b"])
    elif tool_name == "get_user_info":
        return get_user_info(tool_input["user_id"])
    else:
        return {"error": f"Unknown tool: {tool_name}"}


# ============================================================================
# CHAT WITH TOOLS (OpenAI version - DIFFERENT syntax)
# ============================================================================


def chat_with_tools(user_message: str, tools: list, conversation_history: list):
    """
    Handle a conversation with tool use - OpenAI version.

    This pattern:
    - Loops until GPT stops requesting tools
    - Executes tools as GPT requests them
    - Maintains conversation history
    - Returns GPT's final answer

    KEY DIFFERENCES FROM ANTHROPIC:
    - finish_reason instead of stop_reason
    - "tool_calls" instead of "tool_use"
    - function.arguments is a JSON STRING (must parse!)
    - role="tool" instead of role="user" with tool_result
    """

    # Add user message
    conversation_history.append({"role": "user", "content": user_message})

    # THE LOOP: loop until GPT stops using tools
    while True:
        response = client.chat.completions.create(
            model="gpt-4o",
            max_tokens=1024,
            tools=tools,
            messages=conversation_history,
        )

        # These two lines below could have been written:
        # if response.choices[0].finish_reason == "tool_calls":

        finish_reason = response.choices[0].finish_reason
        if finish_reason == "tool_calls":  # ← "tool_calls" not "tool_use"
            # GPT wants to use tools

            # Add GPT's message (includes tool calls)
            conversation_history.append(response.choices[0].message)

            # Execute all requested tools
            tool_calls = response.choices[0].message.tool_calls

            for tool_call in tool_calls:
                function_name = tool_call.function.name

                # CRITICAL: arguments is a JSON STRING!
                function_args = json.loads(tool_call.function.arguments)

                # Execute the tool
                result = execute_tool(function_name, function_args)

                # Add tool result with role="tool"
                conversation_history.append(
                    {
                        "role": "tool",  # ← Special "tool" role
                        "tool_call_id": tool_call.id,  # ← Must match
                        "content": json.dumps(result),
                    }
                )

        else:  # "stop" or "length"
            # GPT is done
            conversation_history.append(response.choices[0].message)
            return response.choices[0].message.content


# ============================================================================
# TEST THE FUNCTION
# ============================================================================

if __name__ == "__main__":
    print("=" * 80)
    print("TESTING CHAT WITH TOOLS - OPENAI VERSION")
    print("=" * 80)

    # Empty conversation history
    conversation_history = []

    # User's question (requires 2 tool calls)
    user_message = "Get info for user_123 and tell me about their city's weather"

    print(f"\nUser: {user_message}\n")
    print("GPT is thinking and using tools...\n")

    # Call the function
    response = chat_with_tools(user_message, tools, conversation_history)

    print("=" * 80)
    print("GPT'S FINAL ANSWER:")
    print("=" * 80)
    print(response)
    print("\n")

    # Show conversation stats
    print("=" * 80)
    print("CONVERSATION STATS:")
    print("=" * 80)
    print(f"Total messages in history: {len(conversation_history)}")
    print("\nMessage breakdown:")
    for i, msg in enumerate(conversation_history, 1):
        # OpenAI messages have different structure
        role = msg.role.upper() if hasattr(msg, "role") else msg["role"].upper()

        # Get content description
        if hasattr(msg, "content"):
            content = msg.content
        elif "content" in msg:
            content = msg["content"]
        else:
            content = None

        if content:
            if isinstance(content, str):
                content_desc = f'"{content[:50]}..."'
            else:
                content_desc = "[complex content]"
        elif hasattr(msg, "tool_calls"):
            content_desc = f"[{len(msg.tool_calls)} tool calls]"
        else:
            content_desc = "[tool result]"

        print(f"  {i}. {role:10} - {content_desc}")
