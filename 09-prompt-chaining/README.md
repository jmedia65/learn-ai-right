# Prompt Chaining

## Core Concept

"Multi-agent systems," "AI orchestration," "agent workflows"—these sound complex. Here's what they actually are:

**Call AI → Process result → Call AI → Process result → Call AI**

That's it. Sequential API calls with logic between them. Each step's output becomes the next step's input. No frameworks required.

## What You'll Learn

- How to chain multiple AI calls together into workflows
- Common patterns: linear chains, conditional chains, iterative chains
- How to combine prompt chaining with other concepts (streaming, RAG, tools)
- When frameworks add value vs. when they're unnecessary

## Files in This Module

- [01_anthropic_chaining.py](./01_anthropic_chaining.py) - Multi-step workflows with Claude
- [02_openai_chaining.py](./02_openai_chaining.py) - Multi-step workflows with GPT

Both examples demonstrate a 3-step content creation pipeline: Research → Write → Edit.

## Key Takeaway

Common prompt chaining patterns:

- **Linear chains**: Step 1 → Step 2 → Step 3 (research → write → edit)
- **Conditional chains**: Classify → Branch based on result → Different handlers
- **Iterative chains**: Generate → Critique → Improve → Repeat until satisfied
- **Parallel chains**: Multiple analyses → Combine results

All of these are just API calls with Python logic between them.
Each step checks completion before passing its output to the next step, including the streamed edit.

## Quick Exercise (10 Minutes)

1. Add a fourth step: "fact-check draft against research."
2. If fact-check fails, branch to rewrite.
3. Print each intermediate output length and summary.

Done when: you can debug the chain step-by-step instead of only reading final output.

## What Breaks in Production

- Error propagation: a weak early step poisons later steps.
- No observability: hard to diagnose which step failed.
- Cost sprawl: many chained calls can become expensive quickly.

## Next Step

You are ready for the full integration challenge:

👉 [10 - Capstone (OpenAI-only)](../10-capstone-openai)
