# RAG (Retrieval Augmented Generation)

## Core Concept

The industry makes RAG sound complex: "You need vector databases! Embedding models! Complex chunking strategies!"

The reality: **RAG is search + put in prompt + ask AI**. That's it.

Find relevant documents, include them in your prompt, and ask the AI to answer based on that context. For many real-world use cases, simple keyword search works fine. No vector databases required.

## What You'll Learn

- The three-step RAG process: Retrieve → Augment → Generate
- How to implement simple keyword search (no embeddings needed)
- How to build context from retrieved documents
- How to instruct the AI to answer only from provided sources
- When keyword search is enough vs. when you need semantic search

## Files in This Module

- [01_anthropic_rag.py](./01_anthropic_rag.py) - Basic RAG with Claude
- [02_openai_rag.py](./02_openai_rag.py) - Basic RAG with GPT
- [sample_documents.py](./sample_documents.py) - Sample document collection

Both examples use the same simple keyword search and document set.

## Key Takeaway

RAG in three steps:

1. **Retrieve**: Search your documents for relevant content (keyword matching works for many cases)
2. **Augment**: Add those documents to your prompt as context
3. **Generate**: Ask the AI to answer based only on the provided documents

This prevents hallucinations and grounds responses in your actual data.

## Read the Full Article

📖 [RAG: Making AI Answer From Your Documents](https://maxbraglia.substack.com/p/rag-making-ai-answer-from-your-documents)

## Next Step

Add conversation memory to your RAG system for follow-up questions:

👉 [05 - Conversational RAG](../05-conversational-rag)
