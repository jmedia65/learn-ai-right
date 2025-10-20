###############################################
# RIA COMPLIANCE DEMO — 3-AGENT WORKFLOW (RAG)
###############################################
# Agent 1: Reads marketing material
# Agent 2: Checks it against SEC compliance rules (RAG)
# Agent 3: Rewrites it with notes on what changed and why
#
# ⚙️ Simple CLI demo — no databases, no web search, no embeddings.
#    Just local RAG context + chat completions.
###############################################

import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# -----------------------------
# RAG Knowledge Base — Compliance Rules
# (Pretend we downloaded and chunked SEC compliance texts)
# -----------------------------
COMPLIANCE_RULES = [
    {
        "title": "SEC Marketing Rule Highlights",
        "content": """Under the SEC's Investment Adviser Marketing Rule (Rule 206(4)-1),
advertisements must be fair and balanced. They cannot:
- Contain untrue statements of material fact
- Omit facts necessary to prevent misleading implications
- Reference specific investment advice results without disclosure
- Use testimonials without clear disclosure
- Make unsubstantiated performance claims
All statements must be factual, balanced, and include proper context.""",
    },
    {
        "title": "Performance & Testimonials",
        "content": """Performance data must include disclosures about time periods, 
fees, and risks. Testimonials or endorsements require disclosure 
of compensation and conflicts of interest. Hypothetical performance 
must be relevant and accompanied by risk warnings.""",
    },
]


# -----------------------------
# Simple Keyword-Based RAG Retriever
# -----------------------------
def simple_rag(query, docs, top_k=2):
    query = query.lower()
    scored = []
    for doc in docs:
        score = sum(word in doc["content"].lower() for word in query.split())
        if score > 0:
            scored.append((score, doc))
    scored.sort(reverse=True, key=lambda x: x[0])
    return [doc["content"] for _, doc in scored[:top_k]]


# -----------------------------
# Agent 1 — Receive Marketing Material
# -----------------------------
def agent_one(marketing_text: str) -> str:
    print("🧠 Agent 1: Received marketing material.\n")
    print(marketing_text, "\n")
    return marketing_text


# -----------------------------
# Agent 2 — Compliance Checker (uses RAG)
# -----------------------------
def agent_two_check_compliance(marketing_text: str) -> str:
    print("⚖️  Agent 2: Checking compliance using RAG...\n")

    # Retrieve relevant rules
    context = "\n\n".join(simple_rag(marketing_text, COMPLIANCE_RULES))

    # Build compliance check prompt
    prompt = f"""You are a compliance officer reviewing marketing content for an RIA firm.
Use the following SEC compliance rules as your reference:

{context}

Marketing text:
{marketing_text}

List any potential compliance risks or rule violations. 
If none found, say 'Compliant'. Be specific."""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        max_tokens=800,
        messages=[{"role": "user", "content": prompt}],
    )

    findings = response.choices[0].message.content
    print(findings, "\n")
    return findings


# -----------------------------
# Agent 3 — Rewrite + Annotate Changes
# -----------------------------
def agent_three_rewrite(marketing_text: str, findings: str) -> str:
    print("✍️  Agent 3: Rewriting with compliance adjustments...\n")

    prompt = f"""You are a compliance editor for an RIA firm.
Below is the original marketing text and the compliance findings.

Original:
{marketing_text}

Compliance Findings:
{findings}

Task:
- Rewrite the text to meet compliance requirements.
- Keep it professional and engaging.
- After the new text, list each change made and the reason why."""

    # Stream this one for fun
    final = ""
    stream = client.chat.completions.create(
        model="gpt-4o-mini",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}],
        stream=True,
    )

    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            text = chunk.choices[0].delta.content
            print(text, end="", flush=True)
            final += text

    print("\n\n✅ Rewrite complete.\n")
    return final


# -----------------------------
# DEMO RUN
# -----------------------------
marketing_example = """Our investment strategy guarantees double-digit returns
every year with minimal risk. Join hundreds of satisfied clients
who have already doubled their money with us!"""

print("🚀 Starting RIA Compliance Demo\n")

material = agent_one(marketing_example)
findings = agent_two_check_compliance(material)
final = agent_three_rewrite(material, findings)

print("=" * 80)
print("FINAL OUTPUT:")
print("=" * 80)
print(final)
