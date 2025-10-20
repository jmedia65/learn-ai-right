###################################
# ANTHROPIC API WORKFLOW (PROMPT-CHAINING)
###################################
# The last step demonstrates how to stream the output token-by-token.

import os
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()
client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))


def research_write_edit(topic: str) -> str:
    """
    A 3-step content creation workflow.

    This is what people call an "AI agent."
    It's just 3 API calls with logic between them.
    """

    print(f"📚 Step 1: Researching '{topic}'...")

    # STEP 1: Research the topic
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
    print(f"✓ Research complete: {len(research)} characters\n")

    # STEP 2: Write article based on research
    print("✍️  Step 2: Writing article...")

    draft_response = client.messages.create(
        model="claude-sonnet-4-20250514",
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
    print(f"✓ Draft complete: {len(draft)} characters\n")

    # STEP 3: Edit for clarity
    # STREAMING: This final step now streams the response token-by-token
    print("✨ Step 3: Editing...")

    final = ""
    with client.messages.stream(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": f"""Edit this article for clarity and flow:

{draft}

Improve readability while keeping the same length.""",
            }
        ],
    ) as stream:
        for text in stream.text_stream:
            print(text, end="", flush=True)
            final += text

    print("\n✓ Editing complete\n")

    return final


# Use it
topic = "FastAPI for building APIs"
article = research_write_edit(topic)

print("=" * 80)
print("FINAL ARTICLE:")
print("=" * 80)
print(article)


###################################
# OPENAI API WORKFLOW (PROMPT-CHAINING WITH STREAMING)
###################################
# The last step demonstrates how to stream the output token-by-token.

import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def research_write_edit(topic: str) -> str:
    """
    A 3-step content creation workflow.

    This is what people call an "AI agent."
    It's just 3 API calls with logic between them.
    """

    print(f"📚 Step 1: Researching '{topic}'...")

    # STEP 1: Research the topic
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
    print(f"✓ Research complete: {len(research)} characters\n")

    # STEP 2: Write article based on research
    print("✍️  Step 2: Writing article...")

    draft_response = client.chat.completions.create(
        model="gpt-4o",
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

    draft = draft_response.choices[0].message.content
    print(f"✓ Draft complete: {len(draft)} characters\n")

    # STEP 3: Edit for clarity
    # STREAMING: This final step now streams the response token-by-token
    print("✨ Step 3: Editing...")

    final = ""
    stream = client.chat.completions.create(
        model="gpt-4o",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": f"""Edit this article for clarity and flow:

{draft}

Improve readability while keeping the same length.""",
            }
        ],
        stream=True,
    )

    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            text = chunk.choices[0].delta.content
            print(text, end="", flush=True)
            final += text

    print("\n✓ Editing complete\n")

    return final


# Use it
topic = "FastAPI for building APIs"
article = research_write_edit(topic)

print("=" * 80)
print("FINAL ARTICLE:")
print("=" * 80)
print(article)


###################################
# OPENAI API WORKFLOW (PROMPT-CHAINING WITH SIMPLE RAG)
###################################
# Adds a retrieval step to the research phase — "RAG-lite"
# NOT INCLUDED IN ARTICLE

import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# -----------------------------
# (1) Simple local "knowledge base"
# -----------------------------
DOCUMENTS = [
    {
        "title": "FastAPI Overview",
        "content": """FastAPI is a modern, fast Python web framework 
        for building APIs. Created by Sebastián Ramírez in 2018, 
        it uses type hints for validation and automatically 
        generates OpenAPI docs.""",
    },
    {
        "title": "FastAPI Performance",
        "content": """Built on Starlette and Pydantic, FastAPI supports 
        asynchronous I/O and can handle tens of thousands of requests 
        per second. It is one of the fastest Python frameworks.""",
    },
    {
        "title": "FastAPI Use Cases",
        "content": """Commonly used for RESTful APIs, microservices, 
        and ML model serving. It’s easy to learn for Python developers 
        and integrates well with async and data science stacks.""",
    },
]


# -----------------------------
# (2) Very simple keyword retriever
# -----------------------------
def simple_search(query, documents, top_k=2):
    query = query.lower()
    scored = []
    for doc in documents:
        score = sum(word in doc["content"].lower() for word in query.split())
        if score > 0:
            scored.append((score, doc))
    scored.sort(reverse=True, key=lambda x: x[0])
    return [doc["content"] for _, doc in scored[:top_k]]


# -----------------------------
# (3) Main workflow
# -----------------------------
def research_write_edit(topic: str) -> str:
    print(f"📚 Step 1: Researching '{topic}' with RAG...")

    # --- RAG PHASE: Retrieve relevant text ---
    retrieved_chunks = simple_search(topic, DOCUMENTS)
    context = "\n\n".join(retrieved_chunks)

    # --- Ask GPT to summarize based on retrieved text ---
    research_prompt = f"""Using the following retrieved context, summarize
the topic and provide:
- 5 key facts
- Main benefits
- Common use cases
- Important considerations

Context:
{context}

Topic: {topic}
Be concise and factual, and only use the info in the context."""

    research_response = client.chat.completions.create(
        model="gpt-4o",
        max_tokens=1024,
        messages=[{"role": "user", "content": research_prompt}],
    )

    research = research_response.choices[0].message.content
    print(f"✓ Research complete: {len(research)} characters\n")

    # --- Step 2: Write article ---
    print("✍️  Step 2: Writing article...")

    draft_response = client.chat.completions.create(
        model="gpt-4o",
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
    draft = draft_response.choices[0].message.content
    print(f"✓ Draft complete: {len(draft)} characters\n")

    # --- Step 3: Edit with streaming ---
    print("✨ Step 3: Editing...")
    final = ""
    stream = client.chat.completions.create(
        model="gpt-4o",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": f"""Edit this article for clarity and flow:

{draft}

Improve readability while keeping the same length.""",
            }
        ],
        stream=True,
    )

    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            text = chunk.choices[0].delta.content
            print(text, end="", flush=True)
            final += text

    print("\n✓ Editing complete\n")
    return final


# -----------------------------
# (4) Run it
# -----------------------------
topic = "FastAPI for building APIs"
article = research_write_edit(topic)

print("=" * 80)
print("FINAL ARTICLE:")
print("=" * 80)
print(article)


###################################
# ANTHROPIC API WORKFLOW (Classify -> Branch -> Respond)
###################################

import os
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()
client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))


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
