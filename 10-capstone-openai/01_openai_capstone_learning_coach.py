"""
CAPSTONE - OPENAI ONLY
AI Learning Coach that combines all course patterns.

Patterns used:
- Responses API baseline
- previous_response_id conversation chaining
- Structured outputs (responses.parse + pydantic)
- Tool calling loop (function_call / function_call_output)
- RAG retrieval
- Prompt chaining (plan -> answer -> polish)
- Streaming final output
"""

import json
import os
from typing import Literal

from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel, Field

load_dotenv()
MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1")
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# =============================================================================
# DATA (RAG corpus + tool data)
# =============================================================================

LESSON_DOCS = [
    {
        "id": "doc1",
        "title": "First AI Call",
        "content": "Initialize client, send input/messages, extract output text from response.",
    },
    {
        "id": "doc2",
        "title": "Memory as List",
        "content": "LLMs are stateless. Conversation memory comes from resending message history.",
    },
    {
        "id": "doc3",
        "title": "previous_response_id",
        "content": "OpenAI Responses API can chain turns using previous_response_id for convenience.",
    },
    {
        "id": "doc4",
        "title": "Structured Outputs",
        "content": "Use schemas and validation so outputs become reliable data, not fragile text.",
    },
    {
        "id": "doc5",
        "title": "Tool Calling",
        "content": "Model decides tool calls, developer executes functions, then returns function_call_output.",
    },
    {
        "id": "doc6",
        "title": "RAG",
        "content": "Retrieve relevant docs, inject context, answer with grounding in provided information.",
    },
    {
        "id": "doc7",
        "title": "Streaming",
        "content": "Use stream=True and consume response.output_text.delta for real-time UX.",
    },
    {
        "id": "doc8",
        "title": "Prompt Chaining",
        "content": "Compose multi-step workflows where each model output becomes next step input.",
    },
]

MODULE_GUIDE = {
    "01": {"name": "First Call", "prereq": []},
    "02": {"name": "Memory as List", "prereq": ["01"]},
    "03": {"name": "previous_response_id", "prereq": ["02"]},
    "04": {"name": "Structured Outputs", "prereq": ["02", "03"]},
    "05": {"name": "Tool Calling", "prereq": ["04"]},
    "06": {"name": "RAG", "prereq": ["05"]},
    "07": {"name": "Conversational RAG", "prereq": ["06"]},
    "08": {"name": "Streaming", "prereq": ["03"]},
    "09": {"name": "Prompt Chaining", "prereq": ["05", "06", "08"]},
    "10": {"name": "Capstone", "prereq": ["01", "02", "03", "04", "05", "06", "08", "09"]},
}


# =============================================================================
# RETRIEVAL
# =============================================================================


def keyword_retrieve(query: str, docs: list[dict], max_results: int = 3) -> list[dict]:
    query_words = set(query.lower().split())
    scored = []
    for doc in docs:
        haystack = (doc["title"] + " " + doc["content"]).lower()
        score = sum(1 for word in query_words if word in haystack)
        if score > 0:
            scored.append((score, doc))

    scored.sort(key=lambda x: x[0], reverse=True)
    return [doc for _, doc in scored[:max_results]]


# =============================================================================
# TOOLS
# =============================================================================


def get_module_info(module_id: str) -> dict:
    module = MODULE_GUIDE.get(module_id)
    if module is None:
        return {"error": f"Unknown module id: {module_id}"}
    return {
        "module_id": module_id,
        "name": module["name"],
        "prerequisites": module["prereq"],
    }


def suggest_next_module(completed_modules: list[str]) -> dict:
    completed = set(completed_modules)
    for module_id in sorted(MODULE_GUIDE.keys()):
        if module_id in completed:
            continue
        prereq = set(MODULE_GUIDE[module_id]["prereq"])
        if prereq.issubset(completed):
            return {
                "next_module_id": module_id,
                "next_module_name": MODULE_GUIDE[module_id]["name"],
            }
    return {"next_module_id": "10", "next_module_name": "Capstone"}


def execute_tool(name: str, args: dict) -> dict:
    if name == "get_module_info":
        return get_module_info(args["module_id"])
    if name == "suggest_next_module":
        return suggest_next_module(args["completed_modules"])
    return {"error": f"Unknown tool: {name}"}


tools = [
    {
        "type": "function",
        "name": "get_module_info",
        "description": "Return curriculum details for a module id (e.g. '05').",
        "parameters": {
            "type": "object",
            "properties": {
                "module_id": {"type": "string"},
            },
            "required": ["module_id"],
            "additionalProperties": False,
        },
    },
    {
        "type": "function",
        "name": "suggest_next_module",
        "description": "Suggest the next module based on completed module ids.",
        "parameters": {
            "type": "object",
            "properties": {
                "completed_modules": {
                    "type": "array",
                    "items": {"type": "string"},
                }
            },
            "required": ["completed_modules"],
            "additionalProperties": False,
        },
    },
]


# =============================================================================
# STRUCTURED OUTPUTS (INTENT ROUTING)
# =============================================================================


class IntentRoute(BaseModel):
    intent: Literal["explain", "planning", "practice"] = Field(
        description="Type of user request"
    )
    search_query: str = Field(description="Best query for retrieval")
    should_use_tools: bool = Field(description="Whether helper tools are useful")


def classify_intent(user_message: str) -> IntentRoute:
    response = client.responses.parse(
        model=MODEL,
        input=f"""Classify this learner request for an AI learning coach.

User message:
{user_message}

Return structured output only.""",
        text_format=IntentRoute,
    )
    return response.output_parsed


# =============================================================================
# CAPSTONE TURN PIPELINE
# =============================================================================


def run_turn(user_message: str, previous_response_id: str | None):
    print("\n" + "=" * 80)
    print(f"USER: {user_message}")
    print("=" * 80)

    # 1) Structured routing
    route = classify_intent(user_message)
    print("\n[1] Intent route:")
    print(route.model_dump_json(indent=2))

    # 2) RAG retrieval
    retrieved_docs = keyword_retrieve(route.search_query, LESSON_DOCS, max_results=3)
    context = "\n\n".join(
        [f"{doc['title']}: {doc['content']}" for doc in retrieved_docs]
    )

    print("\n[2] Retrieved docs:")
    for doc in retrieved_docs:
        print(f"- {doc['title']}")

    # 3) Prompt chain step A: planning
    plan_prompt = f"""Create a concise 3-step response plan for this learner request.

Request:
{user_message}

Retrieved context:
{context}

Return short bullets only."""

    plan_response = client.responses.create(
        model=MODEL,
        input=plan_prompt,
        max_output_tokens=250,
        previous_response_id=previous_response_id,
    )

    plan_text = plan_response.output_text
    print("\n[3] Plan generated:")
    print(plan_text)

    # 4) Prompt chain step B: answer with tool loop
    answer_prompt = f"""Use this plan and context to help the learner.

Plan:
{plan_text}

Request:
{user_message}

Context:
{context}

If useful, call tools to fetch module details or suggest next modules.
Be practical and concise."""

    response = client.responses.create(
        model=MODEL,
        tools=tools,
        input=answer_prompt,
        previous_response_id=plan_response.id,
    )

    while True:
        function_calls = [item for item in response.output if item.type == "function_call"]
        if not function_calls:
            break

        tool_outputs = []
        print("\n[4] Tool calls:")

        for call in function_calls:
            args = json.loads(call.arguments)
            result = execute_tool(call.name, args)
            print(f"- {call.name}({args}) -> {result}")

            tool_outputs.append(
                {
                    "type": "function_call_output",
                    "call_id": call.call_id,
                    "output": json.dumps(result),
                }
            )

        response = client.responses.create(
            model=MODEL,
            tools=tools,
            input=tool_outputs,
            previous_response_id=response.id,
        )

    draft_answer = response.output_text

    # 5) Prompt chain step C + streaming: polish and stream final answer
    polish_prompt = f"""Polish this draft answer.

Requirements:
- Keep it concise
- Use numbered steps when helpful
- End with one concrete next action

Draft:
{draft_answer}"""

    print("\n[5] FINAL (streaming):")
    final_text = ""

    stream = client.responses.create(
        model=MODEL,
        input=polish_prompt,
        previous_response_id=response.id,
        max_output_tokens=500,
        stream=True,
    )

    final_response_id = None
    for event in stream:
        if event.type == "response.output_text.delta":
            print(event.delta, end="", flush=True)
            final_text += event.delta
        elif event.type == "response.completed":
            final_response_id = event.response.id

    print("\n")
    return final_response_id, final_text


# =============================================================================
# DEMO RUN
# =============================================================================

seed_turns = [
    "I'm new. What's the best way to start this curriculum?",
    "Can you quiz me on tool calling in a practical way?",
    "Great. What should I build next week to practice everything?",
]

chain_id = None
for turn in seed_turns:
    chain_id, _ = run_turn(turn, chain_id)

print("=" * 80)
print("Capstone demo complete.")
print("This single flow combined: structured outputs, retrieval, tools, chaining, streaming, and memory.")
print("=" * 80)
