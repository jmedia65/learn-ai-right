"""
PROMPT CHAINING - ANTHROPIC CLAUDE

"Multi-agent systems" and "AI orchestration" sound complex.
The reality: Call AI → Process → Call AI → Process → Call AI

This is just sequential API calls with logic between them.
"""

import os
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()
client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# =============================================================================
# EXAMPLE 1: LINEAR CHAIN (Research → Write → Edit)
# =============================================================================


def research_write_edit(topic: str) -> str:
    """
    A 3-step content creation workflow.

    This is what the industry calls an "AI agent" or "AI workflow."
    It's just 3 API calls with logic between them.

    Pattern: Each step uses the previous step's output as input.
    """

    print(f"{'='*80}")
    print(f"STARTING WORKFLOW: {topic}")
    print(f"{'='*80}\n")

    # STEP 1: Research the topic
    print("📚 STEP 1: Research")
    print("-" * 80)

    research_response = client.messages.create(
        model="claude-sonnet-4-20250514",
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

    research = research_response.content[0].text
    print(f"✓ Research complete ({len(research)} characters)\n")
    print(f"Preview: {research[:200]}...\n")

    # STEP 2: Write article based on research
    # The research output becomes input for this step
    print("✍️  STEP 2: Write Draft")
    print("-" * 80)

    draft_response = client.messages.create(
        model="claude-sonnet-4-20250514",
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

    draft = draft_response.content[0].text
    print(f"✓ Draft complete ({len(draft)} characters)\n")
    print(f"Preview: {draft[:200]}...\n")

    # STEP 3: Edit for clarity (with streaming for better UX!)
    # The draft becomes input for this step
    print("✨ STEP 3: Edit & Polish (streaming...)")
    print("-" * 80)

    final = ""
    with client.messages.stream(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": f"""Edit this article for clarity and flow:

{draft}

Improve readability while keeping the same length.
Output ONLY the final article, no commentary.""",
            }
        ],
    ) as stream:
        for text in stream.text_stream:
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

    Pattern:
    1. Classify the input
    2. Branch to different handlers based on classification
    3. Return appropriate response

    This is how customer support bots work.
    """

    print(f"\n{'='*80}")
    print(f"SUPPORT REQUEST: {user_message}")
    print(f"{'='*80}\n")

    # STEP 1: Classify the request
    print("🔍 STEP 1: Classify Request")
    print("-" * 80)

    classification_response = client.messages.create(
        model="claude-sonnet-4-20250514",
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

    category = classification_response.content[0].text.strip()
    print(f"✓ Classified as: {category}\n")

    # STEP 2: Branch based on classification
    # Different logic for different categories
    print(f"🎯 STEP 2: Handle '{category}'")
    print("-" * 80)

    if category == "bug_report":
        # Handle bug reports
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
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
        # Handle feature requests
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
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
        # Default handler for other categories
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
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

    final_response = response.content[0].text
    print(f"✓ Response generated\n")

    return final_response


# =============================================================================
# RUN EXAMPLES
# =============================================================================

# Example 1: Linear chain
print("\n" + "=" * 80)
print("EXAMPLE 1: LINEAR CHAIN (Research → Write → Edit)")
print("=" * 80)

article = research_write_edit("FastAPI for building APIs")

print("=" * 80)
print("FINAL ARTICLE:")
print("=" * 80)
print(article)
print("=" * 80)

# Example 2: Conditional chain
print("\n" + "=" * 80)
print("EXAMPLE 2: CONDITIONAL CHAIN (Classify → Branch)")
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

1. Prompt chaining is just sequential API calls
   - Linear: Step 1 output → Step 2 input → Step 3 input
   - Conditional: Classify → Branch to different handlers
   - That's it. No magic.

2. Common patterns:
   - Research → Write → Edit (linear)
   - Classify → Route → Respond (conditional)
   - Generate → Critique → Improve → Repeat (iterative)
   - Multiple calls → Combine results (parallel)

3. You can combine concepts:
   - Chaining + Streaming (Step 3 in Example 1)
   - Chaining + RAG (retrieve docs in each step)
   - Chaining + Tool calling (call functions between steps)
   - All patterns can combine

4. When frameworks help:
   - Error handling and retries
   - Parallel execution
   - State management across long workflows
   - Logging and observability

   But you don't NEED them to build this.

CONGRATULATIONS! You've completed all 7 foundational concepts:
1. Basic API calls
2. Conversation memory
3. Tool calling
4. RAG
5. Conversational RAG
6. Streaming
7. Prompt chaining

You now understand how AI applications actually work. Go build something!
"""
