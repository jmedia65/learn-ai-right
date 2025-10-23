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

# Step 1: Initialize the client
# This sets up authentication with Anthropic's API
client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# Step 2: Call the API
# Send a messages array to Claude
response = client.messages.create(
    model="claude-sonnet-4-20250514",  # Which AI model to use
    max_tokens=1024,  # Maximum length of response (~750-1000 words)
    messages=[
        {
            "role": "user",  # Who is speaking (user or assistant)
            "content": "Explain what an API is in one sentence.",  # What you're asking
        }
    ],
)

# Step 3: Extract the response
# The actual text is nested in response.content[0].text
answer = response.content[0].text

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
   - response.content[0].text = the actual response
   - response.model = which model was used
   - response.usage = token counts for billing

3. This pattern works for ANY AI interaction
   - Single questions (like this)
   - Multi-turn conversations (coming next)
   - Tool calling, RAG, agents (all built on this foundation)

NEXT STEP: Learn how to add conversation memory (it's just a list!)
"""
