"""
CONVERSATION MEMORY - OPENAI GPT (Turn-by-Turn)

This demonstrates how AI "remembers" previous messages.
Spoiler: It doesn't. You send the entire conversation history with every request.

Memory = A Python list. That's it.

This is the OpenAI version of 01_anthropic_conversation.py
"""

import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# This is your "memory" - just a Python list
# It will hold all user and assistant messages
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
# Right now it's just one message, but we always send the full list
response_1 = client.chat.completions.create(
    model="gpt-4o",
    max_tokens=1024,
    messages=conversation_history,  # <-- The whole history goes here
)

# Step 3: Extract GPT's response
assistant_message_1 = response_1.choices[0].message.content
print(f"GPT: {assistant_message_1}\n")

# Step 4: Add GPT's response to history
# Now the history has 2 messages: user, then assistant
conversation_history.append({"role": "assistant", "content": assistant_message_1})

# =============================================================================
# TURN 2: User asks about something from Turn 1
# =============================================================================

print("TURN 2: User asks about their name")
print("-" * 80)

user_message_2 = "What's my name?"

# Add to history (now has 3 messages: user, assistant, user)
conversation_history.append({"role": "user", "content": user_message_2})

print(f"User: {user_message_2}")

# Send the ENTIRE conversation history again
# GPT sees all 3 messages, so it knows the user's name is Alex
response_2 = client.chat.completions.create(
    model="gpt-4o",
    max_tokens=1024,
    messages=conversation_history,  # <-- Still just sending the list
)

assistant_message_2 = response_2.choices[0].message.content
print(f"GPT: {assistant_message_2}\n")

# Add GPT's response (now 4 messages: user, assistant, user, assistant)
conversation_history.append({"role": "assistant", "content": assistant_message_2})

# =============================================================================
# TURN 3: Test memory of earlier context
# =============================================================================

print("TURN 3: User asks about their learning topic")
print("-" * 80)

user_message_3 = "What did I say I was learning about?"

conversation_history.append({"role": "user", "content": user_message_3})

print(f"User: {user_message_3}")

# Send the ENTIRE history (now 5 messages)
response_3 = client.chat.completions.create(
    model="gpt-4o",
    max_tokens=1024,
    messages=conversation_history
)

assistant_message_3 = response_3.choices[0].message.content
print(f"GPT: {assistant_message_3}\n")

conversation_history.append({"role": "assistant", "content": assistant_message_3})

# =============================================================================
# TURN 4: Ask GPT to summarize the whole conversation
# =============================================================================

print("TURN 4: Asking GPT to recall everything")
print("-" * 80)

user_message_4 = "Can you summarize what we've talked about?"

conversation_history.append({"role": "user", "content": user_message_4})

print(f"User: {user_message_4}")

response_4 = client.chat.completions.create(
    model="gpt-4o",
    max_tokens=1024,
    messages=conversation_history
)

assistant_message_4 = response_4.choices[0].message.content
print(f"GPT: {assistant_message_4}\n")

conversation_history.append({"role": "assistant", "content": assistant_message_4})

# =============================================================================
# Let's look at what the history contains
# =============================================================================

print("=" * 80)
print("FINAL CONVERSATION HISTORY:")
print("=" * 80)

for i, message in enumerate(conversation_history, 1):
    role = message["role"].upper()
    content = (
        message["content"][:50] + "..."
        if len(message["content"]) > 50
        else message["content"]
    )
    print(f"{i}. {role}: {content}\n")

print(f"Total messages in history: {len(conversation_history)}")

"""
WHAT YOU JUST LEARNED:

1. OpenAI uses the same pattern as Anthropic
   - conversation_history is a plain Python list
   - You append messages to it
   - You send the entire list with each API call
   - Only difference: API method names

2. The AI is stateless
   - GPT doesn't "remember" anything
   - We give it the full history every time
   - It appears to remember because we keep feeding it the context

3. This is how ALL chatbots work
   - ChatGPT does this
   - Claude does this
   - Custom chatbots do this
   - Even complex AI systems do this

4. Conversations get more expensive over time
   - More messages = more tokens sent
   - More tokens = higher API costs
   - Production apps truncate old messages or summarize

NEXT STEP: See how to build an interactive chat loop with this pattern
          (Check out 03_anthropic_while_loop.py or 04_openai_while_loop.py)
"""
