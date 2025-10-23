"""
CONVERSATION MEMORY - OPENAI GPT

This demonstrates the same conversation memory pattern as Anthropic.
The only difference is the API syntax - the concept is identical.

Memory = A Python list. That's it.
"""

import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# This is your "memory" - just a Python list
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
    # GPT sees the entire conversation, so it has "memory"
    response = client.chat.completions.create(
        model="gpt-4o",
        max_tokens=1024,
        messages=conversation_history,  # <-- The entire history every time
    )

    # Step 3: Extract GPT's response
    assistant_message = response.choices[0].message.content

    # Step 4: Display the response
    print(f"\nGPT: {assistant_message}")

    # Step 5: Add GPT's response to history
    # This ensures GPT sees its own previous responses in future turns
    conversation_history.append({"role": "assistant", "content": assistant_message})

    # The loop repeats! Back to Step 1 with an updated history

"""
WHAT YOU JUST LEARNED:

1. The pattern is identical to Anthropic
   - Same messages array structure
   - Same append-send-extract-append loop
   - Just different method names

2. The five-step loop that powers every chatbot:
   Step 1: Append user message to history
   Step 2: Send entire history to API
   Step 3: Extract the response
   Step 4: Display it to the user
   Step 5: Append assistant message to history

   Then repeat forever (or until user types "quit")

3. This works for ANY conversation-based AI application
   - Customer support bots
   - Coding assistants
   - Educational tutors
   - Whatever you want to build

4. Key insight: The AI sees EVERYTHING every time
   - The model doesn't maintain state
   - You maintain state (the history list)
   - You give the model its "memory" by sending the full context

NEXT STEP: Learn how to make AI take actions using tool calling
"""
