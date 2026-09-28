"""
STRUCTURED OUTPUTS - ANTHROPIC CLAUDE

Goal: get JSON we can validate and trust, not free-form text.
"""

import os
from anthropic import Anthropic
from dotenv import load_dotenv
from pydantic import BaseModel, Field

load_dotenv()
MODEL = os.getenv("ANTHROPIC_MODEL", "claude-sonnet-5-5")
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

prompt = f"""Read this lesson text and return a structured summary.

Lesson text:
{lesson_text}
"""

# The SDK turns our Pydantic model into a JSON schema and validates the reply.
response = client.messages.parse(
    model=MODEL,
    max_tokens=4096,
    messages=[{"role": "user", "content": prompt}],
    output_format=LessonSummary,
)
if response.stop_reason != "end_turn" or response.parsed_output is None:
    raise RuntimeError(f"Structured response did not complete: {response.stop_reason}")

summary = response.parsed_output

print("=" * 80)
print("VALIDATED STRUCTURED OUTPUT")
print("=" * 80)
print(summary.model_dump_json(indent=2))
print("=" * 80)

"""
WHAT YOU JUST LEARNED:

1. You can request schema-constrained JSON output from Claude.
2. messages.parse() returns a validated Pydantic object.
3. Check the stop reason before using the parsed result.
"""
