# Structured Outputs

## Core Concept

Before tools and agents, there is a simpler superpower: **reliable structured outputs**.

Instead of hoping the model returns a format you can parse, you define a schema and validate the result. This turns AI output from "nice text" into data your code can trust.

## Why This Module Exists

This is a bridge between:
- **02 - Conversation Memory** (context)
- **03 - Tool Calling** (actions)

If students skip structure, tool calling and workflows feel brittle fast.

## What You'll Learn

- Why plain-text prompting is fragile for production logic
- How to define output schemas with `pydantic`
- How OpenAI's Responses API can parse directly into typed objects
- How to validate Anthropic JSON outputs with schema checks
- How structured outputs improve chaining, routing, and evaluation

## Files in This Module

- [01_anthropic_structured_output.py](./01_anthropic_structured_output.py) - Claude + JSON + pydantic validation
- [02_openai_structured_output.py](./02_openai_structured_output.py) - Responses API parsing into typed objects

## Key Takeaway

Prompting for text is useful.
Prompting for **typed, validated data** is what makes AI systems dependable.

Structured outputs are often the missing step between beginner demos and real applications.

## Recommended Placement

Take this module **after 02** and **before 03**.

## Next Step

Now you're ready for action-taking workflows:

👉 [03 - Tool Calling](../03-tool-calling)
