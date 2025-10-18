import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Documents
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


# Search function (identical to Anthropic version)
def simple_keyword_search(query, documents, max_results=3):
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


# Conversational RAG function (OpenAI version)
def conversational_rag(question, documents, conversation_history):
    # Retrieve docs for this question
    relevant_docs = simple_keyword_search(question, documents, max_results=3)

    if not relevant_docs:
        return ("I couldn't find relevant information.", conversation_history)

    # Build context
    context = ""
    for doc in relevant_docs:
        context += f"{doc['title']}:\n{doc['content'].strip()}\n\n"

    # Build system message
    system_message = f"""You are a helpful assistant that answers questions based on provided documents.

Available documents:
{context}

Instructions:
- Answer based on the documents provided
- Use conversation history for context
- If asked a follow-up question, remember previous exchanges
- Cite which document you're using when possible"""

    # Handle system message in conversation history
    # OpenAI requires system message IN the messages array
    if not conversation_history or conversation_history[0]["role"] != "system":
        conversation_history.insert(0, {"role": "system", "content": system_message})
    else:
        # Update system message with new documents
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

    # Add response
    conversation_history.append({"role": "assistant", "content": answer})

    return answer, conversation_history


# Usage
conversation_history = []

# Turn 1
print("User: What is FastAPI?")
answer1, conversation_history = conversational_rag(
    "What is FastAPI?", DOCUMENTS, conversation_history
)
print(f"Assistant: {answer1}\n")

# Turn 2
print("User: Who created it?")
answer2, conversation_history = conversational_rag(
    "Who created it?", DOCUMENTS, conversation_history
)
print(f"Assistant: {answer2}\n")
