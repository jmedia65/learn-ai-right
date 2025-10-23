"""
YOUR FIRST AI CALL - OPENAI GPT

This is the same foundational pattern as Anthropic, with slightly different syntax.
Three steps: initialize → call → extract.

Compare this with 01_anthropic_basic.py to see the similarities and differences.
"""

import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
# This is where your API keys are stored
load_dotenv()

# Step 1: Initialize the client
# This sets up authentication with OpenAI's API
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Step 2: Call the API
# Send a messages array to GPT
response = client.chat.completions.create(
    model="gpt-4o",                    # Which AI model to use
    max_tokens=1024,                   # Maximum length of response (~750-1000 words)
    messages=[
        {
            "role": "user",            # Who is speaking (user or assistant)
            "content": "Explain what an API is in one sentence."  # What you're asking
        }
    ],
)

# Step 3: Extract the response
# For OpenAI, the text is in response.choices[0].message.content
answer = response.choices[0].message.content

# Display the AI's response
print("=" * 80)
print("GPT'S RESPONSE:")
print("=" * 80)
print(answer)
print("=" * 80)

# Display metadata about the API call
# This information helps you track costs and debug issues
print("\nRESPONSE METADATA:")
print(f"Model used: {response.model}")                           # Confirms which model answered
print(f"Finish reason: {response.choices[0].finish_reason}")    # Why the response ended (usually "stop")
print(f"Input tokens: {response.usage.prompt_tokens}")          # Tokens in your prompt
print(f"Output tokens: {response.usage.completion_tokens}")     # Tokens in GPT's response
print(f"Total tokens: {response.usage.total_tokens}")           # Sum of input + output

"""
WHAT YOU JUST LEARNED:

1. OpenAI uses almost the same pattern as Anthropic
   - Same messages array structure
   - Same role/content format
   - Just different method names and response paths

2. Key differences from Anthropic:
   - Method: client.chat.completions.create() vs client.messages.create()
   - Response path: response.choices[0].message.content vs response.content[0].text
   - Token names: prompt_tokens/completion_tokens vs input_tokens/output_tokens

3. The CONCEPT is identical
   - Send messages array
   - Get response object
   - Extract the text

NEXT STEP: Learn how to add conversation memory (it's just a list!)
"""
