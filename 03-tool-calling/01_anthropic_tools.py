"""
TOOL CALLING - ANTHROPIC CLAUDE

This demonstrates how "AI agents" actually work.
The AI doesn't execute code - it decides what to call, and YOU execute it.

Pattern: AI decides → You execute → Return results → AI responds
"""

import os
from anthropic import Anthropic
from dotenv import load_dotenv
import json

load_dotenv()
client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# =============================================================================
# STEP 1: YOUR PYTHON FUNCTIONS
# =============================================================================
# These are normal Python functions. The AI can't run them directly.


def get_weather(location: str) -> dict:
    """Get weather for a location."""
    # In production, this would call a real weather API
    # For this example, we use fake data
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
    # In production, this would query a real database
    fake_users = {
        "user_123": {"name": "Max", "age": 35, "city": "Miami"},
        "user_456": {"name": "Alex", "age": 28, "city": "New York"},
    }
    return fake_users.get(user_id, {"error": "User not found"})


# =============================================================================
# STEP 2: TOOL SCHEMAS
# =============================================================================
# These describe your functions to Claude in a format it understands

tools = [
    {
        "name": "get_weather",  # Must match your function name
        "description": "Get the current weather for a specific location. Returns temperature, condition, and humidity.",
        "input_schema": {  # Describes the parameters
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "The city name, e.g., 'Miami' or 'New York'",
                }
            },
            "required": ["location"],  # Which parameters are required
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

# =============================================================================
# STEP 3: TOOL ROUTER
# =============================================================================
# This function executes the actual Python code based on Claude's request


def execute_tool(tool_name: str, tool_input: dict):
    """Route tool calls to the correct Python function."""
    if tool_name == "get_weather":
        return get_weather(tool_input["location"])
    elif tool_name == "get_user_info":
        return get_user_info(tool_input["user_id"])
    else:
        return {"error": f"Unknown tool: {tool_name}"}


# =============================================================================
# STEP 4: CHAT WITH TOOLS LOOP
# =============================================================================


def chat_with_tools(user_message: str, tools: list, conversation_history: list):
    """
    Handle a conversation with tool use.

    This function shows the complete loop:
    1. Send message with available tools
    2. If Claude wants to use tools, execute them
    3. Return results to Claude
    4. Repeat until Claude has a final answer
    """
    print(f"\n{'='*80}")
    print(f"USER: {user_message}")
    print(f"{'='*80}\n")

    # Add user message to conversation history
    conversation_history.append({"role": "user", "content": user_message})

    iteration = 0

    # Loop until Claude stops using tools
    while True:
        iteration += 1

        # Call Claude with tools available
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1024,
            tools=tools,  # <-- Provide the tool schemas
            messages=conversation_history,
        )

        # Check if Claude wants to use tools
        if response.stop_reason == "tool_use":
            print(f"🔄 ITERATION {iteration}: Claude wants to use tools")

            # Add Claude's tool request to history
            # This contains both text and tool_use blocks
            conversation_history.append(
                {"role": "assistant", "content": response.content}
            )

            # Uncomment this if you want to print the full response.content
            # print(conversation_history)

            # Execute each tool Claude requested
            tool_results = []
            for block in response.content:
                if block.type == "tool_use":
                    print(f"   📞 Calling: {block.name}({json.dumps(block.input)})")

                    # YOU execute the actual Python function
                    result = execute_tool(block.name, block.input)

                    print(f"   ✅ Result: {json.dumps(result)}\n")

                    # Prepare result to send back to Claude
                    tool_results.append(
                        {
                            "type": "tool_result",
                            "tool_use_id": block.id,  # Links result to request
                            "content": json.dumps(result),
                        }
                    )

            # Add tool results to history as a user message
            conversation_history.append({"role": "user", "content": tool_results})

            # Loop continues - Claude will see the tool results

        else:  # stop_reason is "end_turn" or "max_tokens"
            # Claude has a final answer (no more tools needed)
            print(f"✨ ITERATION {iteration}: Claude has final answer\n")

            conversation_history.append(
                {"role": "assistant", "content": response.content}
            )

            # Uncomment this if you want to print the full response.content
            # print(conversation_history)

            # Extract the text response
            final_answer = response.content[0].text

            print(f"{'='*80}")
            print("CLAUDE'S FINAL ANSWER:")
            print(f"{'='*80}")
            print(final_answer)
            print(f"{'='*80}\n")

            return final_answer


# =============================================================================
# USAGE EXAMPLE
# =============================================================================

conversation_history = []

# Ask Claude to use multiple tools in sequence
chat_with_tools(
    "Get info for user_123 and tell me about their city's weather",
    tools,
    conversation_history,
)

"""
WHAT YOU JUST LEARNED:

1. The AI doesn't execute your code
   - Claude reads the tool schemas
   - Claude decides which tools to call
   - Claude specifies the exact parameters
   - BUT: YOU execute the actual Python function

2. Tool calling is a loop
   - Send message with available tools
   - If stop_reason == "tool_use", execute tools
   - Return results to Claude
   - Repeat until stop_reason == "end_turn"

3. Tool schemas are instructions
   - Name: What to call the function
   - Description: When to use it
   - Input schema: What parameters it needs

4. This is how ALL AI agents work
   - LangChain agents? This pattern.
   - Custom workflow engines? This pattern.
   - Complex multi-agent systems? Sequential API calls with tool use.

NEXT STEP: Learn RAG (making AI answer from your documents)
"""
