"""
RAG (RETRIEVAL AUGMENTED GENERATION) - ANTHROPIC CLAUDE

The industry says: "You need vector databases! Embedding models! Complex frameworks!"
The reality: RAG is just search + put in prompt + ask AI.

This example uses simple keyword search. No vector database needed.
"""

import os
from anthropic import Anthropic
from dotenv import load_dotenv
from sample_documents import DOCUMENTS

load_dotenv()
client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# =============================================================================
# STEP 1: RETRIEVAL - Simple keyword search
# =============================================================================


def simple_keyword_search(query: str, documents: list, max_results: int = 3) -> list:
    """
    Simple keyword-based document search.

    This is the "retrieval" part of RAG.

    How it works:
    1. Split query into words
    2. Count how many query words appear in each document
    3. Return documents sorted by relevance (most matches first)

    For many use cases, this works great! You don't always need embeddings.
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
            results.append(
                {
                    "doc": doc,
                    "score": matches,  # Simple relevance score
                }
            )

    # Sort by relevance (most matches first)
    results.sort(key=lambda x: x["score"], reverse=True)

    # Return top N results
    return [r["doc"] for r in results[:max_results]]


# =============================================================================
# STEP 2-3: AUGMENT + GENERATE - Build context and ask Claude
# =============================================================================


def rag_query(question: str, documents: list, max_context_docs: int = 3) -> str:
    """
    RAG in 3 steps:

    1. RETRIEVE: Find relevant documents (using keyword search)
    2. AUGMENT: Put them in the prompt as context
    3. GENERATE: Ask Claude to answer based on the documents

    That's literally all RAG is!
    """

    print(f"\n{'='*80}")
    print("RAG PROCESS")
    print(f"{'='*80}\n")

    # STEP 1: RETRIEVE relevant documents
    print(f"📚 STEP 1: RETRIEVE")
    print(f"Searching for documents related to: '{question}'\n")

    relevant_docs = simple_keyword_search(question, documents, max_context_docs)

    print(f"Found {len(relevant_docs)} relevant documents:")
    for i, doc in enumerate(relevant_docs, 1):
        print(f"  {i}. {doc['title']} (ID: {doc['id']})")

    if not relevant_docs:
        print("⚠️  No relevant documents found!")
        return "I couldn't find any relevant information to answer your question."

    # STEP 2: AUGMENT - Build context from retrieved documents
    print(f"\n📝 STEP 2: AUGMENT")
    print("Building context from retrieved documents...\n")

    # Combine the documents into a single context string
    context = ""
    for i, doc in enumerate(relevant_docs, 1):
        context += f"Document {i} - {doc['title']}:\n"
        context += doc["content"].strip()
        context += "\n\n"

    print(f"Context length: {len(context)} characters")

    # STEP 3: GENERATE - Ask Claude
    print(f"\n🤖 STEP 3: GENERATE")
    print("Sending to Claude with context...\n")

    # Build the prompt with context
    # This is the key: We give Claude the documents as context
    prompt = f"""Based on the following documents, please answer the question.

Documents:
{context}

Question: {question}

Instructions:
- Answer based ONLY on the information in the documents above
- If the documents don't contain enough information, say so
- Be specific and cite which document you're referencing
- Keep your answer concise and clear"""

    # Call Claude (just a normal API call!)
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}],
    )

    answer = response.content[0].text

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
print("CLAUDE'S ANSWER:")
print(f"{'='*80}")
print(answer)
print(f"{'='*80}\n")

# Try another question
print("\n" + "=" * 80)
question2 = "What are the main types of machine learning?"
print(f"Question: {question2}")

answer2 = rag_query(question2, DOCUMENTS, max_context_docs=3)

print(f"{'='*80}")
print("CLAUDE'S ANSWER:")
print(f"{'='*80}")
print(answer2)
print(f"{'='*80}\n")

"""
WHAT YOU JUST LEARNED:

1. RAG is NOT complex
   - Step 1: Search documents (keyword matching works fine)
   - Step 2: Add documents to prompt
   - Step 3: Ask AI to answer based on those documents
   - That's it. No magic.

2. You don't always need vector databases
   - Keyword search works for 50,000+ documents with basic optimization
   - Embeddings/vector search become valuable at larger scales
   - Start simple, add complexity only when needed

3. The key is in the prompt
   - Give Claude the context (the documents)
   - Explicitly instruct: "answer based ONLY on these documents"
   - This prevents hallucination - Claude can only use provided info

4. This is how production RAG systems work
   - ChatGPT with document uploads? This pattern.
   - Customer support bots? This pattern.
   - Internal knowledge bases? This pattern.
   - They might use fancier retrieval, but the core is the same.

NEXT STEP: Add conversation memory for follow-up questions (Conversational RAG)
"""
