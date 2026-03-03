"""
YOUR FIRST AI CALL - OPENAI GPT (RESPONSES API)

This is the same foundational pattern as Anthropic, using OpenAI's
recommended primary API for new projects: Responses.

Three steps: initialize -> call -> extract.
"""

import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
# This is where your API keys are stored
load_dotenv()

# Optional model override for experiments
MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1")

# Step 1: Initialize the client
# This sets up authentication with OpenAI's API
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Step 2: Call the API (Responses API)
# For simple text tasks, input can be a plain string
response = client.responses.create(
    model=MODEL,
    max_output_tokens=1024,  # Maximum length of response
    input="Explain what an API is in one sentence.",
)

# Step 3: Extract the response
# Responses API exposes a convenience field for final text
answer = response.output_text

# Display the AI's response
print("=" * 80)
print("GPT'S RESPONSE:")
print("=" * 80)
print(answer)
print("=" * 80)

# Display metadata about the API call
# This information helps you track costs and debug issues
print("\nRESPONSE METADATA:")
print(f"Response ID: {response.id}")
print(f"Model used: {response.model}")
print(f"Status: {response.status}")
if response.usage is not None:
    print(f"Input tokens: {response.usage.input_tokens}")
    print(f"Output tokens: {response.usage.output_tokens}")
    print(f"Total tokens: {response.usage.total_tokens}")

"""
WHAT YOU JUST LEARNED:

1. Responses is OpenAI's primary API for new projects
   - Method: client.responses.create()
   - For simple prompts, pass input as a string

2. The concept is still identical
   - Send input
   - Get response object
   - Extract text with response.output_text

3. The same core pattern still applies
   - Initialize client
   - Call model
   - Extract response

NEXT STEP: Learn how to add conversation memory (it's still just a list!)
"""
