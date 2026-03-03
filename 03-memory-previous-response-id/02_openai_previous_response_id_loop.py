"""
MEMORY WITH previous_response_id - OPENAI GPT (Interactive)

Chat loop version using previous_response_id conversation chaining.
"""

import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1")
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

print("Chat with GPT using previous_response_id! (Type 'quit' to exit)")
print("-" * 65)

previous_response_id = None

while True:
    user_input = input("\nYou: ").strip()

    if user_input.lower() == "quit":
        print("Goodbye!")
        break

    request_args = {
        "model": MODEL,
        "max_output_tokens": 500,
        "input": user_input,
    }

    if previous_response_id is not None:
        request_args["previous_response_id"] = previous_response_id

    response = client.responses.create(**request_args)

    print(f"\nGPT: {response.output_text}")

    # Keep advancing the chain id for the next turn
    previous_response_id = response.id

"""
WHAT YOU JUST LEARNED:

1. You can maintain conversational continuity with one variable: previous_response_id.
2. The ID chain is convenient for iterative chat experiences.
3. For maximum transparency and portability, you should still understand list-based memory (step 2).
"""
