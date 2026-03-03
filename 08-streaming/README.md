# Streaming Responses

## Core Concept

Streaming makes AI responses appear word-by-word in real-time instead of waiting for the complete answer.

**The psychology**: Users perceive streamed responses faster even when total time is similar, because they can start reading within milliseconds rather than waiting seconds for completion.

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

1. Enable streaming (`client.messages.stream(...)` for Anthropic, `stream=True` for OpenAI Responses)
2. Iterate through chunks/events as they arrive
3. Print immediately with `flush=True` to bypass Python's output buffering

The total processing time is similar, but the user experience is dramatically better.

## Quick Exercise (10 Minutes)

1. Time non-streaming vs streaming with `time.perf_counter()`.
2. Record time-to-first-text and total completion time.
3. Keep accumulating full text and append it to conversation history.

Done when: you can quantify UX improvement even when total latency is similar.

## What Breaks in Production

- Dropped stream events: partial outputs shown to users.
- No final accumulation: follow-up context is incomplete.
- Backpressure issues: UI freezes on long streams.

## Read the Full Article

📖 [Streaming Responses: Making AI Feel Alive](https://maxbraglia.substack.com/p/streaming-responses-making-ai-feel-alive)

## Next Step

Build complex multi-step workflows with prompt chaining:

👉 [09 - Prompt Chaining](../09-prompt-chaining)
