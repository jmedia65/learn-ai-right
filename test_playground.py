###################################
# OPENAI API WORKFLOW (PROMPT-CHAINING WITH SIMPLE RAG)
###################################
# Adds a retrieval step to the research phase — "RAG-lite"

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
