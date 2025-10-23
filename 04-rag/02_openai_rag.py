"""
RAG (RETRIEVAL AUGMENTED GENERATION) - OPENAI GPT

Same RAG pattern as Anthropic: search + put in prompt + ask AI.
The only difference is the API syntax.
"""

import os
from openai import OpenAI
from dotenv import load_dotenv
from sample_documents import DOCUMENTS

load_dotenv()
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
        # Combine title and content for searching
        searchable_text = (doc["title"] + " " + doc["content"]).lower()

        # Count how many query words appear in the document
        matches = sum(1 for word in query_words if word in searchable_text)

        if matches > 0:
            results.append({"doc": doc, "score": matches})

    # Sort by relevance
    results.sort(key=lambda x: x["score"], reverse=True)

    # Return top N results
    return [r["doc"] for r in results[:max_results]]


# =============================================================================
# STEP 2-3: AUGMENT + GENERATE - Build context and ask GPT
# =============================================================================


def rag_query(question: str, documents: list, max_context_docs: int = 3) -> str:
    """
    RAG in 3 steps (same pattern as Anthropic):

    1. RETRIEVE: Find relevant documents
    2. AUGMENT: Put them in the prompt
    3. GENERATE: Ask GPT to answer based on the documents
    """

    print(f"\n{'='*80}")
    print("RAG PROCESS")
    print(f"{'='*80}\n")

    # STEP 1: RETRIEVE
    print(f"📚 STEP 1: RETRIEVE")
    print(f"Searching for documents related to: '{question}'\n")

    relevant_docs = simple_keyword_search(question, documents, max_context_docs)

    print(f"Found {len(relevant_docs)} relevant documents:")
    for i, doc in enumerate(relevant_docs, 1):
        print(f"  {i}. {doc['title']} (ID: {doc['id']})")

    if not relevant_docs:
        print("⚠️  No relevant documents found!")
        return "I couldn't find any relevant information to answer your question."

    # STEP 2: AUGMENT
    print(f"\n📝 STEP 2: AUGMENT")
    print("Building context from retrieved documents...\n")

    context = ""
    for i, doc in enumerate(relevant_docs, 1):
        context += f"Document {i} - {doc['title']}:\n"
        context += doc["content"].strip()
        context += "\n\n"

    print(f"Context length: {len(context)} characters")

    # STEP 3: GENERATE
    print(f"\n🤖 STEP 3: GENERATE")
    print("Sending to GPT with context...\n")

    # Build the prompt with context
    prompt = f"""Based on the following documents, please answer the question.

Documents:
{context}

Question: {question}

Instructions:
- Answer based ONLY on the information in the documents above
- If the documents don't contain enough information, say so
- Be specific and cite which document you're referencing
- Keep your answer concise and clear"""

    # Call GPT (just a normal API call!)
    response = client.chat.completions.create(
        model="gpt-4o",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}],
    )

    answer = response.choices[0].message.content

    print(f"✅ Answer generated!\n")

    return answer


# =============================================================================
# USAGE EXAMPLE
# =============================================================================

# Ask a question about our documents
question = "What is FastAPI and who created it?"

print(f"Question: {question}")

# Run RAG
answer = rag_query(question, DOCUMENTS, max_context_docs=3)

# Display the answer
print(f"{'='*80}")
print("GPT'S ANSWER:")
print(f"{'='*80}")
print(answer)
print(f"{'='*80}\n")

# Try another question
print("\n" + "="*80)
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
   - Anthropic and OpenAI use the same three-step pattern
   - Only difference is API method names
   - The retrieval logic is completely identical

2. The retrieval step is provider-agnostic
   - simple_keyword_search() works with any AI provider
   - You could swap Claude for GPT or vice versa
   - The search logic doesn't care about the LLM

3. When to use embeddings vs keyword search:
   - Keyword search: < 50,000 documents, exact matches matter
   - Embeddings: > 50,000 documents, semantic meaning matters
   - Many production systems start with keywords, add embeddings later

4. You can build this yourself
   - No framework dependency
   - Full control over retrieval logic
   - Easy to debug and optimize
   - Clear understanding of what's happening

NEXT STEP: Add conversation memory for follow-up questions (Conversational RAG)
"""
