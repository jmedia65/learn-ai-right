"""
CONVERSATION MEMORY - OPENAI GPT (Turn-by-Turn, Responses API)

This demonstrates how AI "remembers" previous messages.
Spoiler: It doesn't. You send the entire conversation history with every request.

Memory = A Python list. That's it.
"""

import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
MODEL = os.getenv("OPENAI_MODEL", "gpt-6-luna")
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# This is your "memory" - just a Python list
# It will hold user messages and every output item returned by the model.
conversation_history = []

# =============================================================================
# TURN 1: User introduces themselves
# =============================================================================

print("TURN 1: User introduces themselves")
print("-" * 80)

user_message_1 = "Hi! My name is Alex and I'm learning about AI."

# Step 1: Add user message to the history list
conversation_history.append({"role": "user", "content": user_message_1})

print(f"User: {user_message_1}")

# Step 2: Send the ENTIRE conversation history
response_1 = client.responses.create(
    model=MODEL,
    max_output_tokens=4096,
    input=conversation_history,
    store=False,
)
if response_1.status != "completed":
    raise RuntimeError(f"Response did not complete: {response_1.status}")

# Step 3: Extract GPT's response
assistant_message_1 = response_1.output_text
print(f"GPT: {assistant_message_1}\n")

# Step 4: Keep all output items, including reasoning items, for the next turn.
conversation_history.extend(response_1.output)

# =============================================================================
# TURN 2: User asks about something from Turn 1
# =============================================================================

print("TURN 2: User asks about their name")
print("-" * 80)

user_message_2 = "What's my name?"

conversation_history.append({"role": "user", "content": user_message_2})

print(f"User: {user_message_2}")

response_2 = client.responses.create(
    model=MODEL,
    max_output_tokens=4096,
    input=conversation_history,
    store=False,
)
if response_2.status != "completed":
    raise RuntimeError(f"Response did not complete: {response_2.status}")

assistant_message_2 = response_2.output_text
print(f"GPT: {assistant_message_2}\n")

conversation_history.extend(response_2.output)

# =============================================================================
# TURN 3: Test memory of earlier context
# =============================================================================

print("TURN 3: User asks about their learning topic")
print("-" * 80)

user_message_3 = "What did I say I was learning about?"

conversation_history.append({"role": "user", "content": user_message_3})

print(f"User: {user_message_3}")

response_3 = client.responses.create(
    model=MODEL,
    max_output_tokens=4096,
    input=conversation_history,
    store=False,
)
if response_3.status != "completed":
    raise RuntimeError(f"Response did not complete: {response_3.status}")

assistant_message_3 = response_3.output_text
print(f"GPT: {assistant_message_3}\n")

conversation_history.extend(response_3.output)

# =============================================================================
# TURN 4: Ask GPT to summarize the whole conversation
# =============================================================================

print("TURN 4: Asking GPT to recall everything")
print("-" * 80)

user_message_4 = "Can you summarize what we've talked about?"

conversation_history.append({"role": "user", "content": user_message_4})

print(f"User: {user_message_4}")

response_4 = client.responses.create(
    model=MODEL,
    max_output_tokens=4096,
    input=conversation_history,
    store=False,
)
if response_4.status != "completed":
    raise RuntimeError(f"Response did not complete: {response_4.status}")

assistant_message_4 = response_4.output_text
print(f"GPT: {assistant_message_4}\n")

conversation_history.extend(response_4.output)

# =============================================================================
# Let's look at what the history contains
# =============================================================================

print("=" * 80)
print("FINAL CONVERSATION HISTORY:")
print("=" * 80)

for i, item in enumerate(conversation_history, 1):
    if isinstance(item, dict):
        label, preview = "USER", item["content"]
    else:
        label = item.type.upper()
        preview = "".join(
            block.text for block in (getattr(item, "content", None) or [])
            if block.type == "output_text"
        ) or "(non-text output item)"
    print(f"{i}. {label}: {preview[:50]}\n")

print(f"Total items in history: {len(conversation_history)}")

"""
WHAT YOU JUST LEARNED:

1. Responses API still uses the same memory concept
   - conversation_history is a plain Python list
   - You append user messages and the model's output items to it
   - You send the entire list with each API call

2. The AI is stateless
   - GPT doesn't "remember" anything between calls by default
   - We give it full history each time
   - It appears to remember because context is resent

3. OpenAI also supports previous_response_id
   - That's a convenience for stateful chaining
   - But this manual list approach teaches the core principle clearly

4. Conversations get more expensive over time
   - More messages = more tokens sent
   - More tokens = higher API costs
   - Production apps truncate old messages or summarize

NEXT STEP: See how to build an interactive chat loop with this pattern
"""
