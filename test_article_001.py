###############################
# ANTHROPIC API MAKE A CALL
###############################

import os
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()
client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Explain what an API is in one sentence."}],
)

answer = response.content[0].text

# print(answer)
# print(f"Model used: {response.model}")
# print(f"Stop reason: {response.stop_reason}")
# print(f"Input tokens: {response.usage.input_tokens}")
# print(f"Output tokens: {response.usage.output_tokens}")

# Extract and display the response
print("=" * 80)
print("CLAUDE’S RESPONSE:")
print("=" * 80)
print(answer)
print("=" * 80)

# Display metadata
print("\nRESPONSE METADATA:")
print(f"Model used: {response.model}")
print(f"Stop reason: {response.stop_reason}")
print(f"Input tokens: {response.usage.input_tokens}")
print(f"Output tokens: {response.usage.output_tokens}")


###############################
# OPENAI API MAKE A CALL
###############################

import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

response = client.chat.completions.create(
    model="gpt-4o",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Explain what an API is in one sentence."}],
)

answer = response.choices[0].message.content

# Extract and display the response
print("=" * 80)
print("GPT'S RESPONSE:")
print("=" * 80)
print(answer)
print("=" * 80)

# Display metadata
print("\nRESPONSE METADATA:")
print(f"Model used: {response.model}")
print(f"Finish reason: {response.choices[0].finish_reason}")
print(f"Input tokens: {response.usage.prompt_tokens}")
print(f"Output tokens: {response.usage.completion_tokens}")
print(f"Total tokens: {response.usage.total_tokens}")
