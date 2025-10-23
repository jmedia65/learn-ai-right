"""
STREAMING RESPONSES - ANTHROPIC CLAUDE

Streaming makes responses appear word-by-word in real-time.
This is how ChatGPT's interface works - it's just streaming!

Without streaming: Wait... wait... wait... then full response
With streaming: Words appear as Claude generates them
"""

import os
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()
client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# =============================================================================
# EXAMPLE 1: NON-STREAMING (for comparison)
# =============================================================================

print("=" * 80)
print("EXAMPLE 1: NON-STREAMING (for comparison)")
print("=" * 80)

print("\nAsking Claude a question...\n")
print("Claude (non-streaming): ", end="", flush=True)

# Regular API call - we've been using this pattern
response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Explain Python in two sentences."}],
)

# All text arrives at once
print(response.content[0].text)
print("\n^ Notice: Full response appeared at once (after waiting)")

# =============================================================================
# EXAMPLE 2: STREAMING - The Key Change
# =============================================================================

print("\n" + "=" * 80)
print("EXAMPLE 2: STREAMING - Word by Word")
print("=" * 80)

print("\nAsking Claude the same question with streaming...\n")
print("Claude (streaming): ", end="", flush=True)

# The only change: Use .stream() instead of .create()
# Wrap in a context manager (with statement) for proper cleanup
with client.messages.stream(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Explain Python in two sentences."}],
) as stream:
    # stream.text_stream yields chunks as they arrive
    for chunk in stream.text_stream:
        # chunk is a small piece of text (word, part of a word, or punctuation)
        # flush=True forces immediate display (bypasses Python's output buffering)
        print(chunk, end="", flush=True)

print("\n\n^ Notice: Text appeared gradually as Claude generated it!")

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
print("Claude: ", end="", flush=True)

# Stream the response AND accumulate it for history
full_response = ""  # We'll build the complete response here

with client.messages.stream(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    messages=conversation_history,
) as stream:
    for chunk in stream.text_stream:
        print(chunk, end="", flush=True)  # Display in real-time
        full_response += chunk  # Accumulate for conversation history

print()  # Newline after streaming completes

# Add Claude's complete response to history
conversation_history.append({"role": "assistant", "content": full_response})

# Now we can ask a follow-up question
print("\nUser: Who created it?\n")
conversation_history.append({"role": "user", "content": "Who created it?"})

print("Claude: ", end="", flush=True)

full_response_2 = ""

with client.messages.stream(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    messages=conversation_history,
) as stream:
    for chunk in stream.text_stream:
        print(chunk, end="", flush=True)
        full_response_2 += chunk

print("\n")

conversation_history.append({"role": "assistant", "content": full_response_2})

print("=" * 80)
print(f"Conversation has {len(conversation_history)} messages")
print("=" * 80)

"""
WHAT YOU JUST LEARNED:

1. Streaming is a simple API change
   - Non-streaming: client.messages.create()
   - Streaming: client.messages.stream() in a with statement

2. The key is flush=True
   - print(chunk, end="", flush=True)
   - Without flush=True, Python buffers output and you won't see real-time streaming
   - end="" prevents newlines after each chunk

3. You can stream AND save for history
   - Display chunks immediately: print(chunk, ...)
   - Accumulate them: full_response += chunk
   - Add complete response to conversation_history after streaming

4. When to use streaming:
   - Interactive applications (chatbots, web interfaces)
   - Long responses (essays, code generation)
   - Better UX (feels 30-40% faster to users)

   When NOT to use streaming:
   - Background processing
   - Batch jobs
   - When you need the complete response before proceeding

NEXT STEP: Learn prompt chaining to build multi-step workflows
"""
