"""
CONVERSATION MEMORY - ANTHROPIC CLAUDE (Interactive Chat Loop)

Now let's take the pattern from 01_anthropic_conversation.py and make it interactive.
Instead of hardcoded turns, we'll use a while loop to chat with Claude in real-time.

This is the practical application of conversation memory.
"""

import os
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()
client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# This is your "memory" - just a Python list
conversation_history = []

print("Chat with Claude! (Type 'quit' to exit)")
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

    # Step 2: Send full history to Claude
    # Claude sees the entire conversation, so it has "memory"
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        messages=conversation_history  # <-- The entire history every time
    )

    # Step 3: Extract Claude's response
    assistant_message = response.content[0].text

    # Step 4: Display the response
    print(f"\nClaude: {assistant_message}")

    # Step 5: Add Claude's response to history
    # This ensures Claude sees its own previous responses in future turns
    conversation_history.append({"role": "assistant", "content": assistant_message})

    # The loop repeats! Back to Step 1 with an updated history

"""
WHAT YOU JUST LEARNED:

1. The five-step loop that powers every chatbot:
   Step 1: Append user message to history
   Step 2: Send entire history to API
   Step 3: Extract the response
   Step 4: Display it to the user
   Step 5: Append assistant message to history

   Then repeat forever (or until user types "quit")

2. This is the exact same pattern as 01_anthropic_conversation.py
   - Just wrapped in a while loop
   - Accepts user input instead of hardcoded messages
   - That's the only difference!

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
