"""
STREAMING RESPONSES - OPENAI GPT (Responses API)

Same streaming concept as Anthropic, with OpenAI-specific event syntax.
Core idea: display text chunks as they arrive.
"""

import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
MODEL = os.getenv("OPENAI_MODEL", "gpt-6-luna")
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# =============================================================================
# EXAMPLE 1: NON-STREAMING (for comparison)
# =============================================================================

print("=" * 80)
print("EXAMPLE 1: NON-STREAMING (for comparison)")
print("=" * 80)

print("\nAsking GPT a question...\n")
print("GPT (non-streaming): ", end="", flush=True)

response = client.responses.create(
    model=MODEL,
    max_output_tokens=4096,
    input="Explain Python in two sentences.",
)
if response.status != "completed":
    raise RuntimeError(f"Response did not complete: {response.status}")

print(response.output_text)
print("\n^ Notice: Full response appeared at once (after waiting)")

# =============================================================================
# EXAMPLE 2: STREAMING - The Key Change
# =============================================================================

print("\n" + "=" * 80)
print("EXAMPLE 2: STREAMING - Word by Word")
print("=" * 80)

print("\nAsking GPT the same question with streaming...\n")
print("GPT (streaming): ", end="", flush=True)

# The key change: stream=True and iterate events
stream = client.responses.create(
    model=MODEL,
    max_output_tokens=4096,
    input="Explain Python in two sentences.",
    stream=True,
)

completed_response = None
for event in stream:
    if event.type == "response.output_text.delta":
        print(event.delta, end="", flush=True)
    elif event.type == "response.completed":
        completed_response = event.response
    elif event.type in ("response.failed", "response.incomplete", "error"):
        raise RuntimeError(f"Stream ended with {event.type}")

if completed_response is None:
    raise RuntimeError("Stream ended before response.completed")

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

full_response = ""

stream = client.responses.create(
    model=MODEL,
    max_output_tokens=4096,
    input=conversation_history,
    stream=True,
    store=False,
)

completed_response = None
for event in stream:
    if event.type == "response.output_text.delta":
        print(event.delta, end="", flush=True)
        full_response += event.delta
    elif event.type == "response.completed":
        completed_response = event.response
    elif event.type in ("response.failed", "response.incomplete", "error"):
        raise RuntimeError(f"Stream ended with {event.type}")

if completed_response is None:
    raise RuntimeError("Stream ended before response.completed")

print()

# Replay every output item so reasoning models retain their full context.
conversation_history.extend(completed_response.output)

print("\nUser: Who created it?\n")
conversation_history.append({"role": "user", "content": "Who created it?"})

print("GPT: ", end="", flush=True)

full_response_2 = ""

stream = client.responses.create(
    model=MODEL,
    max_output_tokens=4096,
    input=conversation_history,
    stream=True,
    store=False,
)

completed_response = None
for event in stream:
    if event.type == "response.output_text.delta":
        print(event.delta, end="", flush=True)
        full_response_2 += event.delta
    elif event.type == "response.completed":
        completed_response = event.response
    elif event.type in ("response.failed", "response.incomplete", "error"):
        raise RuntimeError(f"Stream ended with {event.type}")

if completed_response is None:
    raise RuntimeError("Stream ended before response.completed")

print("\n")

conversation_history.extend(completed_response.output)

print("=" * 80)
print(f"Conversation has {len(conversation_history)} input/output items")
print("=" * 80)

"""
WHAT YOU JUST LEARNED:

1. Responses streaming uses events
   - stream=True enables event streaming
   - response.output_text.delta events carry incremental text

2. The pattern is still the same idea
   - Iterate chunks/events
   - Print immediately with flush=True
   - Optionally accumulate for memory

3. Streaming + memory works cleanly
   - Show text in real-time for UX
   - Save all response output items to conversation_history after completion

NEXT STEP: Learn prompt chaining to build multi-step workflows
"""
