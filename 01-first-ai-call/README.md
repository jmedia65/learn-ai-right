# Your First AI Call

## Core Concept

Every AI application follows the same foundational pattern: **initialize a client → send input → extract the response**. That's it. Whether you're building a chatbot, a code generator, or a complex AI system, this three-step pattern is always there.

## What You'll Learn

- How to make your first API call to Claude (Anthropic) and GPT (OpenAI Responses API)
- The anatomy of a request: model, tokens, and input/messages
- How to extract the AI's response from the API response object
- What metadata the API returns (token usage, stop reasons, model info)

## Files in This Module

- [01_anthropic_basic.py](./01_anthropic_basic.py) - Your first call to Claude
- [02_openai_basic.py](./02_openai_basic.py) - Your first call to GPT

Both examples do the same thing using different APIs. Compare them to see the similarities and differences.

## Key Takeaway

You don't need a framework to talk to an AI. You need:

1. An API client (Anthropic or OpenAI)
2. Input (a string or a messages list)
3. Code to extract the response

Everything else in AI development builds on this pattern.

## Quick Exercise (10 Minutes)

1. Change the prompt to: "Explain REST vs GraphQL in two sentences."
2. Run both scripts and compare output style.
3. Print model + token usage from each response object.

Done when: you can point to where the actual text lives in each SDK response.

## What Breaks in Production

- Missing/invalid API keys: request fails before generation.
- Hard-coded model IDs: examples go stale over time.
- No output checks: empty/partial responses can silently propagate.

## Next Step

Once you understand basic API calls, learn how to give AI memory:

👉 [02 - Conversation Memory](../02-memory-list)
