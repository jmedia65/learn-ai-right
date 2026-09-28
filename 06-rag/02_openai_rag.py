"""
RAG (RETRIEVAL AUGMENTED GENERATION) - OPENAI GPT (Responses API)

Same RAG pattern as Anthropic: search + put in prompt + ask AI.
The only difference is API syntax.
"""

import os
from openai import OpenAI
from dotenv import load_dotenv
from sample_documents import DOCUMENTS

load_dotenv()
MODEL = os.getenv("OPENAI_MODEL", "gpt-6-luna")
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# =============================================================================
# STEP 1: RETRIEVAL - Simple keyword search (identical to Anthropic version)
# =============================================================================


def simple_keyword_search(query: str, documents: list, max_results: int = 3) -> list:
    """
    Simple keyword-based document search.

    This is the "retrieval" part of RAG - same for both providers.
    """

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
# STEP 2-3: AUGMENT + GENERATE - Build context and ask GPT
# =============================================================================


def rag_query(question: str, documents: list, max_context_docs: int = 3) -> str:
    """
    RAG in 3 steps:

    1. RETRIEVE: Find relevant documents
    2. AUGMENT: Put them in the prompt
    3. GENERATE: Ask GPT to answer based on the documents
    """

    print(f"\n{'='*80}")
    print("RAG PROCESS")
    print(f"{'='*80}\n")

    # STEP 1: RETRIEVE
    print("📚 STEP 1: RETRIEVE")
    print(f"Searching for documents related to: '{question}'\n")

    relevant_docs = simple_keyword_search(question, documents, max_context_docs)

    print(f"Found {len(relevant_docs)} relevant documents:")
    for i, doc in enumerate(relevant_docs, 1):
        print(f"  {i}. {doc['title']} (ID: {doc['id']})")

    if not relevant_docs:
        print("⚠️  No relevant documents found!")
        return "I couldn't find any relevant information to answer your question."

    # STEP 2: AUGMENT
    print("\n📝 STEP 2: AUGMENT")
    print("Building context from retrieved documents...\n")

    context = ""
    for i, doc in enumerate(relevant_docs, 1):
        context += f"Document {i} - {doc['title']}:\n"
        context += doc["content"].strip()
        context += "\n\n"

    print(f"Context length: {len(context)} characters")

    # STEP 3: GENERATE
    print("\n🤖 STEP 3: GENERATE")
    print("Sending to GPT with context...\n")

    prompt = f"""Based on the following documents, please answer the question.

Documents:
{context}

Question: {question}

Instructions:
- Answer based ONLY on the information in the documents above
- If the documents don't contain enough information, say so
- Be specific and cite which document you're referencing
- Keep your answer concise and clear"""

    response = client.responses.create(
        model=MODEL,
        max_output_tokens=4096,
        input=prompt,
    )
    if response.status != "completed":
        raise RuntimeError(f"Response did not complete: {response.status}")

    answer = response.output_text

    print("✅ Answer generated!\n")

    return answer


# =============================================================================
# USAGE EXAMPLE
# =============================================================================

question = "What is FastAPI and who created it?"
print(f"Question: {question}")

answer = rag_query(question, DOCUMENTS, max_context_docs=3)

print(f"{'='*80}")
print("GPT'S ANSWER:")
print(f"{'='*80}")
print(answer)
print(f"{'='*80}\n")

print("\n" + "=" * 80)
question2 = "What are the main types of machine learning?"
print(f"Question: {question2}")

answer2 = rag_query(question2, DOCUMENTS, max_context_docs=3)

print(f"{'='*80}")
print("GPT'S ANSWER:")
print(f"{'='*80}")
print(answer2)
print(f"{'='*80}\n")

"""
WHAT YOU JUST LEARNED:

1. RAG is the same across providers
   - Same three-step pattern
   - Different SDK syntax only

2. Responses API handles generation cleanly
   - Pass full prompt in input
   - Read final text from response.output_text

3. Retrieval is provider-agnostic
   - You can swap providers without changing search logic

NEXT STEP: Add conversation memory for follow-up questions (Conversational RAG)
"""
