###################################
# ANTHROPIC API CONVERSATION TURNS
###################################

import os
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()
client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# This is your "memory" - just a Python list
conversation_history = []

# TURN 1: User introduces themselves
print("TURN 1: User introduces themselves")
print("-" * 80)

user_message_1 = "Hi! My name is Alex and I'm learning about AI."

# Add user message to history
conversation_history.append({"role": "user", "content": user_message_1})

print(f"User: {user_message_1}")

# Send the ENTIRE conversation history (so far, just one message)
response_1 = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    messages=conversation_history,  # <-- The whole history goes here
)

assistant_message_1 = response_1.content[0].text
print(f"Claude: {assistant_message_1}\n")

# Add Claude’s response to history
conversation_history.append({"role": "assistant", "content": assistant_message_1})

# --------------------------------------------------------------
# Now here’s where it gets interesting. Let’s add a second turn:

# TURN 2: User asks a question about something from Turn 1
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

# Add Claude’s response to history
conversation_history.append({"role": "assistant", "content": assistant_message_2})

# --------------------------------------------------------------
# Let’s add two more turns to really drive this home:

# TURN 3: User asks about what they’re learning
print("TURN 3: User asks about their learning topic")
print("-" * 80)

user_message_3 = "What did I say I was learning about?"

conversation_history.append({"role": "user", "content": user_message_3})

print(f"User: {user_message_3}")

# Send the ENTIRE history (now 5 messages)
response_3 = client.messages.create(
    model="claude-sonnet-4-20250514", max_tokens=1024, messages=conversation_history
)

assistant_message_3 = response_3.content[0].text
print(f"Claude: {assistant_message_3}\n")

conversation_history.append({"role": "assistant", "content": assistant_message_3})

# TURN 4: Test Claude’s memory of everything
print("TURN 4: Asking Claude to recall everything")
print("-" * 80)

user_message_4 = "Can you summarize what we’ve talked about?"

conversation_history.append({"role": "user", "content": user_message_4})

print(f"User: {user_message_4}")

response_4 = client.messages.create(
    model="claude-sonnet-4-20250514", max_tokens=1024, messages=conversation_history
)

assistant_message_4 = response_4.content[0].text
print(f"Claude: {assistant_message_4}\n")

conversation_history.append({"role": "assistant", "content": assistant_message_4})


# --------------------------------------------------------------
# Let’s look at what that history looks like after four turns:

print("FINAL CONVERSATION HISTORY:")
for i, message in enumerate(conversation_history, 1):
    role = message["role"].upper()
    content = (
        message["content"][:50] + "..."
        if len(message["content"]) > 50
        else message["content"]
    )
    print(f"{i}. {role}: {content}\n")

print(f"Total messages in history: {len(conversation_history)}")


###############################
# ANTHROPIC API WHILE LOOP
###############################

import os
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()
client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

conversation_history = []

print("Chat with Claude! (Type ‘quit’ to exit)")
print("-" * 50)

while True:  # <-- This is the only thing we added!
    user_input = input("\nYou: ")

    if user_input.lower() == "quit":
        break

    # Step 1: Add user message to history
    conversation_history.append({"role": "user", "content": user_input})

    # Step 2: Send full history to Claude
    response = client.messages.create(
        model="claude-sonnet-4-20250514", max_tokens=1024, messages=conversation_history
    )

    # Step 3: Extract response
    assistant_message = response.content[0].text

    # Step 4: Print response
    print(f"\nClaude: {assistant_message}")

    # Step 5: Add response to history
    conversation_history.append({"role": "assistant", "content": assistant_message})

    # Loop repeats! Back to Step 1 with updated history


###############################
# OPENAI API WHILE LOOP
###############################

import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

conversation_history = []

print("Chat with GPT! (Type 'quit' to exit)")
print("-" * 50)

while True:  # <-- This is the only thing we added!
    user_input = input("\nYou: ")

    if user_input.lower() == "quit":
        break

    # Step 1: Add user message to history
    conversation_history.append({"role": "user", "content": user_input})

    # Step 2: Send full history to GPT
    response = client.chat.completions.create(
        model="gpt-4o", max_tokens=1024, messages=conversation_history
    )

    # Step 3: Extract response
    assistant_message = response.choices[0].message.content

    # Step 4: Print response
    print(f"\nGPT: {assistant_message}")

    # Step 5: Add response to history
    conversation_history.append({"role": "assistant", "content": assistant_message})

    # Loop repeats! Back to Step 1 with updated history
