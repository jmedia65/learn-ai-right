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
    """Get weather for a location (fake data for demo)."""
    fake_weather_data = {
        "Miami": {"temp": 75, "condition": "Sunny", "humidity": 65},
        "New York": {"temp": 45, "condition": "Cloudy", "humidity": 70},
        "London": {"temp": 50, "condition": "Rainy", "humidity": 85},
    }

    weather = fake_weather_data.get(
        location, {"temp": 70, "condition": "Unknown", "humidity": 50}
    )
    return weather


def add(a: float, b: float) -> float:
    """Add two numbers."""
    return a + b


def multiply(a: float, b: float) -> float:
    """Multiply two numbers."""
    return a * b


def get_user_info(user_id: str) -> dict:
    """Get user information from database (fake for demo)."""
    fake_users = {
        "user_123": {"name": "Max", "age": 35, "city": "Miami"},
        "user_456": {"name": "Alex", "age": 28, "city": "New York"},
    }
    return fake_users.get(user_id, {"error": "User not found"})


# ============================================================================
# TOOL SCHEMAS (describe functions to Claude)
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
        "name": "add",
        "description": "Add two numbers together.",
        "input_schema": {
            "type": "object",
            "properties": {
                "a": {"type": "number", "description": "First number"},
                "b": {"type": "number", "description": "Second number"},
            },
            "required": ["a", "b"],
        },
    },
    {
        "name": "multiply",
        "description": "Multiply two numbers together.",
        "input_schema": {
            "type": "object",
            "properties": {
                "a": {"type": "number", "description": "First number"},
                "b": {"type": "number", "description": "Second number"},
            },
            "required": ["a", "b"],
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
# TOOL ROUTER (execute the actual functions)
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
# CHAT WITH TOOLS (production-ready pattern)
# ============================================================================


def chat_with_tools(user_message: str, tools: list, conversation_history: list):
    """
    Handle a conversation with tool use.

    This pattern:
    - Loops until Claude stops requesting tools
    - Executes tools as Claude requests them
    - Maintains conversation history
    - Returns Claude's final answer
    """

    # Add user message
    conversation_history.append({"role": "user", "content": user_message})

    # THE LOOP: loop until Claude stops using tools
    while True:
        response = client.messages.create(
            model="claude-4-sonnet-20250514",
            max_tokens=1024,
            tools=tools,
            messages=conversation_history,
        )

        if response.stop_reason == "tool_use":
            # Add assistant's tool request
            conversation_history.append(
                {"role": "assistant", "content": response.content}
            )

            # Execute tools and collect results
            tool_results = []
            for block in response.content:
                if block.type == "tool_use":
                    result = execute_tool(block.name, block.input)
                    tool_results.append(
                        {
                            "type": "tool_result",
                            "tool_use_id": block.id,
                            "content": json.dumps(result),
                        }
                    )

            # Add results
            conversation_history.append({"role": "user", "content": tool_results})

        else:  # end_turn or max_tokens
            # Claude is done
            conversation_history.append(
                {"role": "assistant", "content": response.content}
            )
            return response.content[0].text


# ============================================================================
# TEST THE FUNCTION
# ============================================================================

if __name__ == "__main__":
    print("=" * 80)
    print("TESTING CHAT WITH TOOLS")
    print("=" * 80)

    # Empty conversation history
    conversation_history = []

    # User's question (requires 2 tool calls)
    user_message = "Get info for user_123 and tell me about their city's weather"

    print(f"\nUser: {user_message}\n")
    print("Claude is thinking and using tools...\n")

    # Call the function
    response = chat_with_tools(user_message, tools, conversation_history)

    print("=" * 80)
    print("CLAUDE'S FINAL ANSWER:")
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
        role = msg["role"].upper()
        content_type = type(msg["content"]).__name__
        if isinstance(msg["content"], list):
            content_desc = f"[{len(msg['content'])} items]"
        elif isinstance(msg["content"], str):
            content_desc = f'"{msg["content"][:50]}..."'
        else:
            content_desc = "[complex content]"
        print(f"  {i}. {role:10} - {content_desc}")
