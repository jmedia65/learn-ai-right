"""
CONVERSATION HISTORY WITH OPENAI: Same concept, same simplicity

The only difference from Anthropic:
- System message goes in the messages array (we learned this in file 004)
- Otherwise, conversation history works identically

It's still just a list. Still just appending messages. Still that simple.
"""

import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Your "memory" - still just a list!
# Notice: we're including the system message as the first message
conversation_history = [
    {
        "role": "system",
        "content": "You are a helpful AI assistant. You remember details from the conversation.",
    }
]

print("=" * 80)
print("MULTI-TURN CONVERSATION WITH GPT")
print("=" * 80)
print("Watch how conversation history works with OpenAI...\n")

# TURN 1: User introduces themselves
print("TURN 1: User introduces themselves")
print("-" * 80)

user_message_1 = "Hi! My name is Alex and I'm learning about AI."

# Add user message to history
conversation_history.append({"role": "user", "content": user_message_1})

print(f"User: {user_message_1}")

response_1 = client.chat.completions.create(
    model="gpt-4o",
    max_tokens=1024,
    messages=conversation_history,  # Send the whole history
)

assistant_message_1 = response_1.choices[0].message.content
print(f"GPT: {assistant_message_1}\n")

conversation_history.append({"role": "assistant", "content": assistant_message_1})

# Let's see what the history looks like now
print("CURRENT CONVERSATION HISTORY:")
# print(f"Messages: {len(conversation_history)} (1 system, 1 user, 1 assistant)")
print(f"Messages: {conversation_history}")
print()

# TURN 2: User asks a question
print("TURN 2: User asks about their name")
print("-" * 80)

user_message_2 = "What is my name?"

# Add to history
conversation_history.append({"role": "user", "content": user_message_2})

print(f"User: {user_message_2}")

# Send the ENTIRE conversation history
response_2 = client.chat.completions.create(
    model="gpt-4o",
    max_tokens=1024,
    messages=conversation_history,  # Send the whole history
)

assistant_message_2 = response_2.choices[0].message.content
print(f"GPT: {assistant_message_2}\n")

conversation_history.append({"role": "assistant", "content": assistant_message_2})

print("CURRENT CONVERSATION HISTORY:")
print(f"Messages: {conversation_history}")
print()

# TURN 3: User asks about what they're learning
print("TURN 3: User asks about what they're learning")
print("-" * 80)

user_message_3 = "What did I say I was learning about?"

conversation_history.append({"role": "user", "content": user_message_3})

print(f"User: {user_message_3}")

# Send the ENTIRE conversation history
response_3 = client.chat.completions.create(
    model="gpt-4o",
    max_tokens=1024,
    messages=conversation_history,  # Send the whole history
)

assistant_message_3 = response_3.choices[0].message.content
print(f"GPT: {assistant_message_3}\n")

# Add response to history
conversation_history.append({"role": "assistant", "content": assistant_message_3})

print("CURRENT CONVERSATION HISTORY:")
print(f"Messages: {conversation_history}")
print()

# TURN 4: Test GPT's memory
print("TURN 4: Asking GPT to recall everything")
print("-" * 80)

user_message_4 = "Can you summarize what we've talked about?"

conversation_history.append({"role": "user", "content": user_message_4})

print(f"User: {user_message_4}")

response_4 = client.chat.completions.create(
    model="gpt-4o", max_tokens=1024, messages=conversation_history
)

assistant_message_4 = response_4.choices[0].message.content
print(f"GPT: {assistant_message_4}\n")

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

# BONUS: Side-by-side comparison
print("\n" + "=" * 80)
print("ANTHROPIC VS OPENAI: CONVERSATION HISTORY PATTERN")
print("=" * 80)

print("\nANTHROPIC PATTERN:")
print(
    """
# System prompt separate
conversation = []
conversation.append({"role": "user", "content": "Hello"})

response = client.messages.create(
    model="claude-sonnet-4-20250514",
    system="You are helpful.",
    messages=conversation
)

conversation.append({"role": "assistant", "content": response.content[0].text})
"""
)

print("\nOPENAI PATTERN:")
print(
    """
# System prompt in messages array
conversation = [
    {"role": "system", "content": "You are helpful."}
]
conversation.append({"role": "user", "content": "Hello"})

response = client.chat.completions.create(
    model="gpt-4o",
    messages=conversation
)

conversation.append({"role": "assistant", "content": response.choices[0].message.content})
"""
)

print("\nBOTH ARE JUST LISTS! Same concept, slightly different syntax.")

"""
KEY TAKEAWAYS:

1. OPENAI CONVERSATION HISTORY = LIST
   Just like Anthropic. Nothing special.

2. SYSTEM MESSAGE PLACEMENT:
   With OpenAI, system message is just the first item in the list
   It stays there throughout the conversation
   
   conversation_history = [
       {"role": "system", "content": "..."},  # First message, stays here
       {"role": "user", "content": "..."},
       {"role": "assistant", "content": "..."},
       {"role": "user", "content": "..."},
       # ... more messages
   ]

3. THE PATTERN IS IDENTICAL:
   - Append user message
   - Send entire list
   - Get response
   - Append assistant message
   - Repeat

4. COST CONSIDERATION:
   GPT-4o pricing (as of 2025):
   - Input: $2.50 per 1M tokens
   - Output: $10.00 per 1M tokens
   
   Longer conversations = more input tokens = higher cost
   (Because you send the ENTIRE history each time)

5. MANAGING HISTORY SIZE:
   When history gets too long, you have options:
   
   Option A: Truncate old messages
   Keep only last N messages (plus system)   
   MAX_HISTORY = 10
   if len(conversation_history) > MAX_HISTORY:
   # Keep system message + last N messages
   conversation_history = [conversation_history[0]] + conversation_history[-(MAX_HISTORY-1):]

   Option B: Summarize old messages (compacting)
   Use LLM to summarize first half of conversation
   Replace old messages with summary
   Keep recent messages for context

   Option C: Sliding window
   Keep system + last 20 messages
   Drop everything in between  

6. BUILDING A SIMPLE CHATBOT:
   This is all you need for a functional chatbot:
   def chat(user_input: str, history: list) -> tuple[str, list]:
       # Add user message
       history.append({"role": "user", "content": user_input})
       
       # Get response
       response = client.chat.completions.create(
           model="gpt-4o",
           messages=history
       )
       
       # Extract and add assistant message
       assistant_message = response.choices[0].message.content
       history.append({"role": "assistant", "content": assistant_message})
       
       return assistant_message, history
   
   # Usage
   history = [{"role": "system", "content": "You are helpful."}]
   
   response, history = chat("Hello!", history)
   print(response)
   
   response, history = chat("What's 2+2?", history)
   print(response)   

7. MULTI-USER APPLICATIONS:
In real apps with multiple users:
# Dictionary mapping user_id to their conversation history
   user_conversations = {}
   
   def get_or_create_conversation(user_id: str) -> list:
       if user_id not in user_conversations:
           user_conversations[user_id] = [
               {"role": "system", "content": "You are helpful."}
           ]
       return user_conversations[user_id]
   
   def chat_with_user(user_id: str, message: str) -> str:
       history = get_or_create_conversation(user_id)
       history.append({"role": "user", "content": message})
       
       response = client.chat.completions.create(
           model="gpt-4o",
           messages=history
       )
       
       assistant_message = response.choices[0].message.content
       history.append({"role": "assistant", "content": assistant_message})
       
       return assistant_message

8. PERSISTENCE (DATABASE): To save conversations:
import json
   
   # Save to database
   conversation_json = json.dumps(conversation_history)
   db.execute("INSERT INTO conversations (user_id, messages) VALUES (?, ?)", 
              (user_id, conversation_json))
   
   # Load from database
   row = db.execute("SELECT messages FROM conversations WHERE user_id = ?", 
                    (user_id,)).fetchone()
   conversation_history = json.loads(row[0])


9. COMPARING PROVIDERS:
    You now know conversation history for BOTH Anthropic and OpenAI
    They're 95% identical - just different message structures
    This means you can easily:

    - Switch between providers
    - Use both in the same app
    - Build a unified interface


10. NO FRAMEWORK NEEDED:
Frameworks like LangChain have complex "ConversationBufferMemory" classes
Reality: It's just a list wrapper with extra complexity
You don't need it. You have a list. That's all memory is.

NEXT STEPS:

- Run this file and see GPT remember context
- Compare GPT's responses to Claude's (from file 005)
- Try building a simple chat loop (input in terminal, keep chatting)
- Experiment with truncating history
- Try both providers with the same conversation

You now understand conversation memory.
It's not magic. It's not complex. It's a list.
This is how every chatbot works, from ChatGPT to customer support bots.
"""
