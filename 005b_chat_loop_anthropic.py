import os
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()
client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

conversation_history = []

# while True:
#     user_input = input("You: ")
#     if user_input.lower() == "quit":
#         break

#     # TODO: Add user message to conversation_history
#     conversation_history.append({"role": "user", "content": user_input})

#     # TODO: Call Claude API with conversation_history
#     response = client.messages.create(
#         model="claude-4-sonnet-20250514",
#         max_tokens=1024,
#         messages=conversation_history,
#     )

#     # TODO: Extract Claude's response text
#     assistant_message = response.content[0].text

#     # TODO: Print Claude's response
#     print(f"Claude: {assistant_message}")

#     # TODO: Add Claude's response to conversation_history
#     conversation_history.append({"role": "assistant", "content": assistant_message})

###################################################
# STREAMING EXAMPLE
while True:
    user_input = input("You: ")
    if user_input.lower() == "quit":
        break

    # TODO: Add user message to conversation_history
    conversation_history.append({"role": "user", "content": user_input})

    # TODO: Call Claude API with conversation_history
    # TODO: Extract Claude's response text
    assistant_response = ""

    with client.messages.stream(
        model="claude-4-sonnet-20250514",
        max_tokens=1024,
        messages=conversation_history,
    ) as stream:
        for chunk in stream.text_stream:
            assistant_response += chunk
            print(chunk, end="", flush=True)

    # TODO: Print Claude's response
    print(f"Claude: {assistant_response}")

    # TODO: Add Claude's response to conversation_history
    conversation_history.append({"role": "assistant", "content": assistant_response})
