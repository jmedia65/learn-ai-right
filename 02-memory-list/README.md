# Conversation Memory

## Core Concept

AI conversation memory is simpler than it sounds: **it's just a Python list**.

LLMs like Claude and GPT have no memory between independent API calls. Conversation continuity works because you send the history with every request. That's it. No complex architecture or special database—just a Python list. For OpenAI reasoning models, that list includes the model's full output items as well as user messages. Append the SDK's `response.output` items directly so optional fields are serialized correctly on the next call.

## What You'll Learn

- How chatbots "remember" previous messages (spoiler: they don't, you do)
- The five-step pattern for multi-turn conversations
- How to build both scripted and interactive chat experiences
- How Responses API memory can be done with explicit history lists (and when `previous_response_id` helps)
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
5. Append the assistant response to history (all output items in the OpenAI examples)

**Turn-by-turn examples:** Pattern repeated 4 times with hardcoded messages
**While loop examples:** Pattern wrapped in `while True:` with user input

That's it. No magic. Just a Python list and sequential API calls.

## Quick Exercise (10 Minutes)

1. Add a fifth turn: ask "What are my interests so far?"
2. Print `len(conversation_history)` after each turn. OpenAI may add more than one output item per turn.
3. Compare a short conversation with a longer one and note the token cost.

Done when: you can show the tradeoff between context quality and token cost.

## What Breaks in Production

- History grows forever: context-window and cost blow up.
- Missing assistant output items: reasoning context can be lost.
- No truncation strategy: long chats become slow and expensive.

## Next Step

Now learn OpenAI's memory chaining convenience with `previous_response_id`:

👉 [03 - Memory with `previous_response_id`](../03-memory-previous-response-id)
