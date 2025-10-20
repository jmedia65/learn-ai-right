###################################
# ANTHROPIC API CHAT WITH STREAMING
###################################

import os
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()
client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

conversation_history = []

print("Chat with Claude! (Type ‘quit’ to exit)")
print("-" * 50)

while True:
    user_input = input("\nYou: ")
    if user_input.lower() == "quit":
        break

    # Add user message to history
    conversation_history.append({"role": "user", "content": user_input})

    # Print prompt for streaming output
    print("\nClaude: ", end="", flush=True)

    # Build complete response while streaming
    assistant_response = ""

    # Stream the response
    with client.messages.stream(
        model="claude-sonnet-4-20250514", max_tokens=1024, messages=conversation_history
    ) as stream:
        for chunk in stream.text_stream:
            assistant_response += chunk
            print(chunk, end="", flush=True)

    print()  # Newline after response completes

    # Add complete response to history
    conversation_history.append({"role": "assistant", "content": assistant_response})

###################################
# OPENAI API CHAT WITH STREAMING
###################################

###################################
# OPENAI API CHAT WITH STREAMING
###################################

import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

conversation_history = [
    {"role": "system", "content": "You are a helpful AI assistant."}
]

print("Chat with GPT! (Type ‘quit’ to exit)")
print("-" * 50)

while True:
    user_input = input("\nYou: ")
    if user_input.lower() == "quit":
        break

    # Add user message
    conversation_history.append({"role": "user", "content": user_input})

    # Print prompt for streaming
    print("\nGPT: ", end="", flush=True)

    # Build complete response
    assistant_response = ""

    # Stream the response
    stream = client.chat.completions.create(
        model="gpt-4o",
        max_tokens=1024,
        stream=True,  # Enable streaming
        messages=conversation_history,
    )

    for chunk in stream:
        # OpenAI chunks require null check
        if chunk.choices[0].delta.content is not None:
            content = chunk.choices[0].delta.content
            assistant_response += content
            print(content, end="", flush=True)

    print()  # Newline after response

    # Add to history
    conversation_history.append({"role": "assistant", "content": assistant_response})
