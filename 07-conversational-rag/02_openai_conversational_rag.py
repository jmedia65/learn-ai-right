"""
CONVERSATIONAL RAG - OPENAI GPT (Responses API)

Same pattern as Anthropic: Fresh retrieval + conversation memory.
OpenAI difference: use instructions + input with Responses API.
"""

import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
MODEL = os.getenv("OPENAI_MODEL", "gpt-6-luna")
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# =============================================================================
# SAMPLE DOCUMENTS (same as module 06)
# =============================================================================

DOCUMENTS = [
    {
        "id": "doc1",
        "title": "Python Basics",
        "content": """Python is a high-level programming language known for its
        simplicity and readability. It was created by Guido van Rossum
        and first released in 1991. Python supports multiple programming
        paradigms including procedural, object-oriented, and functional
        programming. Common use cases include web development, data
        science, automation, and artificial intelligence.""",
    },
    {
        "id": "doc2",
        "title": "FastAPI Framework",
        "content": """FastAPI is a modern, fast web framework for building APIs with
        Python. It was created by Sebastián Ramírez and first released
        in 2018. FastAPI is built on top of Starlette and Pydantic,
        providing automatic API documentation, data validation, and
        high performance. It's one of the fastest Python frameworks
        available, comparable to NodeJS and Go.""",
    },
    {
        "id": "doc3",
        "title": "Machine Learning Basics",
        "content": """Machine learning is a subset of artificial intelligence that
        enables systems to learn and improve from experience without
        being explicitly programmed. There are three main types:
        supervised learning, unsupervised learning, and reinforcement
        learning. Popular frameworks include TensorFlow, PyTorch, and
        scikit-learn.""",
    },
]

# =============================================================================
# RETRIEVAL - Simple keyword search (identical to Anthropic version)
# =============================================================================


def simple_keyword_search(query: str, documents: list, max_results: int = 3) -> list:
    """Search documents by keyword matching."""
    query_lower = query.lower()
    query_words = set(query_lower.split())

    results = []
    for doc in documents:
        searchable_text = (doc["title"] + " " + doc["content"]).lower()
        matches = sum(1 for word in query_words if word in searchable_text)
        if matches > 0:
            results.append({"doc": doc, "score": matches})

    results.sort(key=lambda x: x["score"], reverse=True)
    return [r["doc"] for r in results[:max_results]]


# =============================================================================
# CONVERSATIONAL RAG FUNCTION (OpenAI Responses API)
# =============================================================================


def conversational_rag(question: str, documents: list, conversation_history: list):
    """
    Conversational RAG: Fresh retrieval + conversation memory.

    On each turn:
    1. Retrieve docs for THIS question
    2. Build instructions from retrieved docs
    3. Send full conversation history + new question
    4. Append the user message and all response output items to history
    """

    print(f"\n{'='*80}")
    print(f"USER: {question}")
    print(f"{'='*80}\n")

    # STEP 1: Retrieve documents for THIS question
    print("📚 Retrieving relevant documents...")
    relevant_docs = simple_keyword_search(question, documents, max_results=3)

    if not relevant_docs:
        print("⚠️  No relevant documents found!")
        answer = "I couldn't find relevant information to answer that question."
        conversation_history.append({"role": "user", "content": question})
        conversation_history.append({"role": "assistant", "content": answer})
        return answer, conversation_history

    print(f"Found {len(relevant_docs)} documents:")
    for doc in relevant_docs:
        print(f"  - {doc['title']}")

    # STEP 2: Build context from retrieved documents
    print("\n📝 Building context...")
    context = ""
    for doc in relevant_docs:
        context += f"{doc['title']}:\n{doc['content'].strip()}\n\n"

    instructions = f"""You are a helpful assistant that answers questions based on provided documents.

Available documents:
{context}

Instructions:
- Answer based on the documents provided
- Use conversation history for context (e.g., understanding pronouns like 'it')
- If asked a follow-up question, remember previous exchanges
- Cite which document you're using when possible"""

    # STEP 3: Build input with full history + new question
    # History remains explicit so students can see memory mechanics.
    input_messages = conversation_history + [{"role": "user", "content": question}]

    print("🤖 Asking GPT...\n")
    response = client.responses.create(
        model=MODEL,
        max_output_tokens=4096,
        instructions=instructions,
        input=input_messages,
        store=False,
    )
    if response.status != "completed":
        raise RuntimeError(f"Response did not complete: {response.status}")

    answer = response.output_text

    # STEP 4: Keep all output items, including reasoning items, in memory
    conversation_history.append({"role": "user", "content": question})
    conversation_history.extend(response.output)

    return answer, conversation_history


# =============================================================================
# USAGE EXAMPLE - Multi-turn conversation
# =============================================================================

conversation_history = []

print("=" * 80)
print("TURN 1")
print("=" * 80)

question1 = "What is FastAPI?"
answer1, conversation_history = conversational_rag(
    question1, DOCUMENTS, conversation_history
)

print(f"{'='*80}")
print(f"GPT: {answer1}")
print(f"{'='*80}\n")

print("=" * 80)
print("TURN 2")
print("=" * 80)

question2 = "Who created it?"
answer2, conversation_history = conversational_rag(
    question2, DOCUMENTS, conversation_history
)

print(f"{'='*80}")
print(f"GPT: {answer2}")
print(f"{'='*80}\n")

print("=" * 80)
print("TURN 3")
print("=" * 80)

question3 = "What is it built on top of?"
answer3, conversation_history = conversational_rag(
    question3, DOCUMENTS, conversation_history
)

print(f"{'='*80}")
print(f"GPT: {answer3}")
print(f"{'='*80}\n")

"""
WHAT YOU JUST LEARNED:

1. Responses API + instructions cleanly maps to conversational RAG
   - instructions: current retrieved document context
   - input: conversation history + new question

2. Pattern is still identical to Anthropic
   - Fresh retrieval each turn
   - Cumulative conversation memory
   - AI uses both docs + history

3. Memory remains explicit
   - You can inspect and debug conversation_history directly
   - That keeps the fundamentals transparent

NEXT STEP: Learn streaming to make responses feel more alive
"""
