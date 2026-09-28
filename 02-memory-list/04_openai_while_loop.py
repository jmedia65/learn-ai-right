"""
CONVERSATION MEMORY - OPENAI GPT (Interactive, Responses API)

This demonstrates the same conversation memory pattern as Anthropic.
The concept is identical: memory is still a Python list.
"""

import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
MODEL = os.getenv("OPENAI_MODEL", "gpt-6-luna")
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# This is your "memory" - a Python list of user messages and response items.
conversation_history = []

print("Chat with GPT! (Type 'quit' to exit)")
print("-" * 50)

# =============================================================================
# THE CHAT LOOP
# =============================================================================

while True:
    # Get user input
    user_input = input("\nYou: ")

    # Check if user wants to quit
    if user_input.lower() == "quit":
        print("Goodbye!")
        break

    # Step 1: Add user message to history
    conversation_history.append({"role": "user", "content": user_input})

    # Step 2: Send full history to GPT
    response = client.responses.create(
        model=MODEL,
        max_output_tokens=4096,
        input=conversation_history,
        store=False,
    )
    if response.status != "completed":
        raise RuntimeError(f"Response did not complete: {response.status}")

    # Step 3: Extract GPT's response
    assistant_message = response.output_text

    # Step 4: Display the response
    print(f"\nGPT: {assistant_message}")

    # Step 5: Keep all output items, including reasoning items, for the next turn
    conversation_history.extend(response.output)

    # The loop repeats! Back to Step 1 with an updated history

"""
WHAT YOU JUST LEARNED:

1. The pattern is identical to Anthropic
   - Same role/content history list
   - Same append-send-extract-append loop
   - Different SDK method: client.responses.create()

2. The five-step loop that powers every chatbot:
   Step 1: Append user message to history
   Step 2: Send entire history to API
   Step 3: Extract the response
   Step 4: Display it to the user
   Step 5: Append all assistant output items to history

3. This works for ANY conversation-based AI app
   - Customer support bots
   - Coding assistants
   - Educational tutors
   - Anything conversational

4. OpenAI also offers previous_response_id
   - Useful for stateful chains
   - But the list approach keeps the fundamentals explicit

NEXT STEP: Learn how to make AI take actions using tool calling
"""
