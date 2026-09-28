# Conversational RAG

## Core Concept

Combine two patterns you've already learned: **RAG + conversation memory**.

The key insight: **On each turn, retrieve documents for the NEW question, but maintain the conversation history.**

This lets users ask follow-up questions like "Who created it?" and the AI understands "it" refers to the topic from the previous turn, while still having access to fresh, relevant documents.

## What You'll Learn

- How to combine document retrieval with conversation memory
- When to refresh documents (every turn) vs. when to preserve context (history)
- How the AI uses both fresh documents AND conversation history to understand context
- The difference between Anthropic's `system` parameter and OpenAI Responses `instructions` approach

## Files in This Module

- [01_anthropic_conversational_rag.py](./01_anthropic_conversational_rag.py) - Conversational RAG with Claude
- [02_openai_conversational_rag.py](./02_openai_conversational_rag.py) - Conversational RAG with GPT

Both examples use the same documents from module 06.

## Key Takeaway

Conversational RAG pattern:

1. User asks a question
2. **Search documents for THIS question** (fresh retrieval)
3. Build system prompt with retrieved documents
4. **Send full conversation history** (for context)
5. AI uses both documents AND conversation to answer
6. Add response to conversation history (all OpenAI output items for reasoning continuity)
7. Repeat

Fresh documents + conversation memory = natural follow-up questions.

## Quick Exercise (10 Minutes)

1. Ask: "What is FastAPI?" then "Who created it?" then "What is it built on?"
2. Clear conversation history after turn 1 and rerun.
3. Compare how follow-up accuracy changes.

Done when: you can show why retrieval alone is not enough for follow-ups.

## What Breaks in Production

- History bloat: context gets expensive and noisy.
- Reference ambiguity: pronouns like "it" resolve incorrectly.
- Mixing stale and fresh context: answers become inconsistent.

## Next Step

Make your AI responses feel more alive with streaming:

👉 [08 - Streaming](../08-streaming)
