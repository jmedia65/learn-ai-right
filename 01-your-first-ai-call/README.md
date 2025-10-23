# Your First AI Call

## Core Concept

Every AI application follows the same foundational pattern: **initialize a client → send messages → extract the response**. That's it. Whether you're building a chatbot, a code generator, or a complex AI system, this three-step pattern is always there.

## What You'll Learn

- How to make your first API call to Claude (Anthropic) and GPT (OpenAI)
- The anatomy of a request: model, max_tokens, and messages
- How to extract the AI's response from the API response object
- What metadata the API returns (token usage, stop reasons, model info)

## Files in This Module

- [01_anthropic_basic.py](./01_anthropic_basic.py) - Your first call to Claude
- [02_openai_basic.py](./02_openai_basic.py) - Your first call to GPT

Both examples do the same thing using different APIs. Compare them to see the similarities and differences.

## Key Takeaway

You don't need a framework to talk to an AI. You need:
1. An API client (Anthropic or OpenAI)
2. A messages array with user input
3. Code to extract the response

Everything else in AI development builds on this pattern.

## Read the Full Article

📖 [Your First AI Call: The Foundation of Everything](https://maxbraglia.substack.com/p/your-first-ai-call-the-foundation-of-everything)

## Next Step

Once you understand basic API calls, learn how to give AI memory:

👉 [02 - Conversation Memory](../02-conversation-memory)
