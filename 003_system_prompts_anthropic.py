"""
SYSTEM PROMPTS: Control Claude's behavior, personality, and expertise

A system prompt is like giving Claude instructions about WHO it should be
and HOW it should behave throughout the conversation.

Think of it as:
- User messages = what you want Claude to do
- System prompt = who Claude should be while doing it

This is one of the most powerful tools for building AI applications.
"""

import os
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()
client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

########################################
# EXAMPLE 1: Claude as a Python expert
print("=" * 80)
print("EXAMPLE 1: CLAUDE AS PYTHON EXPERT")
print("=" * 80)

response = client.messages.create(
    model="claude-4-sonnet-20250514",
    max_tokens=1024,
    # SYSTEM PROMPT goes here - separate from messages
    # This sets Claude's role/behavior for the entire conversation
    system="You are an expert Python developer who writes clean, simple code. You always explain your reasoning and prefer readability over cleverness.",
    messages=[
        {
            "role": "user",
            "content": "Write a function to find the largest number in an list",
        }
    ],
)

print(response.content[0].text)

########################################
# EXAMPLE 2: Claude as a concise assistant
print("\n" + "=" * 80)
print("EXAMPLE 2: CLAUDE AS CONCISE ASSISTANT")
print("=" * 80)

response = client.messages.create(
    model="claude-4-sonnet-20250514",
    max_tokens=1024,
    # Different system prompt = different behavior
    system="You are a concise assistant. Give brief, direct answers with no extra explanation unless asked.",
    messages=[
        {
            "role": "user",
            "content": "Write a Python function to find the largest number in a list.",
        }
    ],
)

print(response.content[0].text)

########################################
# EXAMPLE 3: Claude with specific formatting requirements
print("\n" + "=" * 80)
print("EXAMPLE 3: CLAUDE WITH FORMATTING RULES")
print("=" * 80)

response = client.messages.create(
    model="claude-4-sonnet-20250514",
    max_tokens=1024,
    system="""You are a JSON-only assistant. Always respond with valid JSON.

For code examples, use this format:
{
    "explanation": "brief explanation here",
    "code": "the actual code here",
    "usage_example": "how to use it"
}""",
    messages=[
        {
            "role": "user",
            "content": "Write a function to find the largest number in a list.",
        }
    ],
)

print(response.content[0].text)

########################################
# EXAMPLE 4: Claude as a domain expert (real-world use case)
print("\n" + "=" * 80)
print("EXAMPLE 4: CLAUDE AS SEO EXPERT")
print("=" * 80)

response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    # Real-world example: building an SEO tool
    system="""You are an SEO expert specializing in programmatic SEO.
    
Your expertise includes:
- Writing SEO-optimized titles and meta descriptions
- Understanding search intent
- Creating content that ranks well
- Following Google's quality guidelines

Always provide actionable, specific advice.""",
    messages=[
        {
            "role": "user",
            "content": "Create an SEO title for a page about 'plumbers in Miami, FL'.",
        }
    ],
)

print(response.content[0].text)

########################################

"""
KEY INSIGHTS ABOUT SYSTEM PROMPTS:

1. WHEN TO USE SYSTEM PROMPTS:
   ✅ Setting Claude's role/expertise (doctor, lawyer, coder, etc.)
   ✅ Defining output format requirements (JSON, XML, specific structure)
   ✅ Establishing conversation rules (concise, detailed, formal, casual)
   ✅ Providing context that applies to ALL messages (company info, guidelines)

2. SYSTEM VS USER MESSAGES:
   - System: "You are a Python expert" (who Claude is)
   - User: "Write a function" (what you want Claude to do)
   
3. SYSTEM PROMPTS ARE PERSISTENT:
   - In multi-turn conversations, the system prompt applies to every turn
   - You don't need to repeat it in each user message
   - Think of it as "configuration" for the conversation

4. REAL-WORLD APPLICATIONS:
   - Customer support chatbot: "You are a helpful support agent for [Company]..."
   - Code reviewer: "You are a senior developer reviewing code for..."
   - Content generator: "You are a copywriter specializing in..."
   - Data analyzer: "You are a data scientist who explains findings clearly..."

5. BEST PRACTICES:
   ✅ Be specific about Claude's role
   ✅ Include relevant expertise/knowledge areas
   ✅ Specify output format if needed
   ✅ Set tone/style expectations
   ✅ Keep it focused (one clear role, not five different personas)

6. SYSTEM PROMPTS + TOKENS:
   - System prompts count toward your token usage
   - But with Anthropic's prompt caching (we'll cover later), 
     you can cache system prompts to save money on repeated calls

COMMON PATTERNS:

Pattern 1: Role-based
system="You are a [ROLE] who [EXPERTISE]. You always [BEHAVIOR]."

Pattern 2: Format enforcement
system="You are an assistant that only responds in [FORMAT]. Never use [OTHER FORMAT]."

Pattern 3: Domain expert
system="You are an expert in [DOMAIN] with experience in [SPECIFICS]. You help users by [METHOD]."

Pattern 4: Structured assistant
system="You are an assistant that follows these rules:
1. [RULE 1]
2. [RULE 2]
3. [RULE 3]"

NEXT STEPS:
- Run this file and see how different system prompts change Claude's behavior
- Try writing your own system prompts for different use cases
- Experiment with different levels of specificity
- Notice how the SAME user message gets DIFFERENT responses with different system prompts

This is the foundation for building AI applications with personality and purpose.
"""
