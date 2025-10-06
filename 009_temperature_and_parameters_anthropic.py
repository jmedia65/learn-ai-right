"""
TEMPERATURE & PARAMETERS: Control AI creativity and behavior

Temperature is THE most important parameter for controlling AI output.
Think of it as a creativity dial:
- Low temperature (0.0-0.3) = Consistent, focused, deterministic
- Medium temperature (0.7-1.0) = Balanced, natural
- High temperature (1.5-2.0) = Creative, random, unpredictable

This is how you make AI behave differently for different tasks.
"""

import os
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()
client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# We'll ask the same question with different temperatures

PROMPT = "Complete this sentence: The best thing about Python programming is"

print("=" * 80)
print("TEMPERATURE EXPERIMENTS")
print("=" * 80)
print(f"\nPrompt: '{PROMPT}'\n")
print("Watch how temperature changes the responses...\n")

# ============================================================================

print("-" * 80)
print("TEMPERATURE: 0.0 (Most deterministic)")
print("-" * 80)

response = client.messages.create(
    model="claude-4-sonnet-20250514",
    max_tokens=1024,
    temperature=0.0,  # Almost always the same response
    messages=[{"role": "user", "content": PROMPT}],
)

print(response.content[0].text)

# Run this 3 times to see the consistency
print("\nRunning same prompt 3 times with temperature=0.0:")
for i in range(1, 4):
    response = client.messages.create(
        model="claude-4-sonnet-20250514",
        max_tokens=1024,
        temperature=0.0,  # Almost always the same response
        messages=[{"role": "user", "content": PROMPT}],
    )
    print(f"\n{i}. {response.content[0].text[:300]}...")

print("\n^ Notice: Nearly identical responses!")

# ============================================================================
print("\n" + "-" * 80)
print("TEMPERATURE: 0.7 (Balanced - DEFAULT)")
print("-" * 80)

response = client.messages.create(
    model="claude-4-sonnet-20250514",
    max_tokens=200,
    temperature=0.7,  # This is the default if you don't specify
    messages=[{"role": "user", "content": PROMPT}],
)

print(response.content[0].text)

print("\nRunning same prompt 3 times with temperature=0.7:")
for i in range(1, 4):
    response = client.messages.create(
        model="claude-4-sonnet-20250514",
        max_tokens=200,
        temperature=0.7,  # This is the default if you don't specify
        messages=[{"role": "user", "content": PROMPT}],
    )
    print(f"\n{i}. {response.content[0].text[:300]}...")

print("\n^ Notice: Similar but with variation!")

# ============================================================================
print("\n" + "-" * 80)
print("TEMPERATURE: 1.0 (Creative)")
print("-" * 80)

response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=200,
    temperature=1.0,  # More creative, more variety
    messages=[{"role": "user", "content": PROMPT}],
)

print(response.content[0].text)

print("\nRunning same prompt 3 times with temperature=1.0:")
for i in range(1, 4):
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=200,
        temperature=1.0,
        messages=[{"role": "user", "content": PROMPT}],
    )
    print(f"\n{i}. {response.content[0].text[:300]}...")

print("\n^ Notice: More diverse responses!")

# ============================================================================
print("\n" + "=" * 80)
print("REAL-WORLD USE CASES")
print("=" * 80)

# ------------------------------------------------------------------
# USE CASE 1: Data extraction (need consistency)
print("\n" + "-" * 80)
print("USE CASE 1: DATA EXTRACTION (temperature=0.0)")
print("-" * 80)

extraction_prompt = """Extract the following information from this text:
Text: "John Smith, age 35, lives in Miami, FL. His email is john@example.com"

Return in this format:
Name:
Age:
City:
Email: """

response = client.messages.create(
    model="claude-4-sonnet-20250514",
    max_tokens=200,
    temperature=0.0,
    messages=[{"role": "user", "content": extraction_prompt}],
)

print(response.content[0].text)
print("\n^ Low temperature ensures consistent, reliable extraction")

# ------------------------------------------------------------------
# USE CASE 2: Creative writing (need variety)
print("\n" + "-" * 80)
print("USE CASE 2: CREATIVE WRITING (temperature=1.0)")
print("-" * 80)

creative_prompt = "Write the opening line of a sci-fi short story."

response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=200,
    temperature=1.0,  # We want creative, unique ideas
    messages=[{"role": "user", "content": creative_prompt}],
)

print(response.content[0].text)
print("\n^ High temperature gives creative, unexpected results")

# ------------------------------------------------------------------
# USE CASE 3: Technical explanations (balanced)
print("\n" + "-" * 80)
print("USE CASE 3: TECHNICAL EXPLANATION (temperature=0.3)")
print("-" * 80)

technical_prompt = "Explain how a binary search tree works."

response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=300,
    temperature=0.3,  # Balanced: accurate but natural
    messages=[{"role": "user", "content": technical_prompt}],
)

print(response.content[0].text)
print("\n^ Low-medium temperature for accurate, consistent technical content")


# ============================================================================
print("\n" + "=" * 80)
print("OTHER PARAMETERS: TOP_P")
print("=" * 80)

print(
    """
TOP_P (nucleus sampling): Alternative to temperature
- Controls diversity by probability mass
- Range: 0.0 to 1.0
- top_p=0.1: Very focused (only top 10% of probable words)
- top_p=0.9: More diverse (top 90% of probable words)

IMPORTANT: Use EITHER temperature OR top_p, not both!
Anthropic recommends using temperature primarily.
"""
)

# Example with top_p
print("\n" + "-" * 80)
print("EXAMPLE: Using top_p instead of temperature")
print("-" * 80)

response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=200,
    top_p=0.1,  # Very focused
    messages=[{"role": "user", "content": PROMPT}],
)

print(f"With top_p=0.1 (focused):\n{response.content[0].text}")

response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=200,
    top_p=0.9,  # More diverse
    messages=[{"role": "user", "content": PROMPT}],
)

print(f"\nWith top_p=0.9 (diverse):\n{response.content[0].text}")

# ============================================================================

"""
COMPREHENSIVE GUIDE TO PARAMETERS:

1. TEMPERATURE (Most Important!)
   Range: 0.0 to 1.0
   
   temperature=0.0  → Deterministic, consistent, focused
   - Use for: Data extraction, structured output, technical docs
   - Example: "Extract name and email from this text"
   
   temperature=0.3  → Slightly varied but mostly consistent
   - Use for: Technical explanations, customer support, FAQs
   - Example: "Explain how OAuth works"
   
   temperature=0.7  → Balanced (DEFAULT)
   - Use for: General conversation, Q&A, most use cases
   - Example: "Help me plan my vacation"
   
   temperature=1.0  → Creative, diverse
   - Use for: Creative writing, brainstorming, marketing copy
   - Example: "Write a poem about AI"

2. TOP_P (Nucleus Sampling)
   Range: 0.0 to 1.0
   
   top_p=0.1  → Very focused (top 10% probability mass)
   top_p=0.5  → Moderately focused
   top_p=0.9  → Diverse (DEFAULT)
   
   RULE: Use temperature OR top_p, not both
   Temperature is usually better/simpler

3. TOP_K (Anthropic-specific)
   Range: 1 to infinity (default varies by model)
   
   Limits vocabulary to top K most likely tokens
   Example: top_k=40 means only consider 40 most likely next words
   
   Rarely need to adjust this - default is fine

4. MAX_TOKENS
   Range: 1 to model's maximum (200K for Claude Sonnet 4)
   
   Controls OUTPUT length, not input
   This is NOT about cost - it's about response length
   
   max_tokens=50    → Very short response (a few sentences)
   max_tokens=1024  → Medium response (few paragraphs)
   max_tokens=4096  → Long response (multiple pages)

5. STOP SEQUENCES
   List of strings that stop generation
   
   stop_sequences=["END", "\n\n\n"]
   
   When Claude generates any of these, it stops
   Useful for structured output

DECISION TREE FOR PARAMETERS:

Q: What task am I doing?

├─ Data extraction / Structured output
│  └─ temperature=0.0, max_tokens=500
│
├─ Technical documentation / Support
│  └─ temperature=0.3, max_tokens=2000
│
├─ General conversation / Q&A
│  └─ temperature=0.7 (default), max_tokens=1024
│
├─ Creative writing / Brainstorming
  └─ temperature=1.0, max_tokens=2000

COMMON MISTAKES:

❌ Using high temperature for structured tasks
   (Results in inconsistent formatting)

❌ Using low temperature for creative tasks
   (Results in boring, repetitive content)

❌ Combining temperature and top_p
   (Pick one! Temperature is usually better)

❌ Setting max_tokens too low
   (Responses get cut off mid-sentence)

❌ Thinking temperature=0.0 is always best
   (It makes responses robotic and unnatural)

✅ Use temperature=0.0-0.3 for factual/structured tasks
✅ Use temperature=0.7 for most conversational tasks
✅ Use temperature=1.0 for creative tasks
✅ Set max_tokens based on expected response length
✅ Start with defaults, then adjust based on results

REAL-WORLD EXAMPLES:

# Customer Support Bot
response = client.messages.create(
    model="claude-sonnet-4-20250514",
    temperature=0.3,  # Consistent but natural
    max_tokens=1024,
    system="You are a helpful customer support agent.",
    messages=[...]
)

# Creative Story Generator
response = client.messages.create(
    model="claude-sonnet-4-20250514",
    temperature=1.0,  # Creative and varied
    max_tokens=4096,
    system="You are a creative fiction writer.",
    messages=[...]
)

# JSON Data Extractor
response = client.messages.create(
    model="claude-sonnet-4-20250514",
    temperature=0.0,  # Deterministic output
    max_tokens=2048,
    system="Extract data and return valid JSON only.",
    messages=[...]
)

# Code Explainer
response = client.messages.create(
    model="claude-sonnet-4-20250514",
    temperature=0.3,  # Accurate but readable
    max_tokens=2048,
    system="You are a helpful programming tutor.",
    messages=[...]
)

TESTING TEMPERATURE:

To find the right temperature for your use case:
1. Start with temperature=0.7 (default)
2. Run the same prompt 5 times
3. Too similar? Increase temperature
4. Too random? Decrease temperature
5. Iterate until you find the sweet spot

Pro tip: Different models have different "temperature personalities"
- Some models are more creative at temp=0.7
- Others need temp=1.0 for similar creativity
- Always test with your specific model

NEXT STEPS:
- Run this file and observe temperature differences
- Try your own prompts with different temperatures
- Find the right temperature for your use cases
- Remember: When in doubt, start with 0.7!

Temperature is your most powerful tool for controlling AI behavior.
Master it, and you control the AI.
"""
