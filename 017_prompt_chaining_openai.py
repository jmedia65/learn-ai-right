# 014_prompt_chaining_openai.py
"""
PROMPT CHAINING: Multi-Step AI Workflows - OPENAI VERSION

Same concepts as Anthropic version, just different API syntax.
Compare both files to see the similarities!

"Multi-agent systems" = Sequential API calls with logic between them

No framework needed. Just API calls + your brain.

Let's build the same 5 patterns with OpenAI.
"""

import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

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

    Same pattern as Anthropic, different API calls.
    """

    print(f"\n📚 Step 1: Researching '{topic}'...\n")

    # STEP 1: Research
    research_response = client.chat.completions.create(
        model="gpt-4o",
        max_tokens=2000,
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
    print(f"Research complete: {len(research)} characters\n")

    # STEP 2: Write based on research
    print("✍️  Step 2: Writing article...\n")

    draft_response = client.chat.completions.create(
        model="gpt-4o",
        max_tokens=2000,
        messages=[
            {
                "role": "user",
                "content": f"""Based on this research, write a 200-word article:

{research}

Make it engaging and accessible.""",
            }
        ],
    )

    draft = draft_response.choices[0].message.content
    print(f"Draft complete: {len(draft)} characters\n")

    # STEP 3: Edit for clarity
    print("✨ Step 3: Editing...\n")

    final_response = client.chat.completions.create(
        model="gpt-4o",
        max_tokens=2000,
        messages=[
            {
                "role": "user",
                "content": f"""Edit this article for clarity and flow:

{draft}

Improve readability while keeping the same length.""",
            }
        ],
    )

    final = final_response.choices[0].message.content

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

    Same logic as Anthropic, OpenAI API calls.
    """

    print(f"\nAnalyzing: '{user_input}'\n")

    # STEP 1: Classify intent
    classification = client.chat.completions.create(
        model="gpt-4o",
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

    intent = classification.choices[0].message.content.strip().lower()
    print(f"Intent classified as: {intent}\n")

    # STEP 2: Branch based on intent
    if intent == "technical_question":
        system_message = (
            "You are a helpful technical expert. Provide detailed, accurate answers."
        )
    elif intent == "bug_report":
        system_message = "You are a support agent. Acknowledge the bug, ask for details, and provide a ticket number."
    elif intent == "feature_request":
        system_message = "You are a product manager. Thank them and ask clarifying questions about the feature."
    else:  # general_chat
        system_message = "You are a friendly assistant. Have a casual conversation."

    # STEP 3: Generate response with appropriate persona
    response = client.chat.completions.create(
        model="gpt-4o",
        max_tokens=1024,
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_input},
        ],
    )

    return response.choices[0].message.content


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

    Same workflow, OpenAI implementation.
    """

    # STEP 1: Summarize
    print("\n📊 Step 1: Summarizing data...\n")

    summary_response = client.chat.completions.create(
        model="gpt-4o",
        max_tokens=500,
        messages=[
            {
                "role": "user",
                "content": f"""Summarize this data in 2-3 sentences:

{data}""",
            }
        ],
    )

    summary = summary_response.choices[0].message.content

    # STEP 2: Find patterns
    print("🔍 Step 2: Finding patterns...\n")

    patterns_response = client.chat.completions.create(
        model="gpt-4o",
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

    patterns = patterns_response.choices[0].message.content

    # STEP 3: Generate insights
    print("💡 Step 3: Generating insights...\n")

    insights_response = client.chat.completions.create(
        model="gpt-4o",
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

    insights = insights_response.choices[0].message.content

    # STEP 4: Create recommendations
    print("🎯 Step 4: Creating recommendations...\n")

    recommendations_response = client.chat.completions.create(
        model="gpt-4o",
        max_tokens=500,
        messages=[
            {
                "role": "user",
                "content": f"""Based on these insights, provide 3 actionable recommendations:

{insights}""",
            }
        ],
    )

    recommendations = recommendations_response.choices[0].message.content

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

    Quality through iteration.
    """

    current_version = initial_content

    for i in range(iterations):
        print(f"\n🔄 Iteration {i + 1}/{iterations}")

        # Critique current version
        critique_response = client.chat.completions.create(
            model="gpt-4o",
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

        critique = critique_response.choices[0].message.content
        print(f"Critique: {critique[:100]}...")

        # Improve based on critique
        improve_response = client.chat.completions.create(
            model="gpt-4o",
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

        current_version = improve_response.choices[0].message.content

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

    Comprehensive coverage from multiple angles.
    """

    print(f"\nAnalyzing '{topic}' from multiple perspectives...\n")

    # Path 1: Technical perspective
    print("🔧 Getting technical perspective...")
    tech_response = client.chat.completions.create(
        model="gpt-4o",
        max_tokens=300,
        messages=[
            {
                "role": "user",
                "content": f"Analyze {topic} from a technical perspective. What are the technical considerations?",
            }
        ],
    )

    tech_view = tech_response.choices[0].message.content

    # Path 2: Business perspective
    print("💼 Getting business perspective...")
    business_response = client.chat.completions.create(
        model="gpt-4o",
        max_tokens=300,
        messages=[
            {
                "role": "user",
                "content": f"Analyze {topic} from a business perspective. What are the ROI and business considerations?",
            }
        ],
    )

    business_view = business_response.choices[0].message.content

    # Path 3: User perspective
    print("👤 Getting user perspective...")
    user_response = client.chat.completions.create(
        model="gpt-4o",
        max_tokens=300,
        messages=[
            {
                "role": "user",
                "content": f"Analyze {topic} from an end-user perspective. What do users care about?",
            }
        ],
    )

    user_view = user_response.choices[0].message.content

    # Combine all perspectives
    print("🔀 Combining perspectives...\n")
    synthesis_response = client.chat.completions.create(
        model="gpt-4o",
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

    return synthesis_response.choices[0].message.content


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

ANTHROPIC VS OPENAI - DIFFERENCES:

API Call Syntax:
--------------
Anthropic:
response = client.messages.create(...)
answer = response.content[0].text

OpenAI:
response = client.chat.completions.create(...)
answer = response.choices[0].message.content

System Message:
--------------
Anthropic:
client.messages.create(system="...", messages=[...])

OpenAI:
client.chat.completions.create(messages=[
    {"role": "system", "content": "..."},
    ...
])

BUT THE LOGIC IS IDENTICAL!

The chaining pattern is provider-agnostic.
Only the API syntax differs.

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

With both Anthropic AND OpenAI.

Same patterns. Different APIs. Same power.

No framework needed.
"""
)

"""
PRODUCTION TIPS:

1. ERROR HANDLING:
   try:
       response = client.chat.completions.create(...)
   except Exception as e:
       # Decide: retry, skip, or fail?
       pass

2. COST MANAGEMENT:
   Track token usage per step
   Use gpt-4o-mini for simple steps
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

COMPARING PROVIDERS:

Both work great for prompt chaining!

Use Claude when:
- Need deep reasoning
- Want better citation following
- Prefer separate system parameter

Use GPT-4o when:
- Need faster responses
- Want lower cost
- Prefer system in messages array

Or use both! The patterns are identical.

NEXT STEPS:

- Add error handling to these examples
- Build your own chains for your use case
- Experiment with different step orders
- Combine with tools from earlier lessons
- Add RAG to make chains document-aware

Prompt chaining is simple but powerful.
Master it and you can build any AI workflow.

No framework needed.
With either provider.

TUTORIAL SERIES COMPLETE!

You now have:
✅ Basic API calls (Anthropic + OpenAI)
✅ System prompts (Anthropic + OpenAI)
✅ Conversation history (Anthropic + OpenAI)
✅ Streaming (Anthropic + OpenAI)
✅ Parameters (Anthropic + OpenAI)
✅ Tool calling (Anthropic + OpenAI)
✅ Simple RAG (Anthropic + OpenAI)
✅ Prompt chaining (Anthropic + OpenAI)

Everything you need to build production AI apps.
No frameworks required.
You're in control.

Now go build something amazing! 🚀
"""
