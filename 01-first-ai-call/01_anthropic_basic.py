"""
YOUR FIRST AI CALL - ANTHROPIC CLAUDE

This is the foundational pattern for all AI applications.
Three steps: initialize → call → extract.

Everything else builds on this.
"""

import os
from anthropic import Anthropic
from dotenv import load_dotenv

# Load environment variables from .env file
# This is where your API keys are stored
load_dotenv()
MODEL = os.getenv("ANTHROPIC_MODEL", "claude-sonnet-5-5")

# Step 1: Initialize the client
# This sets up authentication with Anthropic's API
client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# Step 2: Call the API
# Send a messages array to Claude
response = client.messages.create(
    model=MODEL,  # Which AI model to use
    max_tokens=4096,  # Includes any thinking tokens and the visible answer
    messages=[
        {
            "role": "user",  # Who is speaking (user or assistant)
            "content": "Explain what an API is in one sentence.",  # What you're asking
        }
    ],
)

# Step 3: Extract the response
# A response can start with a thinking block, so select text blocks by type.
if response.stop_reason != "end_turn":
    raise RuntimeError(f"Claude did not finish its answer: {response.stop_reason}")
answer = "".join(block.text for block in response.content if block.type == "text")
if not answer:
    raise RuntimeError("Claude returned no text")

# Display the AI's response
print("=" * 80)
print("CLAUDE'S RESPONSE:")
print("=" * 80)
print(answer)
print("=" * 80)

# Display metadata about the API call
# This information helps you track costs and debug issues
print("\nRESPONSE METADATA:")
print(f"Model used: {response.model}")  # Confirms which model answered
print(
    f"Stop reason: {response.stop_reason}"
)  # Why the response ended (usually "end_turn")
print(f"Input tokens: {response.usage.input_tokens}")  # Tokens in your prompt
print(f"Output tokens: {response.usage.output_tokens}")  # Tokens in Claude's response

"""
WHAT YOU JUST LEARNED:

1. The messages array is the core of every AI call
   - Each message has a "role" (user or assistant)
   - And "content" (the actual text)

2. The response object contains more than just the answer
   - response.content contains blocks; select the text blocks for the answer
   - response.model = which model was used
   - response.usage = token counts for billing

3. This pattern works for ANY AI interaction
   - Single questions (like this)
   - Multi-turn conversations (coming next)
   - Tool calling, RAG, agents (all built on this foundation)

NEXT STEP: Learn how to add conversation memory (it's just a list!)
"""
