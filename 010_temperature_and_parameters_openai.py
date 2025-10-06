"""
TEMPERATURE & PARAMETERS WITH OPENAI

Good news: Temperature works EXACTLY the same with OpenAI!
The concepts are identical, just slightly different parameter names.

OpenAI has one additional useful parameter: seed (for reproducibility)
"""

import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

PROMPT = "Complete this sentence: The best thing about Python programming is"

print("=" * 80)
print("TEMPERATURE EXPERIMENTS WITH OPENAI")
print("=" * 80)
# print(f"\nPrompt: '{PROMPT}'\n")

# ============================================================================
# print("-" * 80)
# print("TEMPERATURE: 0.0 (Most deterministic)")
# print("-" * 80)

# response = client.chat.completions.create(
#     model="gpt-4o",
#     max_tokens=200,
#     temperature=0.0,  # Same as Anthropic!
#     messages=[{"role": "user", "content": PROMPT}],
# )

# print(response.choices[0].message.content)

# print("\nRunning same prompt 3 times with temperature=0.0:")
# for i in range(1, 4):
#     response = client.chat.completions.create(
#         model="gpt-4o",
#         max_tokens=200,
#         temperature=0.0,  # Same as Anthropic!
#         messages=[{"role": "user", "content": PROMPT}],
#     )

#     print(f"\n{i}: {response.choices[0].message.content[:150]}")

# print("\n^ Notice: Nearly identical!")

# ============================================================================
# print("\n" + "-" * 80)
# print("TEMPERATURE: 1.0 (Default for OpenAI)")
# print("-" * 80)

# response = client.chat.completions.create(
#     model="gpt-4o",
#     max_tokens=200,
#     temperature=1.0,  # OpenAI's default is 1.0 (vs Anthropic's 0.7)
#     messages=[{"role": "user", "content": PROMPT}],
# )

# print(response.choices[0].message.content)

# print("\nRunning same prompt 3 times with temperature=1.0:")
# for i in range(1, 4):
#     response = client.chat.completions.create(
#         model="gpt-4o",
#         max_tokens=200,
#         temperature=1.0,
#         messages=[{"role": "user", "content": PROMPT}],
#     )
#     print(f"{i}. {response.choices[0].message.content[:80]}...")

# print("\n^ Notice: More varied!")

# ============================================================================
# print("\n" + "-" * 80)
# print("TEMPERATURE: 2.0 (Maximum creativity)")
# print("-" * 80)

# response = client.chat.completions.create(
#     model="gpt-4o",
#     max_tokens=200,
#     # Don't run temp 2.0 - When I did, I received bunch of gibberish
#     temperature=2.0,  # OpenAI allows up to 2.0
#     messages=[{"role": "user", "content": PROMPT}],
# )

# print(response.choices[0].message.content)
# print("\n^ Very creative/random!")

# ============================================================================
# print("\n" + "=" * 80)
# print("OPENAI-SPECIFIC: SEED PARAMETER (Reproducibility)")
# print("=" * 80)

# print(
#     """
# OpenAI has a special 'seed' parameter for reproducibility.
# With the same seed, you get more consistent results (even with temp > 0).

# This is useful for:
# - Testing and debugging
# - Comparing different prompts
# - Ensuring consistent behavior in production
# """
# )

# print("\n" + "-" * 80)
# print("EXAMPLE: Using seed for reproducibility")
# print("-" * 80)

# # Without seed (random)
# print("\nWithout seed (temperature=1.0) - 3 runs:")
# for i in range(1, 4):
#     response = client.chat.completions.create(
#         model="gpt-4o",
#         temperature=1.0,
#         messages=[{"role": "user", "content": "Say hello in a creative way."}],
#     )
#     print(f"\n{i}. {response.choices[0].message.content}")

# # With seed (more consistent)
# print("\n\nWith seed=12345 (temperature=1.0) - 3 runs:")
# for i in range(1, 4):
#     response = client.chat.completions.create(
#         model="gpt-4o",
#         temperature=1.0,
#         seed=12345,  # Same seed = more consistent
#         messages=[{"role": "user", "content": "Say hello in a creative way."}],
#     )
#     print(f"\n{i}. {response.choices[0].message.content}")

# print("\n^ With seed, responses are more similar even at temp=1.0!")

# ============================================================================
# print("\n" + "=" * 80)
# print("REAL-WORLD USE CASES")
# print("=" * 80)

# USE CASE 1: JSON extraction (need consistency)
# print("\n" + "-" * 80)
# print("USE CASE 1: JSON EXTRACTION (temperature=0.0)")
# print("-" * 80)

# extraction_prompt = """Extract this as JSON:
# "Product: iPhone 15, Price: $999, Stock: 50 units"

# Return only valid JSON."""

# response = client.chat.completions.create(
#     model="gpt-4o",
#     temperature=0.0,  # Consistent JSON structure
#     messages=[{"role": "user", "content": extraction_prompt}],
# )

# print(response.choices[0].message.content)

# # USE CASE 2: Marketing copy (need creativity)
# print("\n" + "-" * 80)
# print("USE CASE 2: MARKETING COPY (temperature=1.2)")
# print("-" * 80)

# marketing_prompt = "Write a catchy tagline for a new fitness app."

# response = client.chat.completions.create(
#     model="gpt-4o",
#     temperature=1.2,  # Creative and punchy
#     messages=[{"role": "user", "content": marketing_prompt}],
# )

# print(response.choices[0].message.content)

# # USE CASE 3: Code generation (balanced)
# print("\n" + "-" * 80)
# print("USE CASE 3: CODE GENERATION (temperature=0.2)")
# print("-" * 80)

# code_prompt = "Write a Python function to check if a number is prime."

# response = client.chat.completions.create(
#     model="gpt-4o",
#     temperature=0.2,  # Consistent, reliable code
#     max_tokens=500,
#     messages=[{"role": "user", "content": code_prompt}],
# )

# print(response.choices[0].message.content)

# ============================================================================
# print("\n" + "=" * 80)
# print("ALL OPENAI PARAMETERS")
# print("=" * 80)

# print(
#     """
# Complete parameter reference:

# response = client.chat.completions.create(
#     model="gpt-4o",

#     # Core parameters (same as Anthropic)
#     temperature=0.7,        # 0.0-2.0, controls randomness
#     max_tokens=1024,        # Max response length
#     top_p=0.9,             # Alternative to temperature (0.0-1.0)

#     # OpenAI-specific parameters
#     seed=12345,            # For reproducibility (integer)
#     frequency_penalty=0.0,  # -2.0 to 2.0, penalize repeated tokens
#     presence_penalty=0.0,   # -2.0 to 2.0, encourage new topics

#     # Stop sequences
#     stop=["END", "\\n\\n"],  # Stop generation at these strings

#     messages=[...]
# )
# """
# )

# ============================================================================
# print("\n" + "=" * 80)
# print("FREQUENCY & PRESENCE PENALTIES (Advanced)")
# print("=" * 80)

# print(
#     """
# These are unique to OpenAI:

# FREQUENCY_PENALTY: Reduces repetition of tokens
# - Range: -2.0 to 2.0
# - Positive: Discourages repeating tokens
# - Use for: Avoiding repetitive text

# PRESENCE_PENALTY: Encourages new topics
# - Range: -2.0 to 2.0
# - Positive: Encourages talking about new topics
# - Use for: Diverse, exploratory responses
# """
# )

# # Example with penalties
# print("\n" + "-" * 80)
# print("EXAMPLE: Without penalties (might repeat)")
# print("-" * 80)

# response = client.chat.completions.create(
#     model="gpt-4o",
#     temperature=0.7,
#     messages=[{"role": "user", "content": "List 10 creative app ideas."}],
# )

# print(response.choices[0].message.content)

# print("\n" + "-" * 80)
# print("EXAMPLE: With frequency_penalty=1.0 (less repetition)")
# print("-" * 80)

# response = client.chat.completions.create(
#     model="gpt-4o",
#     temperature=0.7,
#     frequency_penalty=1.0,  # Penalize repetition
#     messages=[{"role": "user", "content": "List 10 creative app ideas."}],
# )

# print(response.choices[0].message.content)

# ============================================================================
# ============================================================================
print("\n" + "=" * 80)
print("ANTHROPIC VS OPENAI: PARAMETER COMPARISON")
print("=" * 80)

print(
    """
IDENTICAL PARAMETERS:
--------------------
temperature     ✅ Same (0.0-2.0 range, same meaning)
max_tokens      ✅ Same (controls output length)
top_p           ✅ Same (0.0-1.0, nucleus sampling)
stop sequences  ✅ Same (though syntax differs slightly)

OPENAI-SPECIFIC:
----------------
seed               → For reproducibility
frequency_penalty  → Reduce repetition
presence_penalty   → Encourage new topics

ANTHROPIC-SPECIFIC:
-------------------
top_k              → Vocabulary limiting (rarely needed)

DEFAULT VALUES:
---------------
Anthropic: temperature=0.7 (if not specified)
OpenAI:    temperature=1.0 (if not specified)

So OpenAI is slightly more "creative" by default!

RECOMMENDATION:
Always explicitly set temperature for consistent behavior across providers.
"""
)

"""
COMPREHENSIVE OPENAI PARAMETER GUIDE:

1. TEMPERATURE (Most Important)
   Same as Anthropic: 0.0 (deterministic) to 2.0 (very random)
   
   Pro tip: OpenAI's GPT-4o tends to be more creative than Claude
   at the same temperature, so you might use slightly lower temps.

2. SEED (OpenAI Exclusive)
   Integer value for reproducibility
   
   Use cases:
   - Testing: Same seed = easier to compare results
   - Debugging: Reproduce exact behavior
   - Demos: Consistent outputs for presentations
   
   Example:
   seed=42  # Your favorite number

3. FREQUENCY_PENALTY
   Range: -2.0 to 2.0
   
   frequency_penalty=0.0   → No penalty (default)
   frequency_penalty=0.5   → Mild penalty on repetition
   frequency_penalty=1.0   → Strong penalty on repetition
   frequency_penalty=2.0   → Maximum penalty (might hurt quality)
   
   Use for:
   - Long-form content (essays, articles)
   - Lists that shouldn't repeat
   - Creative writing
   
   Avoid for:
   - Technical docs (some repetition is natural)
   - Code generation (patterns repeat legitimately)

4. PRESENCE_PENALTY
   Range: -2.0 to 2.0
   
   presence_penalty=0.0   → No penalty (default)
   presence_penalty=0.5   → Mild encouragement for new topics
   presence_penalty=1.0   → Strong encouragement for diversity
   
   Use for:
   - Brainstorming sessions
   - Exploratory conversations
   - Diverse content generation
   
   Avoid for:
   - Focused technical answers
   - When you want deep dives on one topic

5. STOP SEQUENCES
   List of strings that halt generation
   
   stop=["END"]              → Stop at "END"
   stop=["\\n\\n\\n", "---"] → Stop at triple newline or dashes
   
   Use for:
   - Structured output (stop at delimiter)
   - Preventing overlong responses
   - Format enforcement

PRACTICAL COMBINATIONS:

# Consistent JSON extraction
response = client.chat.completions.create(
    model="gpt-4o",
    temperature=0.0,
    seed=42,  # Extra consistency
    max_tokens=1000,
    messages=[...]
)

# Creative brainstorming
response = client.chat.completions.create(
    model="gpt-4o",
    temperature=1.2,
    presence_penalty=0.6,  # Encourage diverse ideas
    frequency_penalty=0.3,  # Don't repeat same ideas
    max_tokens=2000,
    messages=[...]
)

# Technical documentation
response = client.chat.completions.create(
    model="gpt-4o",
    temperature=0.3,
    frequency_penalty=0.0,  # Allow natural repetition
    max_tokens=4000,
    messages=[...]
)

# Marketing copy (multiple variants)
for i in range(5):
    response = client.chat.completions.create(
        model="gpt-4o",
        temperature=1.0,
        seed=i,  # Different seed = different variant
        frequency_penalty=0.8,  # Avoid clichés
        messages=[...]
    )

TESTING STRATEGY:

To find optimal parameters for your use case:

1. Baseline test (defaults):
   temperature=1.0, no penalties

2. Test temperature:
   Try 0.0, 0.3, 0.7, 1.0, 1.5
   Pick based on creativity needs

3. Add penalties if needed:
   If repetitive → frequency_penalty=0.5
   If too focused → presence_penalty=0.5

4. Add seed if needed:
   For testing/debugging → seed=42

5. Iterate based on results

COMMON MISTAKES:

❌ Using high frequency_penalty for code (breaks patterns)
❌ Using seed in production (defeats randomness)
❌ Combining high temp + high penalties (conflicts)
❌ Setting penalties too high (>1.0 usually hurts quality)

✅ Start with temperature only
✅ Add penalties only if specific issues
✅ Use seed only for testing/debugging
✅ Test thoroughly before production

NEXT STEPS:
- Run this file and observe temperature effects
- Compare GPT vs Claude at same temperatures
- Experiment with seed for reproducibility
- Try frequency/presence penalties
- Find your optimal settings for your use cases

You now control AI behavior at a deep level!
"""
