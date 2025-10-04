"""
ANTHROPIC BASICS: Your first Claude API call

This is the foundation. Everything else builds on this pattern:
1. Import the client
2. Create a client instance
3. Call messages.create()
4. Get the response

That's it. No framework needed.
"""

import os
from anthropic import Anthropic
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Create the Anthropic client
# This uses your ANTHROPIC_API_KEY from environment variables
client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# Make your first API call
# This is THE fundamental pattern you'll use everywhere
response = client.messages.create(
    # Model selection - use the latest Sonnet for best results
    model="claude-4-sonnet-20250514",
    # Maximum tokens in the response (not the input)
    # Think of this as "max length of Claude's answer"
    max_tokens=1024,
    # Messages array - this is your conversation
    # Each message has a "role" (user or assistant) and "content" (the text)
    messages=[{"role": "user", "content": "Explain what an API is in one sentence."}],
)

# The response object contains everything Claude sent back
# Most importantly: response.content is a list of content blocks
# For simple text responses, it's usually just one text block at index [0]
print("=" * 80)
print("CLAUDE'S RESPONSE:")
print("=" * 80)
print(response.content[0].text)
print("=" * 80)

# Let's see what else is in the response object
print("\nRESPONSE METADATA:")
print(f"Model used: {response.model}")

print(
    f"Stop reason: {response.stop_reason}"
)  # Usually "end_turn" for normal completion
print(f"Input tokens: {response.usage.input_tokens}")
print(f"Output tokens: {response.usage.output_tokens}")
print(
    f"Total cost (approx): ${(response.usage.input_tokens * 0.000003 + response.usage.output_tokens * 0.000015):.6f}"
)

"""
KEY TAKEAWAYS:
1. The Anthropic SDK is just a thin wrapper around HTTP requests - nothing magic
2. messages.create() is synchronous - it waits for the full response
3. response.content[0].text gets you Claude's text answer
4. response.usage tells you token counts (important for cost tracking)
5. This pattern is the same whether you're building a chatbot, RAG system, or agent

NEXT STEPS:
- Try changing the prompt
- Try different models (claude-sonnet-4-20250514, claude-haiku-4-20250124)
- Try adjusting max_tokens
- Read the response structure in the docs: https://docs.anthropic.com/en/api/messages
"""
