"""
CONVERSATION HISTORY: The "memory" that isn't magic

Here's the big secret frameworks don't want you to know:
Conversation memory is just a Python list of messages.

That's it. No database. No vector store. No framework.
Just append messages to a list and send the whole list each time.

Claude doesn't remember anything between API calls.
YOU give Claude the conversation history in every request.
"""

import os
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()
client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# This is your "memory" - just a list!
conversation_history = []

print("=" * 80)
print("MULTI-TURN CONVERSATION WITH CLAUDE")
print("=" * 80)
print("Watch how we build conversation history step by step...\n")

# TURN 1: User introduces themselves
print("TURN 1: User introduces themselves")
print("-" * 80)

user_message_1 = "Hi! My name is Alex and I'm learning about AI."

# Add user message to history
conversation_history.append({"role": "user", "content": user_message_1})

print(f"User: {user_message_1}")

# Send the ENTIRE conversation history (so far, just one message)
response_1 = client.messages.create(
    model="claude-4-sonnet-20250514",
    max_tokens=1024,
    messages=conversation_history,  # <-- The whole history goes here
)

assistant_message_1 = response_1.content[0].text
print(f"Claude: {assistant_message_1}\n")

# Add Claude's response to history
conversation_history.append({"role": "assistant", "content": assistant_message_1})

# Let's see what the history looks like now
print("CURRENT CONVERSATION HISTORY:")
print(conversation_history)
print()

# TURN 2: User asks a question
print("TURN 2: User asks about their name")
print("-" * 80)

user_message_2 = "What's my name?"

# Add to history
conversation_history.append({"role": "user", "content": user_message_2})

print(f"User: {user_message_2}")

# Send the ENTIRE conversation history (now 3 messages: user, assistant, user)
response_2 = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    messages=conversation_history,  # <-- Still just sending the list
)

assistant_message_2 = response_2.content[0].text
print(f"Claude: {assistant_message_2}\n")

# Add Claude's response to history
conversation_history.append({"role": "assistant", "content": assistant_message_2})

# Let's see what the history looks like now
print("CURRENT CONVERSATION HISTORY:")
print(conversation_history)
print()

# TURN 3: User asks about what they're learning
print("TURN 3: User asks about their learning topic")
print("-" * 80)

user_message_3 = "What did I say I was learning about?"

# Add to history
conversation_history.append({"role": "user", "content": user_message_3})

print(f"User: {user_message_3}")

# Send the ENTIRE history (now 5 messages)
response_3 = client.messages.create(
    model="claude-sonnet-4-20250514", max_tokens=1024, messages=conversation_history
)

assistant_message_3 = response_3.content[0].text
print(f"Claude: {assistant_message_3}\n")

conversation_history.append({"role": "assistant", "content": assistant_message_3})

# Let's see what the history looks like now
print("CURRENT CONVERSATION HISTORY:")
print(conversation_history)
print()

# TURN 4: Test Claude's memory of everything
print("TURN 4: Asking Claude to recall everything")
print("-" * 80)

user_message_4 = "Can you summarize what we've talked about?"

conversation_history.append({"role": "user", "content": user_message_4})

print(f"User: {user_message_4}")

response_4 = client.messages.create(
    model="claude-sonnet-4-20250514", max_tokens=1024, messages=conversation_history
)

assistant_message_4 = response_4.content[0].text
print(f"Claude: {assistant_message_4}\n")

conversation_history.append({"role": "assistant", "content": assistant_message_4})

# FINAL STATE
print("=" * 80)
print("FINAL CONVERSATION HISTORY:")
print("=" * 80)
for i, message in enumerate(conversation_history, 1):
    role = message["role"].upper()
    content = (
        message["content"][:100] + "..."
        if len(message["content"]) > 100
        else message["content"]
    )
    print(f"{i}. {role}: {content}\n")

print(f"Total messages in history: {len(conversation_history)}")
print(
    f"Total characters in history: {sum(len(m['content']) for m in conversation_history)}"
)

"""
THE BIG REVELATION:

This is ALL conversation memory is:
1. A list of message dictionaries
2. Each with "role" (user/assistant) and "content" (the text)
3. You append new messages
4. You send the entire list with each API call

That's it. No framework needed.

CRITICAL INSIGHTS:

1. CLAUDE HAS NO MEMORY:
   - Each API call is independent
   - Claude doesn't remember previous calls
   - YOU provide the history each time

2. THE PATTERN:
   Step 1: Add user message to list
   Step 2: Send entire list to Claude
   Step 3: Get Claude's response
   Step 4: Add Claude's response to list
   Step 5: Repeat

3. THIS IS STATELESS:
   - No database required (for basic chatbot)
   - No "session" to manage
   - Just a Python list in memory

4. WHEN TO PERSIST:
   - If you want conversations to survive restarts → save to database
   - If multi-user app → store per user
   - But for testing/learning → in-memory list is fine

5. MESSAGE STRUCTURE:
   - "role" must be "user" or "assistant"
   - Messages must alternate (user, assistant, user, assistant...)
   - Can't have two user messages in a row without assistant response

6. TOKEN LIMITS:
   - Claude Sonnet 4 has 200K token context window
   - Your conversation history counts toward this
   - Long conversations = more tokens = higher cost
   - Solution: Summarize old messages or truncate (we'll cover later)

REAL-WORLD IMPLEMENTATION:

In a FastAPI app, you might store this in:
- User's session (for web app)
- Redis (for fast access)
- PostgreSQL (for persistence)
- In-memory dict (for simple cases)

Example FastAPI structure:

In-memory storage (simple version)

conversations = {}  # user_id -> conversation_history

@app.post("/chat")
def chat(user_id: str, message: str):
    
    # Get or create conversation history
    if user_id not in conversations:
    conversations[user_id] = []
    
    # Add user message
    conversations[user_id].append({"role": "user", "content": message})

    # Get Claude's response
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        messages=conversations[user_id]
    )

    # Add assistant response
    assistant_message = response.content[0].text
    conversations[user_id].append({"role": "assistant", "content": assistant_message})

    return {"response": assistant_message}

WHAT ABOUT SYSTEM PROMPTS?

System prompts work with conversation history:

response = client.messages.create(
    model="claude-sonnet-4-20250514",
    system="You are a helpful assistant.",  # Applied to whole conversation
    messages=conversation_history
    )

The system prompt applies to the ENTIRE conversation, not just one turn.

COMMON MISTAKES TO AVOID:

❌ Forgetting to add assistant's response to history
❌ Adding messages in wrong order (must alternate)
❌ Not sending full history (Claude won't remember context)
❌ Letting history grow infinitely (token limits!)

✅ Always append both user AND assistant messages
✅ Maintain alternating user/assistant pattern
✅ Send complete history each time
✅ Monitor history size and truncate when needed

NEXT STEPS:
- Run this file and watch the conversation build
- Try asking Claude about earlier parts of the conversation
- Add more turns yourself
- See what happens if you remove a message from history mid-conversation
- Try building a simple chat loop (we'll do this next)

This is the foundation of every chatbot ever built.
No magic. Just lists.
"""
