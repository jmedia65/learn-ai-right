"""
PROMPT CHAINING - OPENAI GPT (Responses API)

Same pattern as Anthropic: sequential API calls with logic between them.
Only API syntax differs.
"""

import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
MODEL = os.getenv("OPENAI_MODEL", "gpt-6-luna")
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# =============================================================================
# EXAMPLE 1: LINEAR CHAIN (Research -> Write -> Edit)
# =============================================================================


def research_write_edit(topic: str) -> str:
    """
    A 3-step content creation workflow.

    Same pattern as Anthropic: each step uses previous output as input.
    """

    print(f"{'='*80}")
    print(f"STARTING WORKFLOW: {topic}")
    print(f"{'='*80}\n")

    # STEP 1: Research the topic
    print("📚 STEP 1: Research")
    print("-" * 80)

    research_response = client.responses.create(
        model=MODEL,
        max_output_tokens=4096,
        input=f"""Research this topic and provide:
- 5 key facts
- Main benefits
- Common use cases
- Important considerations

Topic: {topic}

Be concise and factual.""",
    )
    if research_response.status != "completed":
        raise RuntimeError(f"Research did not complete: {research_response.status}")

    research = research_response.output_text
    print(f"✓ Research complete ({len(research)} characters)\n")
    print(f"Preview: {research[:200]}...\n")

    # STEP 2: Write article based on research
    print("✍️  STEP 2: Write Draft")
    print("-" * 80)

    draft_response = client.responses.create(
        model=MODEL,
        max_output_tokens=4096,
        input=f"""Based on this research, write a 200-word article:

{research}

Make it engaging and accessible to beginners.""",
    )
    if draft_response.status != "completed":
        raise RuntimeError(f"Draft did not complete: {draft_response.status}")

    draft = draft_response.output_text
    print(f"✓ Draft complete ({len(draft)} characters)\n")
    print(f"Preview: {draft[:200]}...\n")

    # STEP 3: Edit for clarity (with streaming)
    print("✨ STEP 3: Edit & Polish (streaming...)")
    print("-" * 80)

    final = ""
    stream = client.responses.create(
        model=MODEL,
        max_output_tokens=4096,
        input=f"""Edit this article for clarity and flow:

{draft}

Improve readability while keeping the same length.
Output ONLY the final article, no commentary.""",
        stream=True,
    )

    completed = False
    for event in stream:
        if event.type == "response.output_text.delta":
            print(event.delta, end="", flush=True)
            final += event.delta
        elif event.type == "response.completed":
            completed = True
        elif event.type in ("response.failed", "response.incomplete", "error"):
            raise RuntimeError(f"Edit stream ended with {event.type}")

    if not completed:
        raise RuntimeError("Edit stream ended before response.completed")

    print("\n\n✓ Editing complete\n")

    return final


# =============================================================================
# EXAMPLE 2: CONDITIONAL CHAIN (Classify -> Branch)
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

    classification_response = client.responses.create(
        model=MODEL,
        max_output_tokens=4096,
        input=f"""Classify this user message into ONE category:
- bug_report
- feature_request
- how_to_question
- billing_issue

User message: {user_message}

Output ONLY the category name, nothing else.""",
    )
    if classification_response.status != "completed":
        raise RuntimeError(f"Classification did not complete: {classification_response.status}")

    category = classification_response.output_text.strip()
    print(f"✓ Classified as: {category}\n")

    # STEP 2: Branch based on classification
    print(f"🎯 STEP 2: Handle '{category}'")
    print("-" * 80)

    if category == "bug_report":
        response = client.responses.create(
            model=MODEL,
            max_output_tokens=4096,
            input=f"""You're a support engineer. Respond to this bug report:

{user_message}

1. Acknowledge the issue
2. Ask for reproduction steps
3. Provide a temporary workaround if possible""",
        )

    elif category == "feature_request":
        response = client.responses.create(
            model=MODEL,
            max_output_tokens=4096,
            input=f"""You're a product manager. Respond to this feature request:

{user_message}

1. Thank them for the suggestion
2. Explain if this is on the roadmap
3. Ask for more details about their use case""",
        )

    else:
        response = client.responses.create(
            model=MODEL,
            max_output_tokens=4096,
            input=f"""You're a helpful support agent. Respond to:

{user_message}

Be friendly, helpful, and provide actionable next steps.""",
        )

    if response.status != "completed":
        raise RuntimeError(f"Support response did not complete: {response.status}")
    final_response = response.output_text
    print("✓ Response generated\n")

    return final_response


# =============================================================================
# RUN EXAMPLES
# =============================================================================

print("\n" + "=" * 80)
print("EXAMPLE 1: LINEAR CHAIN (Research -> Write -> Edit)")
print("=" * 80)

article = research_write_edit("FastAPI for building APIs")

print("=" * 80)
print("FINAL ARTICLE:")
print("=" * 80)
print(article)
print("=" * 80)

print("\n" + "=" * 80)
print("EXAMPLE 2: CONDITIONAL CHAIN (Classify -> Branch)")
print("=" * 80)

request1 = "The login button is broken on mobile devices"
response1 = handle_support_request(request1)

print("=" * 80)
print("RESPONSE:")
print("=" * 80)
print(response1)
print("=" * 80)

"""
WHAT YOU JUST LEARNED:

1. Prompt chaining is still sequential API calls
   - Step outputs become next step inputs
   - Conditional routing is just branch logic around calls

2. Responses API keeps chaining straightforward
   - Single method: client.responses.create()
   - Unified extraction: response.output_text

3. You can combine everything you've learned
   - Chaining + streaming
   - Chaining + RAG
   - Chaining + tool calling

You've completed steps 1-9 of the curriculum.
NEXT STEP: Build the full integration project in step 10 (OpenAI capstone).
"""
