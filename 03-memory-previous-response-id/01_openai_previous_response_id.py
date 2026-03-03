"""
MEMORY WITH previous_response_id - OPENAI GPT

This shows conversation chaining with OpenAI Responses API.
Instead of resending a full history list, we pass previous_response_id.
"""

import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1")
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

print("TURN 1: User introduces themselves")
print("-" * 80)

response_1 = client.responses.create(
    model=MODEL,
    max_output_tokens=300,
    input="Hi! My name is Alex and I'm learning about AI.",
)
print(f"GPT: {response_1.output_text}\n")

print("TURN 2: Follow-up question")
print("-" * 80)

response_2 = client.responses.create(
    model=MODEL,
    max_output_tokens=300,
    input="What's my name?",
    previous_response_id=response_1.id,
)
print(f"GPT: {response_2.output_text}\n")

print("TURN 3: Another follow-up")
print("-" * 80)

response_3 = client.responses.create(
    model=MODEL,
    max_output_tokens=300,
    input="What did I say I was learning about?",
    previous_response_id=response_2.id,
)
print(f"GPT: {response_3.output_text}\n")

print("TURN 4: Summary request")
print("-" * 80)

response_4 = client.responses.create(
    model=MODEL,
    max_output_tokens=300,
    input="Summarize what we've talked about.",
    previous_response_id=response_3.id,
)
print(f"GPT: {response_4.output_text}\n")

print("=" * 80)
print("CHAIN IDS")
print("=" * 80)
print(f"Turn 1 id: {response_1.id}")
print(f"Turn 2 id: {response_2.id} (linked to turn 1)")
print(f"Turn 3 id: {response_3.id} (linked to turn 2)")
print(f"Turn 4 id: {response_4.id} (linked to turn 3)")

"""
WHAT YOU JUST LEARNED:

1. previous_response_id links one model call to the prior one.
2. You get conversational continuity without manually sending history each time.
3. This is convenience, not magic memory.
"""
