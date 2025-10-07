"""
TOOL/FUNCTION CALLING: Make Claude DO things

This is THE game-changer. Instead of just chatting, Claude can:
- Check the weather
- Query your database
- Send emails
- Calculate complex math
- Search the web
- Anything you can code!

How it works:
1. You define tools (describe what functions you have)
2. Claude decides when to use them
3. Claude tells you which tool to call and with what parameters
4. You execute the function
5. You send results back to Claude
6. Claude uses results to answer the user

This is how AI agents work. No framework needed.
"""

import os
from anthropic import Anthropic
from dotenv import load_dotenv
import json

load_dotenv()
client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# ============================================================================
# print("=" * 80)
# print("EXAMPLE 1: SIMPLE TOOL - GET WEATHER")
# print("=" * 80)


# # STEP 1: Define your actual Python function
# def get_weather(location: str) -> dict:
#     """
#     This is YOUR function. It could call a real weather API.
#     For this demo, we'll return fake data.
#     """
#     # In production, you'd call a real API like OpenWeatherMap
#     fake_weather_data = {
#         "Miami": {"temp": 75, "condition": "Sunny", "humidity": 65},
#         "New York": {"temp": 45, "condition": "Cloudy", "humidity": 70},
#         "London": {"temp": 50, "condition": "Rainy", "humidity": 85},
#     }

#     weather = fake_weather_data.get(
#         location, {"temp": 70, "condition": "Unknown", "humidity": 50}
#     )
#     return weather


# # STEP 2: Define the tool schema (tell Claude about your function)
# tools = [
#     {
#         "name": "get_weather",
#         "description": "Get the current weather for a specific location. Returns temperature, condition, and humidity.",
#         "input_schema": {
#             "type": "object",
#             "properties": {
#                 "location": {
#                     "type": "string",
#                     "description": "The city name, e.g., 'Miami' or 'New York'",
#                 }
#             },
#             "required": ["location"],
#         },
#     }
# ]

# # STEP 3: Make the API call with tools
# print("\nUser asks: 'What's the weather in Miami?'\n")

# response = client.messages.create(
#     model="claude-sonnet-4-20250514",
#     max_tokens=1024,
#     tools=tools,  # Pass the tools to Claude
#     messages=[{"role": "user", "content": "What's the weather in Miami?"}],
# )

# print("Claude's response:")
# print(
#     f"Stop reason: {response.stop_reason}"
# )  # Will be "tool_use" if Claude wants to use a tool

# # STEP 4: Check if Claude wants to use a tool
# if response.stop_reason == "tool_use":
#     print("\n✓ Claude wants to use a tool!")

#     # Extract the tool use request
#     # response.content is a list, find the tool_use block
#     tool_use_block = None
#     for block in response.content:
#         if block.type == "tool_use":
#             tool_use_block = block
#             break

#     if tool_use_block:
#         print(f"\nTool requested: {tool_use_block.name}")
#         print(f"Tool parameters: {json.dumps(tool_use_block.input, indent=2)}")

#     # STEP 5: Execute YOUR function
#     location = tool_use_block.input["location"]
#     weather_result = get_weather(location)

#     print(f"\nExecuting get_weather('{location}')...")
#     print(f"Result: {json.dumps(weather_result, indent=2)}")

#     # STEP 6: Send the result back to Claude
#     print("\nSending result back to Claude...\n")

#     final_response = client.messages.create(
#         model="claude-sonnet-4-20250514",
#         max_tokens=1024,
#         tools=tools,
#         messages=[
#             {"role": "user", "content": "What's the weather in Miami?"},
#             {"role": "assistant", "content": response.content},  # Claude's tool request
#             {
#                 "role": "user",
#                 "content": [
#                     {
#                         "type": "tool_result",
#                         "tool_use_id": tool_use_block.id,  # Must match the tool_use id
#                         "content": json.dumps(weather_result),  # Your function's result
#                     }
#                 ],
#             },
#         ],
#     )

#     # STEP 7: Claude now has the data and can answer
#     print("Claude's final answer:")
#     print(final_response.content[0].text)

# ============================================================================
print("\n" + "=" * 80)
print("EXAMPLE 2: MULTIPLE TOOLS - CALCULATOR")
print("=" * 80)


# Define multiple Python functions
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


# Define tool schemas for ALL your functions
tools_multi = [
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

print("\nUser asks: 'What's 15 multiplied by 23?'\n")

response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    tools=tools_multi,
    messages=[{"role": "user", "content": "What's 15 multiplied by 23?"}],
)

# THIS IS THE KEY - THE IF STATEMENT
if response.stop_reason == "tool_use":
    print("✓ Claude wants to use a tool!")

    # Find the tool use block
    tool_use = next(block for block in response.content if block.type == "tool_use")

    print(f"\nTool: {tool_use.name}")
    print(f"Parameters: {json.dumps(tool_use.input, indent=2)}")

    # Execute the appropriate function
    if tool_use.name == "multiply":
        result = multiply(tool_use.input["a"], tool_use.input["b"])
    elif tool_use.name == "add":
        result = add(tool_use.input["a"], tool_use.input["b"])

    print(f"Result: {result}")

    # Send result back
    final_response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        tools=tools_multi,
        messages=[
            {"role": "user", "content": "What's 15 multiplied by 23?"},
            {"role": "assistant", "content": response.content},
            {
                "role": "user",
                "content": [
                    {
                        "type": "tool_result",
                        "tool_use_id": tool_use.id,
                        "content": str(result),
                    }
                ],
            },
        ],
    )

    print(f"\nClaude's answer: {final_response.content[0].text}")
