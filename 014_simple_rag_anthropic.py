"""
RAG (RETRIEVAL AUGMENTED GENERATION) - THE TRUTH

What the industry says:
- "You need vector databases!"
- "You need embedding models!"
- "You need LlamaIndex or LangChain!"
- "Complex chunking strategies required!"

The reality:
RAG is just: Find relevant text → Put it in the prompt → Ask Claude

That's it. Let's prove it.
"""

import os
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()
client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# ============================================================================
# YOUR DOCUMENTS (this is your "database")
# ============================================================================

# In production, you'd load these from files, databases, etc.
# For this demo, we'll use a simple list of documents

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
# SIMPLE SEARCH (no vector database needed!)
# ============================================================================


def simple_keyword_search(query: str, documents: list, max_results: int = 3) -> list:
    """
    Simple keyword-based search.

    This is the "retrieval" part of RAG.

    In production, you might use:
    - More sophisticated text matching
    - BM25 algorithm
    - Embeddings + vector search (for semantic search)

    But for many use cases, simple keyword matching works great!
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

    # Return top results
    return [r["doc"] for r in results[:max_results]]


# ============================================================================
# RAG QUERY FUNCTION (this is where the magic happens)
# ============================================================================


def rag_query(question: str, documents: list, max_context_docs: int = 3) -> str:
    """
    RAG in 3 steps:

    1. RETRIEVE: Find relevant documents
    2. AUGMENT: Put them in the prompt
    3. GENERATE: Ask Claude to answer based on the documents

    That's literally all RAG is!
    """

    print(f"\n{'='*80}")
    print("RAG PROCESS")
    print(f"{'='*80}\n")

    # STEP 1: RETRIEVE relevant documents
    print(f"📚 STEP 1: RETRIEVE")
    print(f"Searching for documents related to: '{question}'\n")

    # Call the retrieval function
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
    prompt = f"""Based on the following documents, please answer the question.

Documents:
{context}

Question: {question}

Instructions:
- Answer based ONLY on the information in the documents above
- If the documents don't contain enough information, say so
- Be specific and cite which document you're referencing
- Keep your answer concise and clear"""

    # Call Claude
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}],
    )

    answer = response.content[0].text

    print(f"✅ Answer generated!\n")

    return answer


# ============================================================================
# RAG WITH CITATIONS (production-ready version)
# ============================================================================


def rag_query_with_citations(
    question: str, documents: list, max_context_docs: int = 3
) -> dict:
    """
    Enhanced RAG that returns both answer and source documents.

    This is what you'd use in production - gives users transparency
    about where the information came from.
    """

    # Retrieve: call the retrieval function
    relevant_docs = simple_keyword_search(question, documents, max_context_docs)

    if not relevant_docs:
        return {
            "answer": "I couldn't find any relevant information to answer your question.",
            "sources": [],
        }

    # Build context with document IDs for citation
    context = ""
    for i, doc in enumerate(relevant_docs, 1):
        context += f"[Document {i} - {doc['title']} (ID: {doc['id']})]:\n"
        context += doc["content"].strip()
        context += "\n\n"

    # Ask Claude to cite sources
    prompt = f"""Based on the following documents, please answer the question.

Documents:
{context}

Question: {question}

Instructions:
- Answer based ONLY on the information in the documents above
- When stating facts, mention which document number you're referencing (e.g., "According to Document 1...")
- If the documents don't contain enough information, say so clearly
- Be specific and accurate"""

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}],
    )

    answer = response.content[0].text

    # Return answer with sources
    return {
        "answer": answer,
        "sources": [
            {"id": doc["id"], "title": doc["title"], "content": doc["content"]}
            for doc in relevant_docs
        ],
    }


# ============================================================================
# CONVERSATIONAL RAG (with memory)
# ============================================================================


def conversational_rag(
    question: str, documents: list, conversation_history: list
) -> tuple[str, list]:
    """
    RAG + Conversation History = Conversational RAG

    Now users can ask follow-up questions!

    This combines:
    - RAG (retrieve documents and answer)
    - Conversation memory (from earlier lessons)
    """

    # Retrieve relevant documents for this question
    relevant_docs = simple_keyword_search(question, documents, max_results=3)

    if not relevant_docs:
        return (
            "I couldn't find relevant information to answer your question.",
            conversation_history,
        )

    # Build context
    context = ""
    for doc in relevant_docs:
        context += f"{doc['title']}:\n{doc['content'].strip()}\n\n"

    # Build prompt with context AND conversation history
    system_prompt = f"""You are a helpful assistant that answers questions based on provided documents.

Available documents:
{context}

Instructions:
- Answer based on the documents provided
- Use conversation history for context
- If asked a follow-up question, remember previous exchanges
- Cite which document you're using when possible"""

    # Add new user question
    conversation_history.append({"role": "user", "content": question})

    # Call Claude with both system prompt and conversation history
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        system=system_prompt,
        messages=conversation_history,
    )

    answer = response.content[0].text

    # Add assistant response to history
    conversation_history.append({"role": "assistant", "content": answer})

    return answer, conversation_history


# ============================================================================
# EXAMPLES AND TESTS
# ============================================================================

if __name__ == "__main__":
    print("=" * 80)
    print("SIMPLE RAG DEMONSTRATION")
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
RAG IS SIMPLE:
1. Search your documents (keyword search works!)
2. Put relevant docs in the prompt
3. Ask Claude to answer based on those docs

THAT'S ALL RAG IS.

No vector databases required for many use cases.
No complex chunking strategies needed to start.
No frameworks needed.

Start simple. Add complexity only when needed.

WHEN TO ADD COMPLEXITY:
- 1,000+ documents → Consider better search (BM25, embeddings)
- Long documents → Add chunking
- Need semantic search → Add embeddings + vector DB
- But start with simple keyword search first!

YOU JUST RAN PRODUCTION-READY RAG IN ~300 LINES.
"""
    )


"""
COMPREHENSIVE RAG GUIDE:

1. WHAT IS RAG?

   RAG = Retrieval Augmented Generation
   
   Breaking it down:
   - RETRIEVAL: Find relevant information from your documents
   - AUGMENTED: Add that information to the LLM prompt
   - GENERATION: LLM generates answer based on retrieved info
   
   Why RAG?
   - LLMs don't know YOUR specific data
   - LLMs have knowledge cutoffs
   - RAG gives LLMs access to current, specific information

2. THE THREE STEPS:

   Step 1: RETRIEVE
   ----------------
   Find relevant documents from your collection.
   
   Simple approach (this file):
   - Keyword matching
   - Count word overlaps
   - Sort by relevance
   
   Advanced approaches:
   - BM25 algorithm (better keyword search)
   - Embeddings + vector similarity (semantic search)
   - Hybrid (keyword + semantic)
   
   Step 2: AUGMENT
   ---------------
   Put retrieved documents into the prompt.
   
   context = "Document 1: ..." + "Document 2: ..." + ...
   prompt = f"Based on these documents: {context}\nQuestion: {question}"
   
   That's it! Just string concatenation.
   
   Step 3: GENERATE
   ---------------
   Send augmented prompt to LLM, get answer.
   
   response = client.messages.create(messages=[{"role": "user", "content": prompt}])
   
   Done!

3. SIMPLE KEYWORD SEARCH:

   def simple_search(query, documents):
       query_words = query.lower().split()
       results = []
       
       for doc in documents:
           matches = sum(1 for word in query_words if word in doc['content'].lower())
           if matches > 0:
               results.append({"doc": doc, "score": matches})
       
       results.sort(key=lambda x: x["score"], reverse=True)
       return [r["doc"] for r in results[:3]]
   
   This works for:
   - Small document collections (< 1,000 docs)
   - Technical documentation
   - FAQ databases
   - Knowledge bases
   
   When to upgrade:
   - Need semantic understanding ("Python tutorial" should match "Learn Python")
   - Large document collections (> 10,000)
   - Multi-language support
   - Typo tolerance

4. DOCUMENT STRUCTURE:

   Keep it simple:
   
   documents = [
       {
           "id": "unique_id",
           "title": "Document Title",
           "content": "Full text content...",
           "metadata": {  # Optional
               "author": "...",
               "date": "...",
               "tags": [...]
           }
       }
   ]
   
   Load from:
   - Text files (read and parse)
   - Database (query and format)
   - APIs (fetch and structure)
   - PDFs (extract text with pypdf or similar)

5. LOADING DOCUMENTS FROM FILES:

   import os
   
   def load_documents_from_folder(folder_path):
       documents = []
       
       for filename in os.listdir(folder_path):
           if filename.endswith('.txt'):
               with open(os.path.join(folder_path, filename), 'r') as f:
                   content = f.read()
                   documents.append({
                       "id": filename,
                       "title": filename.replace('.txt', ''),
                       "content": content
                   })
       
       return documents
   
   # Usage
   docs = load_documents_from_folder('./knowledge_base/')

6. CHUNKING (when documents are too long):

   def chunk_document(doc, chunk_size=500, overlap=50):
       \"""Split long documents into smaller chunks.\"""
       content = doc['content']
       words = content.split()
       chunks = []
       
       for i in range(0, len(words), chunk_size - overlap):
           chunk_words = words[i:i + chunk_size]
           chunks.append({
               "id": f"{doc['id']}_chunk_{i}",
               "title": doc['title'],
               "content": ' '.join(chunk_words),
               "parent_doc": doc['id']
           })
       
       return chunks
   
   When to chunk:
   - Documents longer than ~2000 words
   - Want precise retrieval
   - Limited context window
   
   Chunking strategies:
   - Fixed size (simple, shown above)
   - Sentence boundaries (better quality)
   - Paragraph boundaries (best for coherence)
   - Semantic chunks (advanced, needs ML)

7. IMPROVING SEARCH QUALITY:

   Simple improvements without vector databases:
   
   a) Weight title matches higher:
   def search_with_title_boost(query, documents):
       query_words = set(query.lower().split())
       results = []
       
       for doc in documents:
           title_matches = sum(1 for word in query_words if word in doc['title'].lower())
           content_matches = sum(1 for word in query_words if word in doc['content'].lower())
           
           # Title matches worth 3x content matches
           score = (title_matches * 3) + content_matches
           
           if score > 0:
               results.append({"doc": doc, "score": score})
       
       results.sort(key=lambda x: x["score"], reverse=True)
       return [r["doc"] for r in results[:3]]
   
   b) Filter out common words (stopwords):
   STOPWORDS = {'the', 'a', 'an', 'is', 'are', 'was', 'were', 'in', 'on', 'at', 'to', 'for'}
   
   query_words = [w for w in query.lower().split() if w not in STOPWORDS]
   
   c) Use fuzzy matching (typo tolerance):
   from difflib import SequenceMatcher
   
   def fuzzy_match(word1, word2, threshold=0.8):
       ratio = SequenceMatcher(None, word1, word2).ratio()
       return ratio >= threshold   

8. HANDLING "NOT FOUND" GRACEFULLY:

   if not relevant_docs:
       return "I couldn't find information about that in the available documents. " \
              "Could you rephrase your question or ask about something else?"
   
   Or let Claude handle it:
   prompt = f\"""Documents: {context}
   
   Question: {question}
   
   If the documents don't contain enough information to answer, say:
   "I don't have enough information in these documents to answer that question."
   \"""       

9. CITATIONS AND SOURCES:

   Always return sources so users can verify:
   
   return {
       "answer": "FastAPI was created by Sebastián Ramírez...",
       "sources": [
           {"id": "doc2", "title": "FastAPI Framework"},
           {"id": "doc4", "title": "API Design"}
       ]
   }
   
   In production:
   - Show clickable source links
   - Display source snippets
   - Allow users to explore sources

10. RAG + CONVERSATION MEMORY:

    Combine RAG with conversation history:
    
    def conversational_rag(question, docs, history):
        # Retrieve docs for THIS question
        relevant_docs = search(question, docs)
        
        # Build context
        context = format_docs(relevant_docs)
        
        # System prompt with context
        system = f"Answer based on: {context}"
        
        # Add question to history
        history.append({"role": "user", "content": question})
        
        # Call Claude with system + history
        response = client.messages.create(
            system=system,
            messages=history
        )
        
        # Add answer to history
        history.append({"role": "assistant", "content": response.content[0].text})
        
        return response.content[0].text, history

11. WHEN TO USE EMBEDDINGS / VECTOR DATABASES:

    Start simple (keyword search).
    
    Upgrade to embeddings when:
    - Need semantic search ("car" should match "automobile")
    - Multi-language search
    - 10,000+ documents
    - Synonym handling is critical
    
    But keyword search is enough for:
    - Technical docs (exact terms)
    - FAQs
    - Small to medium knowledge bases
    - MVP/prototyping
    
    Don't over-engineer!

12. PRODUCTION CHECKLIST:

    ✅ Load documents efficiently (cache in memory or DB)
    ✅ Handle empty search results gracefully
    ✅ Return sources/citations
    ✅ Add error handling
    ✅ Log queries for analysis
    ✅ Monitor retrieval quality
    ✅ Implement caching for common queries
    ✅ Set max context size (don't exceed token limits)
    ✅ Test with diverse questions
    ✅ Provide feedback mechanism

13. COMMON MISTAKES:

    ❌ Over-complicating search from the start
    ❌ Not returning sources
    ❌ Retrieving too many documents (context overload)
    ❌ Retrieving too few documents (missing info)
    ❌ Not handling "no results" case
    ❌ Forgetting to update documents regularly
    ❌ No way to verify accuracy
    
    ✅ Start simple, add complexity when needed
    ✅ Always cite sources
    ✅ Start with 3-5 document retrieval
    ✅ Handle edge cases
    ✅ Keep documents up to date
    ✅ Make sources accessible

14. TESTING YOUR RAG:

    Test questions to try:
    - Factual questions ("What is X?")
    - Comparison questions ("What's the difference between X and Y?")
    - Questions requiring multiple docs
    - Questions with no answer in docs
    - Follow-up questions (conversational)
    - Ambiguous questions
    
    Check:
    - Are the right documents retrieved?
    - Does the answer use the documents?
    - Are sources cited correctly?
    - Does it say "I don't know" when appropriate?

15. SCALING UP:

    Small (< 100 docs):
    - List in memory
    - Simple keyword search
    - This file's approach
    
    Medium (100-10,000 docs):
    - SQLite with FTS5 (full-text search)
    - PostgreSQL with tsvector
    - Still simple, fast, no vector DB needed
    
    Large (10,000+ docs):
    - Consider embeddings
    - Vector databases (Pinecone, Weaviate, pgvector)
    - Or: Elasticsearch, Algolia
    
    But start small!

NEXT STEPS:
- Run this file and see RAG in action
- Try your own documents
- Experiment with different questions
- Build a document Q&A system
- Add to your SaaS applications

RAG is simple. Don't let the industry convince you otherwise.
"""
