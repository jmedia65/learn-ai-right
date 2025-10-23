# Conversation Memory

## Core Concept

AI conversation memory is simpler than it sounds: **it's just a Python list**.

LLMs like Claude and GPT are stateless—they have no memory between API calls. The illusion of memory works because you send the complete conversation history with every request. That's it. No complex architecture, no special databases, just a list of messages.

## What You'll Learn

- How chatbots "remember" previous messages (spoiler: they don't, you do)
- The five-step pattern for multi-turn conversations
- How to build both scripted and interactive chat experiences
- Why conversations get more expensive as they get longer

## Files in This Module

### Part 1: Turn-by-Turn Conversations (Scripted Examples)
These examples show 4 hardcoded conversation turns to demonstrate the pattern clearly:

- [01_anthropic_conversation.py](./01_anthropic_conversation.py) - Multi-turn conversation with Claude (4 scripted turns)
- [02_openai_conversation.py](./02_openai_conversation.py) - Multi-turn conversation with GPT (4 scripted turns)

### Part 2: Interactive Chat Loops (Practical Application)
These examples wrap the same pattern in a `while` loop for real-time interaction:

- [03_anthropic_while_loop.py](./03_anthropic_while_loop.py) - Interactive chat with Claude (user input)
- [04_openai_while_loop.py](./04_openai_while_loop.py) - Interactive chat with GPT (user input)

**Learning Path:** Start with files 01-02 to understand the pattern, then try files 03-04 to see it in action.

## Key Takeaway

Every chatbot, from ChatGPT to custom applications, follows this simple loop:

1. Append user message to history list
2. Send entire history to API
3. Extract the response
4. Display it
5. Append assistant message to history

**Turn-by-turn examples:** Pattern repeated 4 times with hardcoded messages
**While loop examples:** Pattern wrapped in `while True:` with user input

That's it. No magic. Just a Python list and sequential API calls.

## Read the Full Article

📖 [AI Conversation Memory: It's Just a List](https://maxbraglia.substack.com/p/ai-conversation-memory-its-just-a-list)

## Next Step

Now that AI can remember context, let's make it take actions:

👉 [03 - Tool Calling](../03-tool-calling)
