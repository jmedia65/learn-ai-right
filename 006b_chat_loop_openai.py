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

print("Chat with GPT! (Type 'quit' to exit)")
print("-" * 50)

while True:
    user_input = input("\nYou: ")
    if user_input.lower() == "quit":
        break

    # TODO: Add user message to conversation_history
    conversation_history.append({"role": "user", "content": user_input})

    # TODO: Call OpenAI API with conversation_history
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            max_tokens=1024,
            messages=conversation_history,  # Send the whole history
        )

        # TODO: Extract Claude's response text
        assistant_message = response.choices[0].message.content
    except Exception as e:
        print(f"Error: {e}")
        # Don't add to history if API call failed
        conversation_history.pop()  # Remove the user message we just added
        continue

    # TODO: Print Claude's response
    print(f"\nGPT: {assistant_message}")

    # TODO: Add Claude's response to conversation_history
    conversation_history.append({"role": "assistant", "content": assistant_message})
