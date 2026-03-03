# Memory with `previous_response_id` (OpenAI)

## Core Concept

In step 2, memory was explicit: a Python list you resend each call.

OpenAI also provides a convenience mechanism: `previous_response_id`.
You can chain responses without manually re-sending the full message list.

## Why This Step Exists

- Step 2 taught the **stateless truth** (you control memory).
- Step 3 teaches a **modern convenience** (SDK-assisted conversation state).

You should understand both.

## What You'll Learn

- How to continue a conversation by passing `previous_response_id`
- How this differs from manually managing a message history list
- Tradeoffs between explicit control and convenience

## Files in This Module

- [01_openai_previous_response_id.py](./01_openai_previous_response_id.py) - scripted multi-turn example
- [02_openai_previous_response_id_loop.py](./02_openai_previous_response_id_loop.py) - interactive chat loop

## Key Takeaway

`previous_response_id` is not magic memory. It is a convenience API for conversation chaining.

## Next Step

Turn model output into reliable typed data:

👉 [04 - Structured Outputs](../04-structured-outputs)
