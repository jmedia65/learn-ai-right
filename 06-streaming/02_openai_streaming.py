"""
STREAMING RESPONSES - OPENAI GPT

Same streaming concept as Anthropic, with OpenAI-specific syntax.
The core idea is identical: Display chunks as they arrive.
"""

import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# =============================================================================
# EXAMPLE 1: NON-STREAMING (for comparison)
# =============================================================================

print("=" * 80)
print("EXAMPLE 1: NON-STREAMING (for comparison)")
print("=" * 80)

print("\nAsking GPT a question...\n")
print("GPT (non-streaming): ", end="", flush=True)

# Regular API call
response = client.chat.completions.create(
    model="gpt-4o",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Explain Python in two sentences."}],
)

# All text arrives at once
print(response.choices[0].message.content)
print("\n^ Notice: Full response appeared at once (after waiting)")

# =============================================================================
# EXAMPLE 2: STREAMING - The Key Change
# =============================================================================

print("\n" + "=" * 80)
print("EXAMPLE 2: STREAMING - Word by Word")
print("=" * 80)

print("\nAsking GPT the same question with streaming...\n")
print("GPT (streaming): ", end="", flush=True)

# The only change: Add stream=True
# OpenAI returns an iterator directly (no 'with' statement needed)
stream = client.chat.completions.create(
    model="gpt-4o",
    max_tokens=1024,
    stream=True,  # This enables streaming!
    messages=[{"role": "user", "content": "Explain Python in two sentences."}],
)

# Iterate through chunks
for chunk in stream:
    # IMPORTANT: Check if chunk has content
    # Some chunks don't have content (e.g., metadata chunks)
    if chunk.choices[0].delta.content is not None:
        print(chunk.choices[0].delta.content, end="", flush=True)

print("\n\n^ Notice: Text appeared gradually as GPT generated it!")

# =============================================================================
# EXAMPLE 3: STREAMING WITH CONVERSATION MEMORY
# =============================================================================

print("\n" + "=" * 80)
print("EXAMPLE 3: STREAMING + CONVERSATION MEMORY")
print("=" * 80)

print("\nBuilding a response while streaming for conversation history...\n")

conversation_history = []

# Add user message
user_message = "What is FastAPI?"
conversation_history.append({"role": "user", "content": user_message})

print(f"User: {user_message}\n")
print("GPT: ", end="", flush=True)

# Stream the response AND accumulate it for history
full_response = ""  # We'll build the complete response here

stream = client.chat.completions.create(
    model="gpt-4o",
    max_tokens=1024,
    stream=True,
    messages=conversation_history,
)

for chunk in stream:
    # Check if chunk has content
    if chunk.choices[0].delta.content is not None:
        content = chunk.choices[0].delta.content
        print(content, end="", flush=True)  # Display in real-time
        full_response += content  # Accumulate for conversation history

print()  # Newline after streaming completes

# Add GPT's complete response to history
conversation_history.append({"role": "assistant", "content": full_response})

# Now we can ask a follow-up question
print("\nUser: Who created it?\n")
conversation_history.append({"role": "user", "content": "Who created it?"})

print("GPT: ", end="", flush=True)

full_response_2 = ""

stream = client.chat.completions.create(
    model="gpt-4o",
    max_tokens=1024,
    stream=True,
    messages=conversation_history,
)

for chunk in stream:
    if chunk.choices[0].delta.content is not None:
        content = chunk.choices[0].delta.content
        print(content, end="", flush=True)
        full_response_2 += content

print("\n")

conversation_history.append({"role": "assistant", "content": full_response_2})

print("=" * 80)
print(f"Conversation has {len(conversation_history)} messages")
print("=" * 80)

"""
WHAT YOU JUST LEARNED:

1. OpenAI vs Anthropic streaming differences:
   - Anthropic: client.messages.stream() with 'with' statement
   - OpenAI: client.chat.completions.create(stream=True) returns iterator
   - Anthropic: stream.text_stream yields text directly
   - OpenAI: Must check if chunk.choices[0].delta.content is not None

2. The pattern is the same:
   - Enable streaming
   - Iterate through chunks
   - Print immediately with flush=True
   - Accumulate for conversation history

3. Why check for None?
   - OpenAI sends metadata chunks without content
   - You must check before accessing .content
   - Anthropic's .text_stream filters these automatically

4. Real-world usage:
   - Web apps: Stream to frontend via WebSockets or SSE
   - CLI tools: Stream to terminal (this example)
   - Batch processing: Don't use streaming

NEXT STEP: Learn prompt chaining to build multi-step workflows
"""
