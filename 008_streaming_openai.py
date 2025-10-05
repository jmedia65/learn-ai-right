"""
STREAMING WITH OPENAI: Same concept, slightly different syntax

OpenAI's streaming works almost identically to Anthropic's.
Main difference: response structure is different (as usual).

But the core concept is the same: chunks arrive, you print them.
"""

import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ============================================================================

print("=" * 80)
print("EXAMPLE 1: NON-STREAMING (for comparison)")
print("=" * 80)

print("\nAsking GPT to write a poem...\n")
print("GPT (non-streaming): ", end="", flush=True)

response = client.chat.completions.create(
    model="gpt-4o",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "Write a short poem about Python programming."}
    ],
)

print(response.choices[0].message.content)
print("\n^ Notice: Full response appeared at once")

# ============================================================================

print("\n" + "=" * 80)
print("EXAMPLE 2: STREAMING - The Magic!")
print("=" * 80)

print("\nAsking GPT the same question with streaming...\n")
print("GPT (streaming): ", end="", flush=True)

# OPENAI STREAMING: Add stream=True
stream = client.chat.completions.create(
    model="gpt-4o",
    max_tokens=1024,
    stream=True,  # This enables streaming!
    messages=[
        {
            "role": "user",
            "content": "Write two short sentences about Python programming.",
        }
    ],
)

# OpenAI returns an iterator directly (no 'with' statement needed)
for chunk in stream:
    # Check if chunk has content
    if chunk.choices[0].delta.content is not None:
        print(chunk.choices[0].delta.content, end="", flush=True)

print("\n\n^ Notice: Text appeared word-by-word!")

# ============================================================================

print("\n" + "=" * 80)
print("EXAMPLE 3: UNDERSTANDING THE CHUNK STRUCTURE")
print("=" * 80)

print("\nLet's examine what's in each chunk...\n")

stream = client.chat.completions.create(
    model="gpt-4o",
    max_tokens=1024,
    stream=True,
    messages=[{"role": "user", "content": "Count to 5."}],
)

full_response = ""
chunk_count = 0

for chunk in stream:
    chunk_count += 1

    # OpenAI chunks have a delta object with content
    content = chunk.choices[0].delta.content

    if content is not None:
        full_response += content
        print(content, end="", flush=True)

print(f"\n\nReceived {chunk_count} chunks")
print(f"Full response: '{full_response}'")
print(f"Response length: {len(full_response)} characters")

# ============================================================================

print("\n" + "=" * 80)
print("EXAMPLE 4: STREAMING IN A CONVERSATION")
print("=" * 80)

# Your "memory" - still just a list!
# Notice: we're including the system message as the first message
conversation_history = [
    {
        "role": "system",
        "content": "You are a helpful AI assistant. You remember details from the conversation.",
    }
]

print("\nLet's have a streaming conversation...\n")

while True:
    user_input = input("\nYou: ")
    if user_input.lower() == "quit":
        break

    conversation_history.append({"role": "user", "content": user_input})

    print("GPT: ", end="", flush=True)  # Changed: prepare for streaming output

    try:
        stream = client.chat.completions.create(  # Changed: assigned to variable
            model="gpt-4o",
            max_tokens=1024,
            stream=True,  # Added: enable streaming
            messages=conversation_history,
        )

        assistant_message = ""  # Changed: build response from chunks

        for chunk in stream:  # Added: iterate over chunks
            if chunk.choices[0].delta.content is not None:  # Added: null check
                content = chunk.choices[0].delta.content
                assistant_message += content  # Added: build full response
                print(content, end="", flush=True)  # Changed: print each chunk

        print()

    except Exception as e:
        print(f"Error: {e}")
        # Don't add to history if API call failed
        conversation_history.pop()  # Remove the user message we just added
        continue

    conversation_history.append({"role": "assistant", "content": assistant_message})

# ============================================================================

print("\n" + "=" * 80)
print("COMPARING ANTHROPIC VS OPENAI STREAMING")
print("=" * 80)

print(
    """
ANTHROPIC PATTERN:
------------------
with client.messages.stream(
    model="claude-sonnet-4-20250514",
    messages=[...]
) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)

OPENAI PATTERN:
---------------
stream = client.chat.completions.create(
    model="gpt-4o",
    stream=True,
    messages=[...]
)

for chunk in stream:
    if chunk.choices[0].delta.content is not None:
        print(chunk.choices[0].delta.content, end="", flush=True)

KEY DIFFERENCES:
----------------
1. Anthropic uses `with` statement, OpenAI doesn't require it
2. Anthropic: stream.text_stream (cleaner)
   OpenAI: chunk.choices[0].delta.content (more verbose)
3. Anthropic: No null check needed
   OpenAI: Must check if content is not None
4. Anthropic: stream.get_final_message() for metadata
   OpenAI: Metadata in final chunk (finish_reason, usage)

SIMILARITIES:
-------------
1. Both use stream=True to enable streaming
2. Both iterate over chunks
3. Both require building full response manually
4. Both need flush=True for immediate output
5. Both work with conversation history

WHICH IS BETTER?
----------------
Neither! Just different API designs.
- Anthropic's is slightly cleaner (no null checks)
- OpenAI's is more explicit (you see the structure)
"""
)

"""
KEY INSIGHTS ABOUT OPENAI STREAMING:

1. ENABLING STREAMING:
   Just add stream=True to the create() call
   
   stream = client.chat.completions.create(
       model="gpt-4o",
       stream=True,  # This is all you need!
       messages=[...]
   )

2. CHUNK STRUCTURE:
   Each chunk is a ChatCompletionChunk object:
   
   chunk.choices[0].delta.content  # The text content (or None)
   chunk.choices[0].finish_reason  # Why stream ended (in final chunk)
   
   First few chunks: content has text
   Middle chunks: content has text
   Last chunk: content is None, finish_reason is set

3. NULL CHECKING REQUIRED:
   Always check if content exists:
   
   if chunk.choices[0].delta.content is not None:
       text = chunk.choices[0].delta.content
   
   Without this check, you'll get errors!

4. BUILDING FULL RESPONSE:
   full_response = ""
   for chunk in stream:
       if chunk.choices[0].delta.content is not None:
           full_response += chunk.choices[0].delta.content
   
   Then add full_response to conversation_history

5. NO 'WITH' STATEMENT:
   Unlike Anthropic, OpenAI doesn't require `with`
   But it's fine to use try/finally if you want cleanup

6. METADATA:
   The final chunk contains:
   - finish_reason: "stop", "length", etc.
   - usage: token counts (sometimes)
   
   But not all models return usage in streaming mode

7. SYSTEM MESSAGES:
   Work exactly the same with streaming:
   
   messages = [
       {"role": "system", "content": "You are helpful."},
       {"role": "user", "content": "Hello"}
   ]
   
   stream = client.chat.completions.create(
       model="gpt-4o",
       stream=True,
       messages=messages
   )

REAL-WORLD PATTERN (Interactive Chatbot):

conversation_history = [
    {"role": "system", "content": "You are helpful."}
]

while True:
    user_input = input("\nYou: ")
    if user_input.lower() == "quit":
        break
    
    conversation_history.append({"role": "user", "content": user_input})
    
    print("GPT: ", end="", flush=True)
    
    assistant_response = ""
    
    stream = client.chat.completions.create(
        model="gpt-4o",
        stream=True,
        messages=conversation_history
    )
    
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            content = chunk.choices[0].delta.content
            assistant_response += content
            print(content, end="", flush=True)
    
    conversation_history.append({"role": "assistant", "content": assistant_response})
    print()

COMMON MISTAKES:

❌ Forgetting to check if content is not None
❌ Not setting stream=True
❌ Forgetting flush=True
❌ Not building full response for history

✅ Always check: if chunk.choices[0].delta.content is not None
✅ Always set stream=True
✅ Always use flush=True
✅ Always concatenate chunks to build full response

NEXT STEPS:
- Run this file and see streaming in action
- Compare to Anthropic streaming (007)
- Build a streaming version of your OpenAI chat loop
- Try streaming with longer responses (stories, code, etc.)

Streaming makes your apps feel professional and responsive.
"""
