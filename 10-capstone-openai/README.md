# Capstone (OpenAI Only): AI Learning Coach

## Goal

Build one end-to-end assistant that combines all previous steps into a practical project.

## What This Capstone Combines

1. **First call** - Responses API foundation
2. **Memory as list** - conceptual baseline from earlier steps
3. **Memory with `previous_response_id`** - turn-to-turn state
4. **Structured outputs** - intent parsing via `responses.parse`
5. **Tool calling** - function execution loop with `function_call_output`
6. **RAG** - keyword retrieval over course documents
7. **Conversational RAG** - follow-up questions with memory + fresh retrieval
8. **Streaming** - event-based real-time final response
9. **Prompt chaining** - plan -> answer -> polish

## Files

- [01_openai_capstone_learning_coach.py](./01_openai_capstone_learning_coach.py)

## Run

```bash
cd 10-capstone-openai
python 01_openai_capstone_learning_coach.py
```

## Quick Exercise (15 Minutes)

1. Add one new lesson document to the capstone corpus.
2. Add one new tool (e.g., `get_study_plan(level)`).
3. Ask a question that triggers retrieval, tool use, and streaming.

Done when: one user request clearly passes through routing -> retrieval -> tools -> polished streamed answer.

## What Breaks in Production

- Orchestration coupling: one step change can break the full pipeline.
- Missing evaluation: polished output can still be wrong.
- Retry/timeouts not handled: long multi-step flows fail unpredictably.

## Next Challenges

- Replace fake tools with real APIs (calendar, LMS, docs index)
- Swap keyword retrieval for embeddings at larger scale
- Add evaluation checks for answer quality and source grounding
