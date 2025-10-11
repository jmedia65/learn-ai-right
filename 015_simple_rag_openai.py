"""
RAG (RETRIEVAL AUGMENTED GENERATION) - OPENAI VERSION

Same concepts as Anthropic version, just different API syntax.
Compare both files to see the similarities!

RAG is just: Find relevant text → Put it in the prompt → Ask GPT

That's it. Let's prove it with OpenAI.
"""

import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ============================================================================
# YOUR DOCUMENTS (IDENTICAL to Anthropic version)
# ============================================================================

DOCUMENTS = [
    {
        "id": "doc1",
        "title": "Python Basics",
        "content": """
        Python is a high-level programming language known for its simplicity and readability.
        It was created by Guido van Rossum and first released in 1991. Python supports multiple
        programming paradigms including procedural, object-oriented, and functional programming.
        Common use cases include web development, data science, automation, and artificial intelligence.
        """,
    },
    {
        "id": "doc2",
        "title": "FastAPI Framework",
        "content": """
        FastAPI is a modern, fast web framework for building APIs with Python. It was created by
        Sebastián Ramírez and first released in 2018. FastAPI is built on top of Starlette and
        Pydantic, providing automatic API documentation, data validation, and high performance.
        It's one of the fastest Python frameworks available, comparable to NodeJS and Go.
        """,
    },
    {
        "id": "doc3",
        "title": "Machine Learning Basics",
        "content": """
        Machine learning is a subset of artificial intelligence that enables systems to learn
        and improve from experience without being explicitly programmed. There are three main
        types: supervised learning, unsupervised learning, and reinforcement learning. Popular
        frameworks include TensorFlow, PyTorch, and scikit-learn. Applications include image
        recognition, natural language processing, and predictive analytics.
        """,
    },
    {
        "id": "doc4",
        "title": "API Design Best Practices",
        "content": """
        Good API design is crucial for maintainability and usability. Key principles include:
        using RESTful conventions, providing clear error messages, versioning your API,
        implementing proper authentication, and documenting endpoints thoroughly. APIs should
        be consistent, intuitive, and follow standard HTTP methods (GET, POST, PUT, DELETE).
        Rate limiting and caching are important for performance.
        """,
    },
    {
        "id": "doc5",
        "title": "Database Fundamentals",
        "content": """
        Databases are organized collections of data that can be easily accessed and managed.
        SQL databases (like PostgreSQL and MySQL) use structured tables and relationships,
        while NoSQL databases (like MongoDB) offer more flexibility with document-based storage.
        Key concepts include indexing for performance, normalization for data integrity,
        and ACID properties (Atomicity, Consistency, Isolation, Durability) for transactions.
        """,
    },
]

# ============================================================================
# SIMPLE SEARCH (IDENTICAL to Anthropic version - provider-agnostic!)
# ============================================================================


def simple_keyword_search(query: str, documents: list, max_results: int = 3) -> list:
    """
    Simple keyword-based search.

    This function is IDENTICAL in both Anthropic and OpenAI versions.
    The search logic doesn't care which LLM you use!
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
                    "score": matches,
                }
            )

    # Sort by relevance
    results.sort(key=lambda x: x["score"], reverse=True)

    # Return top results
    return [r["doc"] for r in results[:max_results]]


# ============================================================================
# RAG QUERY FUNCTION (OpenAI version)
# ============================================================================


def rag_query(question: str, documents: list, max_context_docs: int = 3) -> str:
    """
    RAG in 3 steps - OpenAI version:

    1. RETRIEVE: Find relevant documents (same as Anthropic)
    2. AUGMENT: Put them in the prompt (same as Anthropic)
    3. GENERATE: Ask GPT to answer (different API call)
    """

    print(f"\n{'='*80}")
    print("RAG PROCESS - OPENAI VERSION")
    print(f"{'='*80}\n")

    # STEP 1: RETRIEVE (IDENTICAL to Anthropic version)
    print(f"📚 STEP 1: RETRIEVE")
    print(f"Searching for documents related to: '{question}'\n")

    relevant_docs = simple_keyword_search(question, documents, max_context_docs)

    print(f"Found {len(relevant_docs)} relevant documents:")
    for i, doc in enumerate(relevant_docs, 1):
        print(f"  {i}. {doc['title']} (ID: {doc['id']})")

    if not relevant_docs:
        print("⚠️  No relevant documents found!")
        return "I couldn't find any relevant information to answer your question."

    # STEP 2: AUGMENT (IDENTICAL to Anthropic version)
    print(f"\n📝 STEP 2: AUGMENT")
    print("Building context from retrieved documents...\n")

    context = ""
    for i, doc in enumerate(relevant_docs, 1):
        context += f"Document {i} - {doc['title']}:\n"
        context += doc["content"].strip()
        context += "\n\n"

    print(f"Context length: {len(context)} characters")

    # STEP 3: GENERATE (DIFFERENT - OpenAI API)
    print(f"\n🤖 STEP 3: GENERATE")
    print("Sending to GPT with context...\n")

    # Build the prompt
    prompt = f"""Based on the following documents, please answer the question.

Documents:
{context}

Question: {question}

Instructions:
- Answer based ONLY on the information in the documents above
- If the documents don't contain enough information, say so
- Be specific and cite which document you're referencing
- Keep your answer concise and clear"""

    # Call OpenAI (different than Anthropic)
    response = client.chat.completions.create(
        model="gpt-4o", max_tokens=1024, messages=[{"role": "user", "content": prompt}]
    )

    answer = response.choices[0].message.content

    print(f"✅ Answer generated!\n")

    return answer


# ============================================================================
# RAG WITH CITATIONS (OpenAI version)
# ============================================================================


def rag_query_with_citations(
    question: str, documents: list, max_context_docs: int = 3
) -> dict:
    """
    Enhanced RAG with citations - OpenAI version.

    Same logic as Anthropic, different API syntax.
    """

    # Retrieve (same as Anthropic)
    relevant_docs = simple_keyword_search(question, documents, max_context_docs)

    if not relevant_docs:
        return {
            "answer": "I couldn't find any relevant information to answer your question.",
            "sources": [],
        }

    # Build context (same as Anthropic)
    context = ""
    for i, doc in enumerate(relevant_docs, 1):
        context += f"[Document {i} - {doc['title']} (ID: {doc['id']})]:\n"
        context += doc["content"].strip()
        context += "\n\n"

    # Build prompt (same as Anthropic)
    prompt = f"""Based on the following documents, please answer the question.

Documents:
{context}

Question: {question}

Instructions:
- Answer based ONLY on the information in the documents above
- When stating facts, mention which document number you're referencing (e.g., "According to Document 1...")
- If the documents don't contain enough information, say so clearly
- Be specific and accurate"""

    # Call OpenAI (different from Anthropic)
    response = client.chat.completions.create(
        model="gpt-4o",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}],
    )

    answer = response.choices[0].message.content

    # Return (same structure as Anthropic)
    return {
        "answer": answer,
        "sources": [
            {"id": doc["id"], "title": doc["title"], "content": doc["content"]}
            for doc in relevant_docs
        ],
    }


# ============================================================================
# CONVERSATIONAL RAG (OpenAI version)
# ============================================================================


def conversational_rag(
    question: str, documents: list, conversation_history: list
) -> tuple[str, list]:
    """
    RAG + Conversation History - OpenAI version.

    KEY DIFFERENCE from Anthropic:
    - OpenAI uses system message in messages array
    - Anthropic uses separate system parameter
    """

    # Retrieve (same as Anthropic)
    relevant_docs = simple_keyword_search(question, documents, max_results=3)

    if not relevant_docs:
        return (
            "I couldn't find relevant information to answer your question.",
            conversation_history,
        )

    # Build context (same as Anthropic)
    context = ""
    for doc in relevant_docs:
        context += f"{doc['title']}:\n{doc['content'].strip()}\n\n"

    # Build system message with context
    system_message = f"""You are a helpful assistant that answers questions based on provided documents.

Available documents:
{context}

Instructions:
- Answer based on the documents provided
- Use conversation history for context
- If asked a follow-up question, remember previous exchanges
- Cite which document you're using when possible"""

    # For OpenAI, system message goes in the messages array
    # If this is the first turn, add system message
    if not conversation_history or conversation_history[0]["role"] != "system":
        conversation_history.insert(0, {"role": "system", "content": system_message})
    else:
        # Update system message with new context
        conversation_history[0] = {"role": "system", "content": system_message}

    # Add user question
    conversation_history.append({"role": "user", "content": question})

    # Call OpenAI
    response = client.chat.completions.create(
        model="gpt-4o",
        max_tokens=1024,
        messages=conversation_history,
    )

    answer = response.choices[0].message.content

    # Add assistant response
    conversation_history.append({"role": "assistant", "content": answer})

    return answer, conversation_history


# ============================================================================
# EXAMPLES AND TESTS
# ============================================================================

if __name__ == "__main__":
    print("=" * 80)
    print("SIMPLE RAG DEMONSTRATION - OPENAI VERSION")
    print("=" * 80)

    # Example 1: Basic RAG
    print("\n" + "=" * 80)
    print("EXAMPLE 1: BASIC RAG QUERY")
    print("=" * 80)

    question1 = "What is FastAPI and who created it?"
    answer1 = rag_query(question1, DOCUMENTS)

    print(f"{'='*80}")
    print("QUESTION:")
    print(f"{'='*80}")
    print(question1)
    print(f"\n{'='*80}")
    print("ANSWER:")
    print(f"{'='*80}")
    print(answer1)

    # Example 2: RAG with citations
    print("\n\n" + "=" * 80)
    print("EXAMPLE 2: RAG WITH CITATIONS")
    print("=" * 80)

    question2 = "What are the main types of machine learning?"
    result2 = rag_query_with_citations(question2, DOCUMENTS)

    print(f"\nQuestion: {question2}\n")
    print(f"{'='*80}")
    print("ANSWER:")
    print(f"{'='*80}")
    print(result2["answer"])
    print(f"\n{'='*80}")
    print("SOURCES:")
    print(f"{'='*80}")
    for i, source in enumerate(result2["sources"], 1):
        print(f"{i}. {source['title']} (ID: {source['id']})")

    # Example 3: Query with no relevant documents
    print("\n\n" + "=" * 80)
    print("EXAMPLE 3: QUESTION WITH NO RELEVANT DOCS")
    print("=" * 80)

    question3 = "What is the capital of France?"
    result3 = rag_query_with_citations(question3, DOCUMENTS)

    print(f"\nQuestion: {question3}\n")
    print("Answer:", result3["answer"])

    # Example 4: Conversational RAG
    print("\n\n" + "=" * 80)
    print("EXAMPLE 4: CONVERSATIONAL RAG")
    print("=" * 80)

    print("\nStarting a conversation about Python and FastAPI...\n")

    conversation_history = []

    # Turn 1
    q1 = "What is Python used for?"
    print(f"User: {q1}")
    a1, conversation_history = conversational_rag(q1, DOCUMENTS, conversation_history)
    print(f"Assistant: {a1}\n")

    # Turn 2 - Follow-up question
    q2 = "What about web frameworks? Tell me about one."
    print(f"User: {q2}")
    a2, conversation_history = conversational_rag(q2, DOCUMENTS, conversation_history)
    print(f"Assistant: {a2}\n")

    # Turn 3 - Another follow-up
    q3 = "Who created it?"
    print(f"User: {q3}")
    a3, conversation_history = conversational_rag(q3, DOCUMENTS, conversation_history)
    print(f"Assistant: {a3}\n")

    # Summary
    print("=" * 80)
    print("KEY INSIGHTS")
    print("=" * 80)
    print(
        """
RAG IS SIMPLE (with OpenAI too!):
1. Search your documents (keyword search works!)
2. Put relevant docs in the prompt
3. Ask GPT to answer based on those docs

SAME CONCEPTS AS ANTHROPIC VERSION.

The retrieval and augmentation are IDENTICAL.
Only the LLM API call is different.

No vector databases required.
No complex frameworks needed.
No vendor lock-in.

Start simple. Add complexity only when needed.

YOU JUST RAN PRODUCTION-READY RAG WITH OPENAI!
"""
    )


"""
ANTHROPIC VS OPENAI - RAG COMPARISON:

1. WHAT'S IDENTICAL:

   ✅ Document structure (same)
   ✅ Search function (100% identical)
   ✅ Context building (same string concatenation)
   ✅ Prompt structure (same instructions)
   ✅ Return values (same format)
   ✅ Overall logic (exactly the same)

2. WHAT'S DIFFERENT:

   API Call Syntax:
   
   Anthropic:
   ----------
   response = client.messages.create(
       model="claude-sonnet-4-20250514",
       max_tokens=1024,
       messages=[{"role": "user", "content": prompt}]
   )
   answer = response.content[0].text
   
   OpenAI:
   -------
   response = client.chat.completions.create(
       model="gpt-4o",
       max_tokens=1024,
       messages=[{"role": "user", "content": prompt}]
   )
   answer = response.choices[0].message.content

3. CONVERSATIONAL RAG DIFFERENCE:

   Anthropic:
   ----------
   response = client.messages.create(
       system="System prompt with context",  # Separate parameter
       messages=conversation_history
   )
   
   OpenAI:
   -------
   conversation_history = [
       {"role": "system", "content": "System prompt with context"},  # In array
       ...other messages
   ]
   response = client.chat.completions.create(
       messages=conversation_history
   )

4. THE BIG INSIGHT:

   RAG logic is PROVIDER-AGNOSTIC!
   
   The same search function works with both.
   The same document structure works with both.
   The same prompting strategy works with both.
   
   Only the final API call differs.

5. BUILDING PROVIDER-AGNOSTIC RAG:

   You could easily abstract the differences:
   
   def call_llm(prompt, provider="anthropic"):
       if provider == "anthropic":
           response = anthropic_client.messages.create(
               model="claude-sonnet-4-20250514",
               messages=[{"role": "user", "content": prompt}]
           )
           return response.content[0].text
       
       elif provider == "openai":
           response = openai_client.chat.completions.create(
               model="gpt-4o",
               messages=[{"role": "user", "content": prompt}]
           )
           return response.choices[0].message.content
   
   def rag_query(question, documents, provider="anthropic"):
       relevant_docs = search(question, documents)  # Provider-agnostic
       context = build_context(relevant_docs)       # Provider-agnostic
       prompt = build_prompt(context, question)     # Provider-agnostic
       answer = call_llm(prompt, provider)          # Provider-specific
       return answer
   
   Now you can switch providers with one parameter!

6. PERFORMANCE COMPARISON:

   In practice, for RAG:
   - Claude: Better at following citation instructions
   - GPT-4o: Slightly faster responses
   - Both: Excellent at answering based on context
   - Both: Work great with simple keyword search
   
   Use whichever you prefer!

7. COST COMPARISON (approximate):

   For a typical RAG query with 3 documents (~1500 tokens context):
   
   Anthropic (Claude Sonnet 4):
   - Input: ~1500 tokens × $0.003/1K = $0.0045
   - Output: ~200 tokens × $0.015/1K = $0.003
   - Total: ~$0.0075 per query
   
   OpenAI (GPT-4o):
   - Input: ~1500 tokens × $0.0025/1K = $0.00375
   - Output: ~200 tokens × $0.01/1K = $0.002
   - Total: ~$0.00575 per query
   
   Both are very affordable for RAG!

8. WHEN TO USE WHICH:

   Use Claude when:
   - Need precise citation following
   - Longer context windows needed
   - Want slightly better reasoning
   
   Use GPT-4o when:
   - Need faster responses
   - Want lower cost
   - Prefer OpenAI ecosystem
   
   Honestly: Both work great for RAG!

9. THE UNIVERSAL RAG PATTERN:

   Regardless of provider:
   
   1. Load documents
   2. Implement search (keyword or semantic)
   3. Build context from top results
   4. Create prompt with context + question
   5. Call LLM
   6. Return answer + sources
   
   This pattern works with:
   - Anthropic Claude
   - OpenAI GPT
   - Google Gemini
   - Any other LLM
   
   The search logic doesn't change!

10. NO VENDOR LOCK-IN:

    Because RAG logic is provider-agnostic:
    - Easy to switch providers
    - Easy to A/B test providers
    - Easy to use both (different use cases)
    - No framework dependency
    
    Your documents and search logic stay the same.
    Just swap the API call.

KEY TAKEAWAY:

RAG is simple with ANY provider.
The concepts are universal.
Only the API syntax differs.

You now have both Anthropic AND OpenAI RAG implementations.
Compare them. See the similarities. Master both.

No frameworks needed. No vendor lock-in. Full control.
"""
