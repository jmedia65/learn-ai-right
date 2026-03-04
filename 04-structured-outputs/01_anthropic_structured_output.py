"""
STRUCTURED OUTPUTS - ANTHROPIC CLAUDE

Goal: get JSON we can validate and trust, not free-form text.
"""

import json
import os
from anthropic import Anthropic
from dotenv import load_dotenv
from pydantic import BaseModel, Field, ValidationError

load_dotenv()
MODEL = os.getenv("ANTHROPIC_MODEL", "claude-sonnet-4-6")
client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))


class LessonSummary(BaseModel):
    """Schema we want the AI to follow."""

    topic: str = Field(description="Main topic name")
    difficulty: str = Field(description="beginner, intermediate, or advanced")
    prerequisites: list[str] = Field(description="Required prior knowledge")
    key_points: list[str] = Field(description="Top concepts to remember")


lesson_text = """
FastAPI is a modern Python framework for building APIs quickly.
It is known for strong developer experience, automatic documentation,
and good performance. It works well for backend services and AI APIs.
""".strip()

prompt = f"""Read this lesson text and return ONLY valid JSON with this exact shape:

{{
  "topic": "string",
  "difficulty": "beginner|intermediate|advanced",
  "prerequisites": ["string", "string"],
  "key_points": ["string", "string", "string"]
}}

Lesson text:
{lesson_text}
"""

response = client.messages.create(
    model=MODEL,
    max_tokens=500,
    messages=[{"role": "user", "content": prompt}],
)

raw_output = response.content[0].text

print("=" * 80)
print("RAW MODEL OUTPUT")
print("=" * 80)
print(raw_output)
print()

# Claude may wrap JSON in markdown code fences (```json ... ```).
# Strip those fences so json.loads() gets clean JSON text.
clean_output = raw_output.strip()
if clean_output.startswith("```"):
    lines = clean_output.splitlines()
    if lines:
        lines = lines[1:]  # remove opening fence line (```json or ```)
    if lines and lines[-1].strip().startswith("```"):
        lines = lines[:-1]  # remove closing fence line
    clean_output = "\n".join(lines).strip()

# Parse JSON from model output
try:
    parsed_json = json.loads(clean_output)
except json.JSONDecodeError as e:
    print("JSON parsing failed:", e)
    raise

# Validate against schema
try:
    summary = LessonSummary.model_validate(parsed_json)
except ValidationError as e:
    print("Schema validation failed:")
    print(e)
    raise

print("=" * 80)
print("VALIDATED STRUCTURED OUTPUT")
print("=" * 80)
print(summary.model_dump_json(indent=2))
print("=" * 80)

"""
WHAT YOU JUST LEARNED:

1. You can request strict JSON output from Claude.
2. Always validate model output before using it in app logic.
3. pydantic makes schema mismatches visible immediately.
"""
