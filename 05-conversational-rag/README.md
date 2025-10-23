# Conversational RAG

## Core Concept

Combine two patterns you've already learned: **RAG + conversation memory**.

The key insight: **On each turn, retrieve documents for the NEW question, but maintain the conversation history.**

This lets users ask follow-up questions like "Who created it?" and the AI understands "it" refers to the topic from the previous turn, while still having access to fresh, relevant documents.

## What You'll Learn

- How to combine document retrieval with conversation memory
- When to refresh documents (every turn) vs. when to preserve context (history)
- How the AI uses both fresh documents AND conversation history to understand context
- The difference between Anthropic's system parameter and OpenAI's system message approach

## Files in This Module

- [01_anthropic_conversational_rag.py](./01_anthropic_conversational_rag.py) - Conversational RAG with Claude
- [02_openai_conversational_rag.py](./02_openai_conversational_rag.py) - Conversational RAG with GPT

Both examples use the same documents from module 04.

## Key Takeaway

Conversational RAG pattern:

1. User asks a question
2. **Search documents for THIS question** (fresh retrieval)
3. Build system prompt with retrieved documents
4. **Send full conversation history** (for context)
5. AI uses both documents AND conversation to answer
6. Add response to conversation history
7. Repeat

Fresh documents + conversation memory = natural follow-up questions.

## Read the Full Article

📖 [Conversational RAG: Adding Follow-Up Questions](https://maxbraglia.substack.com/p/conversational-rag-adding-follow-up-questions)

## Next Step

Make your AI responses feel more alive with streaming:

👉 [06 - Streaming](../06-streaming)
