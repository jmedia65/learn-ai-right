"""
PROMPT CHAINING: Multi-Step AI Workflows

What the industry calls "multi-agent systems" or "agentic workflows"?
It's just this: Call AI → Process → Call AI → Process → Done

No framework needed. Just sequential API calls with logic between them.

This is how you build:
- Research assistants
- Content generators
- Data analyzers
- Complex problem solvers

Let's demystify it.
"""

import os
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()
client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# ============================================================================
# EXAMPLE 1: SIMPLE 3-STEP CHAIN
# ============================================================================

print("=" * 80)
print("EXAMPLE 1: RESEARCH → WRITE → EDIT CHAIN")
print("=" * 80)


def research_write_edit(topic: str) -> str:
    """
    A 3-step workflow:
    1. Research the topic
    2. Write article based on research
    3. Edit for clarity

    This is "prompt chaining" - nothing magical.
    """

    print(f"\n📚 Step 1: Researching '{topic}'...\n")

    # STEP 1: Research
    research_response = client.messages.create(
        model="claude-4-sonnet-20250514",
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
    print(f"Research complete: {len(research)} characters\n")

    # STEP 2: Write based on research
    print("✍️  Step 2: Writing article...\n")

    draft_response = client.messages.create(
        model="claude-4-sonnet-20250514",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": f"""Based on this research, write a 200-word article:

{research}

Make it engaging and accessible.""",
            }
        ],
    )

    draft = draft_response.content[0].text
    print(f"Draft complete: {len(draft)} characters\n")

    # STEP 3: Edit for clarity
    print("✨ Step 3: Editing...\n")

    final_response = client.messages.create(
        model="claude-4-sonnet-20250514",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": f"""Edit this article for clarity and flow:

{draft}

Improve readability while keeping the same length.""",
            }
        ],
    )

    final = final_response.content[0].text

    return final


# Run the chain
topic = "FastAPI for building APIs"
result = research_write_edit(topic)

print("=" * 80)
print("FINAL RESULT:")
print("=" * 80)
print(result)

# ============================================================================
# EXAMPLE 2: CONDITIONAL CHAIN (with branching logic)
# ============================================================================


print("\n\n" + "=" * 80)
print("EXAMPLE 2: CONDITIONAL CHAIN WITH BRANCHING")
print("=" * 80)


def analyze_and_respond(user_input: str) -> str:
    """
    Chain with conditional logic:
    1. Classify user intent
    2. Branch based on classification
    3. Generate appropriate response

    This is how smart chatbots work.
    """

    print(f"\nAnalyzing: '{user_input}'\n")

    # STEP 1: Classify intent
    classification = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=100,
        messages=[
            {
                "role": "user",
                "content": f"""Classify this user input into ONE category:
- technical_question
- bug_report
- feature_request
- general_chat

User input: {user_input}

Respond with ONLY the category name.""",
            }
        ],
    )

    intent = classification.content[0].text.strip().lower()
    print(f"Intent classified as: {intent}\n")

    # STEP 2: Branch based on intent
    if intent == "technical_question":
        system_prompt = (
            "You are a helpful technical expert. Provide detailed, accurate answers."
        )
    elif intent == "bug_report":
        system_prompt = "You are a support agent. Acknowledge the bug, ask for details, and provide a ticket number."
    elif intent == "feature_request":
        system_prompt = "You are a product manager. Thank them and ask clarifying questions about the feature."
    else:  # general_chat
        system_prompt = "You are a friendly assistant. Have a casual conversation."

    # STEP 3: Generate response with appropriate persona
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        system=system_prompt,
        messages=[{"role": "user", "content": user_input}],
    )

    return response.content[0].text


# Test different inputs
inputs = [
    "How do I implement authentication in FastAPI?",
    "The app crashes when I upload a file larger than 10MB",
    "Can you add dark mode to the dashboard?",
]

for user_input in inputs:
    print("=" * 80)
    result = analyze_and_respond(user_input)
    print(f"\nResponse:\n{result}\n")

# ============================================================================
# EXAMPLE 3: DATA PROCESSING CHAIN
# ============================================================================

print("\n" + "=" * 80)
print("EXAMPLE 3: DATA ANALYSIS CHAIN")
print("=" * 80)


def analyze_data_chain(data: str) -> dict:
    """
    Multi-step data analysis:
    1. Summarize data
    2. Find patterns
    3. Generate insights
    4. Create recommendations

    This is how AI data analysts work.
    """

    # STEP 1: Summarize
    print("\n📊 Step 1: Summarizing data...\n")

    summary_response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=500,
        messages=[
            {
                "role": "user",
                "content": f"""Summarize this data in 2-3 sentences:

{data}""",
            }
        ],
    )

    summary = summary_response.content[0].text

    # STEP 2: Find patterns
    print("🔍 Step 2: Finding patterns...\n")

    patterns_response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=500,
        messages=[
            {
                "role": "user",
                "content": f"""Based on this data, identify 3 key patterns or trends:

{data}

List them as bullet points.""",
            }
        ],
    )

    patterns = patterns_response.content[0].text

    # STEP 3: Generate insights
    print("💡 Step 3: Generating insights...\n")

    insights_response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=500,
        messages=[
            {
                "role": "user",
                "content": f"""Given this summary and patterns, what are 2 key insights?

Summary: {summary}

Patterns: {patterns}""",
            }
        ],
    )

    insights = insights_response.content[0].text

    # STEP 4: Create recommendations
    print("🎯 Step 4: Creating recommendations...\n")

    recommendations_response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=500,
        messages=[
            {
                "role": "user",
                "content": f"""Based on these insights, provide 3 actionable recommendations:

{insights}""",
            }
        ],
    )

    recommendations = recommendations_response.content[0].text

    return {
        "summary": summary,
        "patterns": patterns,
        "insights": insights,
        "recommendations": recommendations,
    }


# Test with sample data
sample_data = """
Sales data Q4 2024:
- October: $45,000 (120 customers)
- November: $52,000 (145 customers)
- December: $78,000 (210 customers)

Top products:
1. Product A: 45% of revenue
2. Product B: 30% of revenue
3. Product C: 25% of revenue

Customer acquisition cost: $150
Average order value: Increased from $375 to $371
"""

analysis = analyze_data_chain(sample_data)

print("=" * 80)
print("COMPLETE ANALYSIS:")
print("=" * 80)
print(f"\nSUMMARY:\n{analysis['summary']}")
print(f"\nPATTERNS:\n{analysis['patterns']}")
print(f"\nINSIGHTS:\n{analysis['insights']}")
print(f"\nRECOMMENDATIONS:\n{analysis['recommendations']}")

# ============================================================================
# EXAMPLE 4: ITERATIVE REFINEMENT CHAIN
# ============================================================================

print("\n\n" + "=" * 80)
print("EXAMPLE 4: ITERATIVE REFINEMENT")
print("=" * 80)


def iterative_improve(initial_content: str, iterations: int = 3) -> str:
    """
    Iteratively improve content:
    1. Generate initial version
    2. Critique it
    3. Improve based on critique
    4. Repeat

    This is how you get high-quality output.
    """

    current_version = initial_content

    for i in range(iterations):
        print(f"\n🔄 Iteration {i + 1}/{iterations}")

        # Critique current version
        critique_response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=500,
            messages=[
                {
                    "role": "user",
                    "content": f"""Critique this text and suggest 2-3 specific improvements:

{current_version}

Focus on clarity, engagement, and accuracy.""",
                }
            ],
        )

        critique = critique_response.content[0].text
        print(f"Critique: {critique[:100]}...")

        # Improve based on critique
        improve_response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1000,
            messages=[
                {
                    "role": "user",
                    "content": f"""Improve this text based on the critique:

Original text:
{current_version}

Critique:
{critique}

Provide the improved version.""",
                }
            ],
        )

        current_version = improve_response.content[0].text

    return current_version


# Test iterative improvement
initial_text = "Python is a programming language. It is used for many things. People like it because it is easy."

print("\nInitial version:")
print(initial_text)

improved = iterative_improve(initial_text, iterations=2)

print("\n" + "=" * 80)
print("FINAL IMPROVED VERSION:")
print("=" * 80)
print(improved)

# ============================================================================
# EXAMPLE 5: PARALLEL CHAIN (multiple paths, then combine)
# ============================================================================

print("\n\n" + "=" * 80)
print("EXAMPLE 5: PARALLEL PROCESSING")
print("=" * 80)


def parallel_analysis(topic: str) -> str:
    """
    Run multiple analyses in parallel (conceptually):
    1. Technical analysis
    2. Business analysis
    3. User perspective
    4. Combine all viewpoints

    This gives comprehensive coverage.
    """

    print(f"\nAnalyzing '{topic}' from multiple perspectives...\n")

    # Path 1: Technical perspective
    print("🔧 Getting technical perspective...")
    tech_response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=300,
        messages=[
            {
                "role": "user",
                "content": f"Analyze {topic} from a technical perspective. What are the technical considerations?",
            }
        ],
    )

    tech_view = tech_response.content[0].text

    # Path 2: Business perspective
    print("💼 Getting business perspective...")
    business_response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=300,
        messages=[
            {
                "role": "user",
                "content": f"Analyze {topic} from a business perspective. What are the ROI and business considerations?",
            }
        ],
    )

    business_view = business_response.content[0].text

    # Path 3: User perspective
    print("👤 Getting user perspective...")
    user_response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=300,
        messages=[
            {
                "role": "user",
                "content": f"Analyze {topic} from an end-user perspective. What do users care about?",
            }
        ],
    )

    user_view = user_response.content[0].text

    # Combine all perspectives
    print("🔀 Combining perspectives...\n")
    synthesis_response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1000,
        messages=[
            {
                "role": "user",
                "content": f"""Synthesize these three perspectives into a comprehensive analysis:

Technical: {tech_view}

Business: {business_view}

User: {user_view}

Provide a balanced view that considers all three perspectives.""",
            }
        ],
    )

    return synthesis_response.content[0].text


# Test parallel analysis
topic = "implementing AI chatbots in customer service"
comprehensive_analysis = parallel_analysis(topic)

print("=" * 80)
print("COMPREHENSIVE ANALYSIS:")
print("=" * 80)
print(comprehensive_analysis)

# ============================================================================
# KEY INSIGHTS
# ============================================================================

print("\n\n" + "=" * 80)
print("KEY INSIGHTS ABOUT PROMPT CHAINING")
print("=" * 80)

print(
    """
WHAT IS PROMPT CHAINING?

Sequential API calls where:
- Output of one call feeds into the next
- You add logic/processing between calls
- You can branch based on results
- You can iterate until satisfied

PATTERNS YOU JUST SAW:

1. LINEAR CHAIN (Example 1)
   Research → Write → Edit
   Simple, powerful, common

2. CONDITIONAL CHAIN (Example 2)
   Classify → Branch → Respond
   Different paths based on input

3. MULTI-STEP PROCESSING (Example 3)
   Summarize → Patterns → Insights → Recommendations
   Build complexity gradually

4. ITERATIVE REFINEMENT (Example 4)
   Generate → Critique → Improve → Repeat
   Quality through iteration

5. PARALLEL + SYNTHESIS (Example 5)
   Multiple analyses → Combine
   Comprehensive coverage

WHEN TO USE PROMPT CHAINING:

✅ Task is too complex for one prompt
✅ Need intermediate results
✅ Want to validate/filter between steps
✅ Different steps need different instructions
✅ Building multi-stage workflows

REAL-WORLD APPLICATIONS:

- Content creation pipelines
- Data analysis workflows
- Customer support routing
- Research assistants
- Code review processes
- Quality assurance
- Document processing

THE POWER:

You control the flow. You add logic. You decide when to branch.
This is "agentic AI" without the framework.

WHAT FRAMEWORKS ADD:

- Error handling & retries
- Parallel execution
- State management
- Logging & monitoring
- Pre-built chains

All useful. None required to start.

YOU JUST BUILT 5 DIFFERENT "AGENT" PATTERNS.

No framework. Just API calls + logic.

This is how production AI systems work.
"""
)

"""
PRODUCTION TIPS:

1. ERROR HANDLING:
   Wrap each step in try/except
   Decide: retry, skip, or fail?

2. COST MANAGEMENT:
   Track token usage per step
   Use cheaper models for simple steps
   Cache intermediate results

3. PERFORMANCE:
   Consider async for parallel paths
   Stream long-running steps
   Show progress to users

4. QUALITY CONTROL:
   Validate outputs between steps
   Set quality thresholds
   Log all intermediate results

5. TESTING:
   Test each step independently
   Test the full chain
   Test edge cases and errors

NEXT STEPS:

- Add error handling to these examples
- Build your own chains for your use case
- Experiment with different step orders
- Combine with tools from earlier lessons
- Add RAG to make chains document-aware

Prompt chaining is simple but powerful.
Master it and you can build any AI workflow.

No framework needed.
"""
