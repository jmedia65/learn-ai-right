"""
SAMPLE DOCUMENTS FOR RAG EXAMPLES

This is a simple document collection for demonstrating RAG.
In production, you'd load these from files, databases, APIs, etc.
"""

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
