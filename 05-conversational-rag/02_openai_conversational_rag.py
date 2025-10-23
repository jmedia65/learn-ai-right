"""
CONVERSATIONAL RAG - OPENAI GPT

Same pattern as Anthropic: Fresh retrieval + conversation memory.
The only difference is how system messages are handled.
"""

import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# =============================================================================
# SAMPLE DOCUMENTS (same as module 04)
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
# CONVERSATIONAL RAG FUNCTION (OpenAI version)
# =============================================================================


def conversational_rag(question: str, documents: list, conversation_history: list):
    """
    Conversational RAG: Fresh retrieval + conversation memory.

    OpenAI difference: System messages go IN the messages array,
    not as a separate parameter.
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

    # STEP 3: Build system message with CURRENT documents
    system_message_content = f"""You are a helpful assistant that answers questions based on provided documents.

Available documents:
{context}

Instructions:
- Answer based on the documents provided
- Use conversation history for context (e.g., understanding pronouns like "it")
- If asked a follow-up question, remember previous exchanges
- Cite which document you're using when possible"""

    # STEP 4: Build full messages array
    # OpenAI requires system message to be IN the messages array
    # We rebuild it each turn with fresh documents
    messages = [
        {"role": "system", "content": system_message_content}
    ] + conversation_history + [
        {"role": "user", "content": question}
    ]

    # STEP 5: Call GPT
    print("🤖 Asking GPT...\n")

    response = client.chat.completions.create(
        model="gpt-4o",
        max_tokens=1024,
        messages=messages,  # System message + conversation + new question
    )

    answer = response.choices[0].message.content

    # STEP 6: Add user question and response to conversation history
    # Note: We don't store the system message in history
    # We regenerate it each turn with fresh documents
    conversation_history.append({"role": "user", "content": question})
    conversation_history.append({"role": "assistant", "content": answer})

    return answer, conversation_history


# =============================================================================
# USAGE EXAMPLE - Multi-turn conversation
# =============================================================================

conversation_history = []

# TURN 1: Initial question
print("="*80)
print("TURN 1")
print("="*80)

question1 = "What is FastAPI?"
answer1, conversation_history = conversational_rag(
    question1, DOCUMENTS, conversation_history
)

print(f"{'='*80}")
print(f"GPT: {answer1}")
print(f"{'='*80}\n")

# TURN 2: Follow-up question using pronoun "it"
print("="*80)
print("TURN 2")
print("="*80)

question2 = "Who created it?"
answer2, conversation_history = conversational_rag(
    question2, DOCUMENTS, conversation_history
)

print(f"{'='*80}")
print(f"GPT: {answer2}")
print(f"{'='*80}\n")

# TURN 3: Another follow-up
print("="*80)
print("TURN 3")
print("="*80)

question3 = "What is it built on top of?"
answer3, conversation_history = conversational_rag(
    question3, DOCUMENTS, conversation_history
)

print(f"{'='*80}")
print(f"GPT: {answer3}")
print(f"{'='*80}\n")

"""
WHAT YOU JUST LEARNED:

1. OpenAI vs Anthropic system message difference:
   - Anthropic: system parameter separate from messages
   - OpenAI: system message goes IN the messages array
   - Both achieve the same result

2. The pattern is identical:
   - Fresh document retrieval each turn
   - Maintain conversation history
   - AI sees both documents + history

3. Implementation strategy:
   - conversation_history: Only stores user/assistant exchanges
   - System message: Built fresh each turn with new documents
   - Final messages array: system + history + new question

4. This handles complex follow-ups:
   "What is X?" → "Who created it?" → "When?" → "Why?"
   Each question triggers fresh retrieval, but AI remembers context

NEXT STEP: Learn streaming to make responses feel more alive
"""
