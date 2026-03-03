# Learn AI Right: AI Development Without Frameworks

**Learn AI fundamentals without frameworks. Just Python, APIs, and clarity.**

![Learn AI Right Hero Image](assets/learn_ai_right_hero.jpg)

## Why This Exists

When I started learning AI development, I found endless tutorials on various frameworks and libraries. But when something broke, I had no idea what was actually happening under the hood. I couldn't debug issues, optimize performance, or make informed architectural decisions.

This course fills that gap. It teaches you what AI systems actually do, stripped of abstractions and marketing jargon. You'll learn the foundational patterns that all AI applications use - whether they admit it or not.

## The Philosophy

**Frameworks have their place.** I use them. I like several of them. But jumping into a framework without understanding the fundamentals is inefficient. You build on shaky ground.

This course teaches you what's really happening when you:

- Chat with an AI
- Give it memory
- Make it use tools
- Have it search your documents
- Build multi-step workflows

Once you understand these patterns, you can use any framework effectively—or build exactly what you need without one.

## What AI Actually Is

The industry loves complex terminology. Here's what things really are:

| Industry Term                            | What It Actually Is                                                     |
| ---------------------------------------- | ----------------------------------------------------------------------- |
| **AI Agents**                            | Python functions the AI decides to call                                 |
| **Memory/Context**                       | A Python list of messages you send with each request                    |
| **RAG (Retrieval Augmented Generation)** | Search for relevant text + add to prompt + ask AI                       |
| **Multi-Agent Systems**                  | Sequential API calls with logic between them                            |
| **Embeddings/Vector DBs**                | Useful for large datasets, but keyword search works fine for most cases |
| **Prompt Chaining**                      | Call AI → process result → call AI again                                |

That's it. No magic. Just API calls and basic programming.

## What You'll Learn

This course now follows a clean **10-step canonical path**:

1. **First AI Call** - The basic pattern every AI application uses
2. **Memory as List** - The stateless truth behind chatbots
3. **Memory with `previous_response_id`** - OpenAI convenience chaining
4. **Structured Outputs** - Turning model output into typed, validated data
5. **Tool Calling** - Making AI take actions through functions
6. **RAG** - Making AI answer questions from your documents
7. **Conversational RAG** - Adding follow-up questions to document Q&A
8. **Streaming** - Displaying AI responses word-by-word in real-time
9. **Prompt Chaining** - Building multi-step AI workflows
10. **Capstone (OpenAI-only)** - One end-to-end project combining everything

By the end, you'll understand how production AI systems work under the hood.

## API Versions in This Repo

- OpenAI examples use the **Responses API** (`client.responses.create(...)`), which is the recommended primary API for new projects.
- Anthropic examples use the current `messages` API patterns.
- Models are configurable via env vars:
  - `OPENAI_MODEL` (default in examples: `gpt-4.1`)
  - `ANTHROPIC_MODEL` (default in examples: `claude-sonnet-4-6`)

## Prerequisites

**You only need to know Python.** That's it.

No machine learning background. No advanced math. No framework experience.

If you can write functions, loops, and understand lists and dictionaries, you're ready.

## Quick Start

**1. Clone this repository**

```bash
git clone https://github.com/jmedia65/learn-ai-right.git
cd learn-ai-right
```

**2. Install dependencies**

```bash
pip install -r requirements.txt
```

**3. Set up your API keys**

Copy `.env.example` to `.env`:

```bash
cp .env.example .env
```

Add your API keys to `.env`:

```
ANTHROPIC_API_KEY=your_anthropic_key_here
OPENAI_API_KEY=your_openai_key_here
# Optional:
# ANTHROPIC_MODEL=claude-sonnet-4-6
# OPENAI_MODEL=gpt-4.1
```

Get API keys:

- Anthropic: https://console.anthropic.com/
- OpenAI: https://platform.openai.com/api-keys

**4. Start with the first module**

```bash
cd 01-first-ai-call
python 01_anthropic_basic.py
```

## Course Structure

Each module contains:

- A README explaining the concept
- OpenAI examples (all steps)
- Anthropic companion examples (most steps)
- Heavily commented code showing exactly what's happening

Work through them in order:

### [01 - First AI Call](./01-first-ai-call)

Learn the foundational pattern: initialize → call → extract response.

📖 [Read the full article](https://maxbraglia.substack.com/p/your-first-ai-call-the-foundation-of-everything)

### [02 - Memory as List](./02-memory-list)

Understand how chatbots remember context (spoiler: it's just a list).

📖 [Read the full article](https://maxbraglia.substack.com/p/ai-conversation-memory-its-just-a-list)

### [03 - Memory with `previous_response_id` (OpenAI)](./03-memory-previous-response-id)

Learn OpenAI's state-chaining convenience API after mastering list-based memory.

### [04 - Structured Outputs](./04-structured-outputs)

Bridge module: get typed, validated outputs before tool calling.

### [05 - Tool Calling](./05-tool-calling)

Make AI take actions by calling your Python functions.

📖 [Read the full article](https://maxbraglia.substack.com/p/tool-calling-making-ai-do-things)

### [06 - RAG](./06-rag)

Make AI answer questions from your own documents.

📖 [Read the full article](https://maxbraglia.substack.com/p/rag-making-ai-answer-from-your-documents)

### [07 - Conversational RAG](./07-conversational-rag)

Add follow-up questions to your document Q&A system.

📖 [Read the full article](https://maxbraglia.substack.com/p/conversational-rag-adding-follow-up-questions)

### [08 - Streaming](./08-streaming)

Display AI responses in real-time, word by word.

📖 [Read the full article](https://maxbraglia.substack.com/p/streaming-responses-making-ai-feel-alive)

### [09 - Prompt Chaining](./09-prompt-chaining)

Build multi-step AI workflows and "agent" systems.

📖 [Read the full article](https://maxbraglia.substack.com/p/prompt-chaining-building-multi-step-workflows)

### [10 - Capstone (OpenAI-only)](./10-capstone-openai)

Build one complete AI Learning Coach that combines memory, structured outputs, tools, RAG, streaming, and chaining.

## About

I'm [Max Braglia](https://maxbraglia.com/), and I write about AI engineering at [maxbraglia.substack.com](https://maxbraglia.substack.com). I built this course because I wish it existed when I started learning AI development.

If you find this valuable, consider [subscribing to my newsletter](https://maxbraglia.substack.com) where I share practical AI development insights.

## License

MIT License - use this code however you want. Learn, build, teach others.
