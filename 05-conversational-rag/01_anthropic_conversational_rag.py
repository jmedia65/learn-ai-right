"""
CONVERSATIONAL RAG - ANTHROPIC CLAUDE

Combining RAG + conversation memory for follow-up questions.

The pattern:
- Fresh document retrieval on each turn (for new question)
- Maintain conversation history (for context)
- AI uses BOTH to understand and answer
"""

import os
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()
client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

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
# RETRIEVAL - Simple keyword search (same as module 04)
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
# CONVERSATIONAL RAG FUNCTION
# =============================================================================


def conversational_rag(question: str, documents: list, conversation_history: list):
    """
    Conversational RAG: Fresh retrieval + conversation memory.

    On each turn:
    1. Retrieve documents for THIS question (fresh)
    2. Build system prompt with current documents
    3. Add user question to conversation history
    4. Send history + system prompt to Claude
    5. Add response to history

    This lets Claude use both the documents AND conversation context.
    """

    print(f"\n{'='*80}")
    print(f"USER: {question}")
    print(f"{'='*80}\n")

    # STEP 1: Retrieve documents for THIS question
    # This happens fresh on every turn
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

    # STEP 3: Create system prompt with CURRENT documents
    # This changes on every turn based on what was retrieved
    system_prompt = f"""You are a helpful assistant that answers questions based on provided documents.

Available documents:
{context}

Instructions:
- Answer based on the documents provided
- Use conversation history for context (e.g., understanding pronouns like "it")
- If asked a follow-up question, remember previous exchanges
- Cite which document you're using when possible"""

    # STEP 4: Add user question to conversation history
    conversation_history.append({"role": "user", "content": question})

    # STEP 5: Call Claude with system prompt + full conversation history
    # Claude sees:
    # - The documents (via system prompt)
    # - The entire conversation (via messages)
    print("🤖 Asking Claude...\n")

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        system=system_prompt,  # Documents go here (refreshed each turn)
        messages=conversation_history,  # Conversation history goes here
    )

    answer = response.content[0].text

    # STEP 6: Add Claude's response to history
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
print(f"CLAUDE: {answer1}")
print(f"{'='*80}\n")

# TURN 2: Follow-up question using pronoun "it"
# Claude needs conversation history to know "it" = FastAPI
# But we also retrieve fresh documents for this specific question
print("="*80)
print("TURN 2")
print("="*80)

question2 = "Who created it?"
answer2, conversation_history = conversational_rag(
    question2, DOCUMENTS, conversation_history
)

print(f"{'='*80}")
print(f"CLAUDE: {answer2}")
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
print(f"CLAUDE: {answer3}")
print(f"{'='*80}\n")

"""
WHAT YOU JUST LEARNED:

1. Conversational RAG = RAG + Memory
   - Each turn: retrieve fresh documents for the NEW question
   - Each turn: send the FULL conversation history
   - AI uses BOTH to understand context and answer

2. How follow-up questions work:
   Turn 1: "What is FastAPI?" → Retrieves FastAPI doc
   Turn 2: "Who created it?" → Retrieves docs for "created it"
                              → But conversation history tells Claude "it" = FastAPI
   Turn 3: "What is it built on?" → Same pattern

3. The key is separating concerns:
   - Document retrieval: Fresh on every turn (based on new question)
   - Conversation memory: Cumulative (keeps growing)
   - AI sees both: Documents + full conversation history

4. System prompt vs messages:
   - System prompt: Contains the documents (changes each turn)
   - Messages: Contains the conversation (grows each turn)
   - Anthropic lets you pass both separately

NEXT STEP: Learn streaming to make responses feel more alive
"""
