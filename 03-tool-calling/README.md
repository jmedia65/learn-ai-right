# Tool Calling

## Core Concept

"AI agents" sounds complex, but here's the reality: **the AI doesn't execute your functions. It can't.**

Instead, the AI decides which functions to call and with what parameters. You execute the actual Python code. You return the results. The AI uses those results to formulate its response.

Tool calling = AI orchestrates, you execute.

## What You'll Learn

- How to define tool schemas that describe your functions to the AI
- The request-execute-return loop that powers tool calling
- How to handle multiple sequential tool calls
- The differences between Anthropic and OpenAI tool formats

## Files in This Module

- [01_anthropic_tools.py](./01_anthropic_tools.py) - Tool calling with Claude
- [02_openai_tools.py](./02_openai_tools.py) - Tool calling with GPT

Both examples use the same weather and user info functions but different API formats.

## Key Takeaway

Every "AI agent" system follows this pattern:

1. Define function schemas (descriptions + parameters)
2. AI analyzes user request and decides which tools are needed
3. AI specifies which function to call with exact parameters
4. **You** execute the Python code
5. **You** return results to the AI
6. AI incorporates findings into its response

Loop until AI stops requesting tools.

## Read the Full Article

📖 [Tool Calling: Making AI DO Things](https://maxbraglia.substack.com/p/tool-calling-making-ai-do-things)

## Next Step

Now that AI can take actions, let's make it answer questions from your documents:

👉 [04 - RAG](../04-rag)
