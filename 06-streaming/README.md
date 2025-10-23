# Streaming Responses

## Core Concept

Streaming makes AI responses appear word-by-word in real-time instead of waiting for the complete answer.

**The psychology**: Users perceive streamed responses as 30-40% faster even when total time is similar, because they can start reading within milliseconds rather than waiting seconds for completion.

**The reality**: Streaming is just iterating through response chunks as they arrive from the API.

## What You'll Learn

- The difference between non-streaming and streaming responses
- How to display text chunks in real-time with `flush=True`
- How to accumulate the full response while streaming for conversation history
- When to use streaming vs. non-streaming

## Files in This Module

- [01_anthropic_streaming.py](./01_anthropic_streaming.py) - Streaming with Claude
- [02_openai_streaming.py](./02_openai_streaming.py) - Streaming with GPT

Both examples compare non-streaming vs. streaming side-by-side.

## Key Takeaway

Streaming in three steps:

1. Use `.stream()` instead of `.create()` (wrapped in context manager)
2. Iterate through chunks as they arrive
3. Print immediately with `flush=True` to bypass Python's output buffering

The total processing time is similar, but the user experience is dramatically better.

## Read the Full Article

📖 [Streaming Responses: Making AI Feel Alive](https://maxbraglia.substack.com/p/streaming-responses-making-ai-feel-alive)

## Next Step

Build complex multi-step workflows with prompt chaining:

👉 [07 - Prompt Chaining](../07-prompt-chaining)
