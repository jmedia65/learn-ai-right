"""
STREAMING RESPONSES: Make Claude respond in real-time

Without streaming:
- User waits... waits... waits... then gets full response at once
- Feels slow and unresponsive

With streaming:
- Claude's response appears word-by-word (or chunk-by-chunk)
- Feels fast and interactive
- Better UX, especially for long responses

This is how ChatGPT's interface works - it's just streaming!
"""

import os
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()
client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# ============================================================================
# EXAMPLE 1: NON-STREAMING

print("=" * 80)
print("EXAMPLE 1: NON-STREAMING (for comparison)")
print("=" * 80)

# Regular (non-streaming) call - we've been doing this
print("\nAsking Claude to write a poem...\n")
print("Claude (non-streaming): ", end="", flush=True)

response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "Write two sentences about Python programming."}
    ],
)

# All text arrives at once
print(response.content[0].text)
print("\n^ Notice: Full response appeared at once (after waiting)")

# ============================================================================
# EXAMPLE 2: STREAMING

print("\n" + "=" * 80)
print("EXAMPLE 2: STREAMING - The Magic!")
print("=" * 80)

print("\nAsking Claude the same question with streaming...\n")
print("Claude (streaming): ", end="", flush=True)

# STREAMING: Just add stream=True!
# The with statement ensures proper cleanup
with client.messages.stream(
    model="claude-4-sonnet-20250514",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "Write two sentences about Python programming."}
    ],
) as stream:
    # stream is an iterator that yields chunks as they arrive
    for chunk in stream.text_stream:
        # text is a small chunk (could be a word, part of a word, or punctuation)
        print(chunk, end="", flush=True)  # Print immediately, no newline

print("\n\n^ Notice: Text appeared word-by-word as Claude generated it!")

# ============================================================================
# EXAMPLE 3: STREAMING WITH FULL CONTROL

print("\n" + "=" * 80)
print("EXAMPLE 3: STREAMING WITH FULL CONTROL")
print("=" * 80)

print("\nLet's see what's actually happening in the stream...\n")

full_response = ""  # We'll build the complete response

with client.messages.stream(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "Explain what streaming is in one sentence."}
    ],
) as stream:
    chunk_count = 0

    for chunk in stream.text_stream:
        chunk_count += 1
        full_response += chunk  # Build complete response
        print(chunk, end="", flush=True)

print(f"\n\nReceived {chunk_count} chunks")
print(f"Full response length: {len(full_response)} characters")

# ============================================================================
# EXAMPLE 4: ACCESSING STREAM METADATA

print("\n" + "=" * 80)
print("EXAMPLE 4: ACCESSING STREAM METADATA")
print("=" * 80)

print("\nStreaming also gives you access to events and metadata...\n")

with client.messages.stream(
    model="claude-4-sonnet-20250514",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Count to 5."}],
) as stream:
    # Print the response
    for chunk in stream.text_stream:
        print(chunk, end="", flush=True)

    # After streaming completes, get the final message
    final_message = stream.get_final_message()

print("\n\nSTREAM METADATA:")
print(f"Model used: {final_message.model}")
print(f"Stop reason: {final_message.stop_reason}")
print(f"Input tokens: {final_message.usage.input_tokens}")
print(f"Output tokens: {final_message.usage.output_tokens}")

# ============================================================================
# EXAMPLE 5: STREAMING IN A CONVERSATION

print("\n" + "=" * 80)
print("EXAMPLE 5: STREAMING IN A CONVERSATION")
print("=" * 80)

conversation_history = []

print("\nLet's have a streaming conversation...\n")

# Turn 1
user_msg_1 = "Hi! My name is Max."
conversation_history.append({"role": "user", "content": user_msg_1})

print(f"You: {user_msg_1}")
print("Claude: ", end="", flush=True)

assistant_response_1 = ""

with client.messages.stream(
    model="claude-4-sonnet-20250514",
    max_tokens=1024,
    messages=conversation_history,
) as stream:
    for chunk in stream.text_stream:
        assistant_response_1 += chunk
        print(chunk, end="", flush=True)

conversation_history.append({"role": "assistant", "content": assistant_response_1})

# Turn 2
print("\n")
user_msg_2 = "What's my name?"
conversation_history.append({"role": "user", "content": user_msg_2})

print(f"You: {user_msg_2}")
print("Claude: ", end="", flush=True)

assistant_response_2 = ""

with client.messages.stream(
    model="claude-sonnet-4-20250514", max_tokens=1024, messages=conversation_history
) as stream:
    for text in stream.text_stream:
        assistant_response_2 += text
        print(text, end="", flush=True)

conversation_history.append({"role": "assistant", "content": assistant_response_2})

print("\n")

"""
KEY INSIGHTS ABOUT STREAMING:

1. WHY STREAMING MATTERS:
   ✅ Better UX - users see progress immediately
   ✅ Feels faster (even if total time is similar)
   ✅ Users can start reading while Claude is still generating
   ✅ Professional feel (like ChatGPT)

2. HOW STREAMING WORKS:
   - Non-streaming: client.messages.create()
   - Streaming: client.messages.stream()
   
   That's the only difference in the call!

3. THE PATTERN:
   with client.messages.stream(...) as stream:
       for text in stream.text_stream:
           print(text, end="", flush=True)
   
   - `with` ensures proper cleanup
   - `stream.text_stream` yields text chunks as they arrive
   - `end=""` prevents newlines between chunks
   - `flush=True` forces immediate output (important!)

4. BUILDING THE FULL RESPONSE:
   You need to concatenate chunks yourself:
   
   full_response = ""
   for text in stream.text_stream:
       full_response += text
       print(text, end="", flush=True)
   
   Then add full_response to conversation_history

5. METADATA STILL AVAILABLE:
   After streaming completes:
   final_message = stream.get_final_message()
   
   This gives you:
   - Token counts
   - Stop reason
   - Model used
   - Everything from non-streaming response

6. CHUNK SIZES:
   - Chunks are typically 1-10 characters
   - Could be a word, part of a word, or punctuation
   - You have no control over chunk size (server decides)
   - Just process them as they arrive

7. ERROR HANDLING:
   with client.messages.stream(...) as stream:
       try:
           for text in stream.text_stream:
               print(text, end="", flush=True)
       except Exception as e:
           print(f"\nStreaming error: {e}")

8. STREAMING WITH SYSTEM PROMPTS:
   Works exactly the same:
   
   with client.messages.stream(
       model="claude-sonnet-4-20250514",
       system="You are helpful.",  # System prompt works!
       messages=[...]
   ) as stream:
       for text in stream.text_stream:
           print(text, end="", flush=True)

9. WHEN TO USE STREAMING:
   ✅ Interactive chatbots (always!)
   ✅ Long responses (essays, code, analysis)
   ✅ User-facing applications
   
   ❌ Background processing (use non-streaming)
   ❌ When you need full response before proceeding
   ❌ Logging/analytics (harder with streaming)

10. PERFORMANCE:
    - Streaming doesn't make Claude faster
    - Total time is similar to non-streaming
    - But PERCEIVED speed is much better (UX win)

REAL-WORLD PATTERN (Interactive Chatbot):

conversation_history = []

while True:
    user_input = input("\nYou: ")
    if user_input.lower() == "quit":
        break
    
    conversation_history.append({"role": "user", "content": user_input})
    
    print("Claude: ", end="", flush=True)
    
    assistant_response = ""
    
    with client.messages.stream(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        messages=conversation_history
    ) as stream:
        for text in stream.text_stream:
            assistant_response += text
            print(text, end="", flush=True)
    
    conversation_history.append({"role": "assistant", "content": assistant_response})
    print()  # Newline after response

COMMON MISTAKES:

❌ Forgetting flush=True (output won't appear immediately)
❌ Not building full_response (can't add to history)
❌ Not using `with` statement (resources not cleaned up)
❌ Adding newlines between chunks (breaks the effect)

✅ Always use flush=True
✅ Concatenate chunks to build full response
✅ Use `with` for proper cleanup
✅ Use end="" to avoid newlines

NEXT STEPS:
- Run this file and watch streaming in action
- Compare the non-streaming vs streaming examples
- Try longer prompts to see streaming really shine
- Build a streaming version of your chat loop!

Streaming is how you make AI feel magical to users.
"""
