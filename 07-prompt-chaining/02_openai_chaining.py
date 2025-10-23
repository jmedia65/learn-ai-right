"""
PROMPT CHAINING - OPENAI GPT

Same pattern as Anthropic: Sequential API calls with logic between them.
The only difference is the API syntax.
"""

import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# =============================================================================
# EXAMPLE 1: LINEAR CHAIN (Research → Write → Edit)
# =============================================================================


def research_write_edit(topic: str) -> str:
    """
    A 3-step content creation workflow.

    Same pattern as Anthropic: Each step uses the previous step's output.
    """

    print(f"{'='*80}")
    print(f"STARTING WORKFLOW: {topic}")
    print(f"{'='*80}\n")

    # STEP 1: Research the topic
    print("📚 STEP 1: Research")
    print("-" * 80)

    research_response = client.chat.completions.create(
        model="gpt-4o",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": f"""Research this topic and provide:
- 5 key facts
- Main benefits
- Common use cases
- Important considerations

Topic: {topic}

Be concise and factual.""",
            }
        ],
    )

    research = research_response.choices[0].message.content
    print(f"✓ Research complete ({len(research)} characters)\n")
    print(f"Preview: {research[:200]}...\n")

    # STEP 2: Write article based on research
    print("✍️  STEP 2: Write Draft")
    print("-" * 80)

    draft_response = client.chat.completions.create(
        model="gpt-4o",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": f"""Based on this research, write a 200-word article:

{research}

Make it engaging and accessible to beginners.""",
            }
        ],
    )

    draft = draft_response.choices[0].message.content
    print(f"✓ Draft complete ({len(draft)} characters)\n")
    print(f"Preview: {draft[:200]}...\n")

    # STEP 3: Edit for clarity (with streaming!)
    print("✨ STEP 3: Edit & Polish (streaming...)")
    print("-" * 80)

    final = ""
    stream = client.chat.completions.create(
        model="gpt-4o",
        max_tokens=1024,
        stream=True,
        messages=[
            {
                "role": "user",
                "content": f"""Edit this article for clarity and flow:

{draft}

Improve readability while keeping the same length.
Output ONLY the final article, no commentary.""",
            }
        ],
    )

    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            text = chunk.choices[0].delta.content
            print(text, end="", flush=True)
            final += text

    print("\n\n✓ Editing complete\n")

    return final


# =============================================================================
# EXAMPLE 2: CONDITIONAL CHAIN (Classify → Branch)
# =============================================================================


def handle_support_request(user_message: str) -> str:
    """
    A conditional workflow that routes based on AI classification.

    Same pattern as Anthropic, just different API syntax.
    """

    print(f"\n{'='*80}")
    print(f"SUPPORT REQUEST: {user_message}")
    print(f"{'='*80}\n")

    # STEP 1: Classify the request
    print("🔍 STEP 1: Classify Request")
    print("-" * 80)

    classification_response = client.chat.completions.create(
        model="gpt-4o",
        max_tokens=100,
        messages=[
            {
                "role": "user",
                "content": f"""Classify this user message into ONE category:
- bug_report
- feature_request
- how_to_question
- billing_issue

User message: {user_message}

Output ONLY the category name, nothing else.""",
            }
        ],
    )

    category = classification_response.choices[0].message.content.strip()
    print(f"✓ Classified as: {category}\n")

    # STEP 2: Branch based on classification
    print(f"🎯 STEP 2: Handle '{category}'")
    print("-" * 80)

    if category == "bug_report":
        response = client.chat.completions.create(
            model="gpt-4o",
            max_tokens=500,
            messages=[
                {
                    "role": "user",
                    "content": f"""You're a support engineer. Respond to this bug report:

{user_message}

1. Acknowledge the issue
2. Ask for reproduction steps
3. Provide a temporary workaround if possible""",
                }
            ],
        )

    elif category == "feature_request":
        response = client.chat.completions.create(
            model="gpt-4o",
            max_tokens=500,
            messages=[
                {
                    "role": "user",
                    "content": f"""You're a product manager. Respond to this feature request:

{user_message}

1. Thank them for the suggestion
2. Explain if this is on the roadmap
3. Ask for more details about their use case""",
                }
            ],
        )

    else:
        response = client.chat.completions.create(
            model="gpt-4o",
            max_tokens=500,
            messages=[
                {
                    "role": "user",
                    "content": f"""You're a helpful support agent. Respond to:

{user_message}

Be friendly, helpful, and provide actionable next steps.""",
                }
            ],
        )

    final_response = response.choices[0].message.content
    print(f"✓ Response generated\n")

    return final_response


# =============================================================================
# RUN EXAMPLES
# =============================================================================

# Example 1: Linear chain
print("\n" + "="*80)
print("EXAMPLE 1: LINEAR CHAIN (Research → Write → Edit)")
print("="*80)

article = research_write_edit("FastAPI for building APIs")

print("="*80)
print("FINAL ARTICLE:")
print("="*80)
print(article)
print("="*80)

# Example 2: Conditional chain
print("\n" + "="*80)
print("EXAMPLE 2: CONDITIONAL CHAIN (Classify → Branch)")
print("="*80)

request1 = "The login button is broken on mobile devices"
response1 = handle_support_request(request1)

print("="*80)
print("RESPONSE:")
print("="*80)
print(response1)
print("="*80)

"""
WHAT YOU JUST LEARNED:

1. Prompt chaining is the same across providers
   - Sequential API calls with logic between them
   - Only difference: API method names
   - The PATTERN is universal

2. Real-world applications:
   - Customer support routing (classify → handle)
   - Content creation (research → write → edit)
   - Code review (analyze → suggest → refine)
   - Data analysis (extract → analyze → visualize)

3. Combining everything you've learned:
   Module 1: Basic API calls ✓
   Module 2: Conversation memory ✓
   Module 3: Tool calling ✓
   Module 4: RAG ✓
   Module 5: Conversational RAG ✓
   Module 6: Streaming ✓
   Module 7: Prompt chaining ✓

   You can mix and match these patterns:
   - Chain with RAG (retrieve docs in each step)
   - Chain with tools (call functions between steps)
   - Chain with streaming (stream final output)
   - Chain with memory (conversational workflows)

4. When to use frameworks:
   Frameworks like LangChain add:
   - Built-in error handling
   - Retry logic
   - Parallel execution
   - Logging and monitoring

   But you DON'T need them to understand or build AI systems.
   Now that you know the fundamentals, you can choose wisely.

CONGRATULATIONS! You've completed all 7 foundational concepts.
You now understand how production AI applications actually work.

Go build something amazing!
"""
