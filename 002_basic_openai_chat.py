"""
OPENAI BASICS: Your first GPT API call

Notice how similar this is to Anthropic? That's intentional.
Once you learn one, the other is easy.

Key differences from Anthropic:
1. Uses chat.completions.create() instead of messages.create()
2. Response structure is slightly different
3. Token counting works differently

But the core concept is identical: send messages, get response.
"""

import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Create the OpenAI client
# This uses your OPENAI_API_KEY from environment variables
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Make your first API call
# Notice: nearly identical to Anthropic, just different method name
response = client.chat.completions.create(
    # Model selection
    # gpt-4o is the latest, smartest model (similar to Claude Sonnet)
    # gpt-4o-mini is faster/cheaper (similar to Claude Haiku)
    model="gpt-4o",
    # Maximum tokens in the response
    max_tokens=1024,
    # Messages array - same structure as Anthropic!
    # Each message needs "role" and "content"
    messages=[{"role": "user", "content": "Explain what an API is in one sentence."}],
)

# Get the response text
# OpenAI structure: response.choices[0].message.content
# (Slightly different from Anthropic's response.content[0].text)
print("=" * 80)
print("GPT'S RESPONSE:")
print("=" * 80)
print(response.choices[0].message.content)
print("=" * 80)

# Response metadata
print("\nRESPONSE METADATA:")
print(f"Model used: {response.model}")
print(
    f"Finish reason: {response.choices[0].finish_reason}"
)  # Usually "stop" for normal completion
print(f"Input tokens (prompt): {response.usage.prompt_tokens}")
print(f"Output tokens (completion): {response.usage.completion_tokens}")
print(f"Total tokens: {response.usage.total_tokens}")
print(
    f"Total cost (approx): ${(response.usage.prompt_tokens * 0.0000025 + response.usage.completion_tokens * 0.00001):.6f}"
)

"""
KEY DIFFERENCES FROM ANTHROPIC:

1. METHOD NAMES:
   - Anthropic: client.messages.create()
   - OpenAI: client.chat.completions.create()

2. RESPONSE STRUCTURE:
   - Anthropic: response.content[0].text
   - OpenAI: response.choices[0].message.content

3. TOKEN USAGE:
   - Anthropic: response.usage.input_tokens / output_tokens
   - OpenAI: response.usage.prompt_tokens / completion_tokens

4. STOP REASON:
   - Anthropic: response.stop_reason (values: "end_turn", "max_tokens", "stop_sequence")
   - OpenAI: response.choices[0].finish_reason (values: "stop", "length", "content_filter")

But the CORE CONCEPT is identical: send messages array, get response back.

NEXT STEPS:
- Compare responses from Claude vs GPT on the same prompt
- Try different models (gpt-4o, gpt-4o-mini, gpt-3.5-turbo)
- Experiment with max_tokens
- Read the response structure: https://platform.openai.com/docs/api-reference/chat
"""
