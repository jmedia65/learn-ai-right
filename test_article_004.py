###############################
# ANTHROPIC API RAG
###############################

import os
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()
client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# Your documents
DOCUMENTS = [
    {
        "id": "doc1",
        "title": "Python Basics",
        "content": """
        Python is a high-level programming language known for its 
        simplicity and readability. It was created by Guido van Rossum 
        and first released in 1991. Python supports multiple programming 
        paradigms including procedural, object-oriented, and functional 
        programming. Common use cases include web development, data 
        science, automation, and artificial intelligence.
        """,
    },
    {
        "id": "doc2",
        "title": "FastAPI Framework",
        "content": """
        FastAPI is a modern, fast web framework for building APIs with 
        Python. It was created by Sebastián Ramírez and first released 
        in 2018. FastAPI is built on top of Starlette and Pydantic, 
        providing automatic API documentation, data validation, and 
        high performance. It’s one of the fastest Python frameworks 
        available, comparable to NodeJS and Go.
        """,
    },
    {
        "id": "doc3",
        "title": "Machine Learning Basics",
        "content": """
        Machine learning is a subset of artificial intelligence that 
        enables systems to learn and improve from experience without 
        being explicitly programmed. There are three main types: 
        supervised learning, unsupervised learning, and reinforcement 
        learning. Popular frameworks include TensorFlow, PyTorch, and 
        scikit-learn.
        """,
    },
]


# Simple keyword search
def simple_keyword_search(query: str, documents: list, max_results: int = 3):
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


# RAG query function
def rag_query(question: str, documents: list, max_context_docs: int = 3):
    # 1. RETRIEVE
    relevant_docs = simple_keyword_search(question, documents, max_context_docs)

    if not relevant_docs:
        return "I couldn’t find any relevant information."

    # 2. AUGMENT
    context = ""
    for i, doc in enumerate(relevant_docs, 1):
        context += f"Document {i} - {doc['title']}:\n"
        context += doc["content"].strip() + "\n\n"

    # 3. GENERATE
    prompt = f"""Based on the following documents, answer the question.

Documents:
{context}

Question: {question}

Answer based ONLY on the documents above."""

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}],
    )

    return response.content[0].text


# Use it
answer = rag_query("What is FastAPI?", DOCUMENTS)
print(answer)


###############################
# OPENAI API RAG
###############################

import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Your documents
DOCUMENTS = [
    {
        "id": "doc1",
        "title": "Python Basics",
        "content": """
        Python is a high-level programming language known for its 
        simplicity and readability. It was created by Guido van Rossum 
        and first released in 1991. Python supports multiple programming 
        paradigms including procedural, object-oriented, and functional 
        programming. Common use cases include web development, data 
        science, automation, and artificial intelligence.
        """,
    },
    {
        "id": "doc2",
        "title": "FastAPI Framework",
        "content": """
        FastAPI is a modern, fast web framework for building APIs with 
        Python. It was created by Sebastián Ramírez and first released 
        in 2018. FastAPI is built on top of Starlette and Pydantic, 
        providing automatic API documentation, data validation, and 
        high performance. It's one of the fastest Python frameworks 
        available, comparable to NodeJS and Go.
        """,
    },
    {
        "id": "doc3",
        "title": "Machine Learning Basics",
        "content": """
        Machine learning is a subset of artificial intelligence that 
        enables systems to learn and improve from experience without 
        being explicitly programmed. There are three main types: 
        supervised learning, unsupervised learning, and reinforcement 
        learning. Popular frameworks include TensorFlow, PyTorch, and 
        scikit-learn.
        """,
    },
]


# Simple keyword search (identical to Anthropic version)
def simple_keyword_search(query: str, documents: list, max_results: int = 3):
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


# RAG query function (OpenAI version)
def rag_query(question: str, documents: list, max_context_docs: int = 3):
    # 1. RETRIEVE
    relevant_docs = simple_keyword_search(question, documents, max_context_docs)

    if not relevant_docs:
        return "I couldn't find any relevant information."

    # 2. AUGMENT
    context = ""
    for i, doc in enumerate(relevant_docs, 1):
        context += f"Document {i} - {doc['title']}:\n"
        context += doc["content"].strip() + "\n\n"

    # 3. GENERATE
    prompt = f"""Based on the following documents, answer the question.

Documents:
{context}

Question: {question}

Answer based ONLY on the documents above."""

    response = client.chat.completions.create(
        model="gpt-4o",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}],
    )

    return response.choices[0].message.content


# Use it
answer = rag_query("What is FastAPI?", DOCUMENTS)
print(answer)
