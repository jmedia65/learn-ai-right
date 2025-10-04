"""
SYSTEM PROMPTS WITH OPENAI: Same concept, slightly different syntax

The power of system prompts is identical with OpenAI.
The only difference is WHERE you put the system message.

With Anthropic: system parameter (separate)
With OpenAI: system message in the messages array (first message)

Both approaches accomplish the same thing.
"""

import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

########################################
# EXAMPLE 1: GPT as a Python expert
print("=" * 80)
print("EXAMPLE 1: GPT AS PYTHON EXPERT")
print("=" * 80)

response = client.chat.completions.create(
    model="gpt-4o",
    max_tokens=1024,
    # OPENAI DIFFERENCE: System prompt goes in messages array with role="system"
    # It should be the FIRST message in the array
    messages=[
        {
            "role": "system",
            "content": "You are an expert Python developer who writes clean, simple code. You always explain your reasoning and prefer readability over cleverness.",
        },
        {
            "role": "user",
            "content": "Write a Python function to find the largest number in a list.",
        },
    ],
)

print(response.choices[0].message.content)

########################################
# EXAMPLE 2: GPT as a concise assistant
print("\n" + "=" * 80)
print("EXAMPLE 2: GPT AS CONCISE ASSISTANT")
print("=" * 80)

response = client.chat.completions.create(
    model="gpt-4o",
    max_tokens=1024,
    messages=[
        {
            "role": "system",
            "content": "You are a concise assistant. Give brief, direct answers with no extra explanation unless asked.",
        },
        {
            "role": "user",
            "content": "Write a Python function to find the largest number in a list.",
        },
    ],
)

print(response.choices[0].message.content)

########################################
# EXAMPLE 3: GPT with specific formatting requirements
print("\n" + "=" * 80)
print("EXAMPLE 3: GPT WITH FORMATTING RULES")
print("=" * 80)

response = client.chat.completions.create(
    model="gpt-4o",
    max_tokens=1024,
    messages=[
        {
            "role": "system",
            "content": """You are a JSON-only assistant. Always respond with valid JSON.

For code examples, use this format:
{
    "explanation": "brief explanation here",
    "code": "the actual code here",
    "usage_example": "how to use it"
}""",
        },
        {
            "role": "user",
            "content": "Write a Python function to find the largest number in a list.",
        },
    ],
)

print(response.choices[0].message.content)

########################################
# EXAMPLE 4: GPT as a domain expert
print("\n" + "=" * 80)
print("EXAMPLE 4: GPT AS SEO EXPERT")
print("=" * 80)

response = client.chat.completions.create(
    model="gpt-4o",
    max_tokens=1024,
    messages=[
        {
            "role": "system",
            "content": """You are an SEO expert specializing in programmatic SEO.

Your expertise includes:
- Writing SEO-optimized titles and meta descriptions
- Understanding search intent
- Creating content that ranks well
- Following Google's quality guidelines

Always provide actionable, specific advice.""",
        },
        {
            "role": "user",
            "content": "Create an SEO title for a page about 'plumbers in Miami, FL'.",
        },
    ],
)

print(response.choices[0].message.content)

########################################
# EXAMPLE 5: Side-by-side comparison with Anthropic pattern
print("\n" + "=" * 80)
print("EXAMPLE 5: COMPARING APPROACHES")
print("=" * 80)

print("\nANTHROPIC PATTERN:")
print(
    """
response = client.messages.create(
    model="claude-sonnet-4-20250514",
    system="You are a helpful assistant.",  # <-- System prompt separate
    messages=[
        {"role": "user", "content": "Hello"}
    ]
)
"""
)

print("\nOPENAI PATTERN:")
print(
    """
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},  # <-- System in messages
        {"role": "user", "content": "Hello"}
    ]
)
"""
)

########################################

"""
KEY DIFFERENCES: ANTHROPIC VS OPENAI

1. SYSTEM PROMPT LOCATION:
   Anthropic: system parameter (separate from messages)
   OpenAI: First message in messages array with role="system"

2. WHY THE DIFFERENCE?
   - Just API design choices by each company
   - Functionally identical
   - Both achieve the same goal

3. WHICH IS BETTER?
   Neither! They're just different patterns.
   - Anthropic's separation is slightly cleaner (system is config, messages are conversation)
   - OpenAI's approach is more flexible (system can be treated like any message)

4. MULTI-TURN CONVERSATIONS:
   Both providers: System message stays at the beginning, applies to all turns
   
   Anthropic:
   system="You are helpful.",
   messages=[
       {"role": "user", "content": "Hi"},
       {"role": "assistant", "content": "Hello!"},
       {"role": "user", "content": "What's 2+2?"}
   ]
   
   OpenAI:
   messages=[
       {"role": "system", "content": "You are helpful."},
       {"role": "user", "content": "Hi"},
       {"role": "assistant", "content": "Hello!"},
       {"role": "user", "content": "What's 2+2?"}
   ]

5. BUILDING ABSTRACTION:
   Since you'll use BOTH APIs, you might want a simple wrapper:

   def call_llm(provider, system_prompt, user_message):
       if provider == "anthropic":
           return client.messages.create(
               model="claude-sonnet-4-20250514",
               system=system_prompt,
               messages=[{"role": "user", "content": user_message}]
           )
       elif provider == "openai":
           return client.chat.completions.create(
               model="gpt-4o",
               messages=[
                   {"role": "system", "content": system_prompt},
                   {"role": "user", "content": user_message}
               ]
           )

   This is the kind of simple abstraction that's useful - not a framework!

REAL-WORLD USAGE:

Your SaaS apps might have system prompts like:
- "You are a customer support agent for [Company]. You have access to user's order history."
- "You are a code reviewer. Review code for security issues, performance, and best practices."
- "You are a content writer. Create SEO-optimized content in a friendly, conversational tone."
- "You are a data analyst. Explain findings clearly and suggest actionable insights."

NEXT STEPS:
- Run this file and compare GPT's responses to Claude's (from file 003)
- Try the same system prompts with both providers
- Notice any differences in how they interpret instructions
- Build your own system prompts for your actual use cases

Remember: System prompts are configuration. User messages are requests.
Master this and you control the AI's behavior.
"""
