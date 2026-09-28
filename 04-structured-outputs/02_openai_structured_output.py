"""
STRUCTURED OUTPUTS - OPENAI GPT (Responses API)

Goal: parse model output directly into typed Python objects.
"""

import os
from openai import OpenAI
from dotenv import load_dotenv
from pydantic import BaseModel, Field

load_dotenv()
MODEL = os.getenv("OPENAI_MODEL", "gpt-6-luna")
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


class LessonSummary(BaseModel):
    """Schema we want from the model."""

    topic: str = Field(description="Main topic name")
    difficulty: str = Field(description="beginner, intermediate, or advanced")
    prerequisites: list[str] = Field(description="Required prior knowledge")
    key_points: list[str] = Field(description="Top concepts to remember")


lesson_text = """
FastAPI is a modern Python framework for building APIs quickly.
It is known for strong developer experience, automatic documentation,
and good performance. It works well for backend services and AI APIs.
""".strip()

response = client.responses.parse(
    model=MODEL,
    input=f"""Read this lesson text and return a structured summary.

Lesson text:
{lesson_text}
""",
    text_format=LessonSummary,
)
if response.status != "completed" or response.output_parsed is None:
    raise RuntimeError(f"Structured response did not complete: {response.status}")

summary = response.output_parsed

print("=" * 80)
print("VALIDATED STRUCTURED OUTPUT")
print("=" * 80)
print(summary.model_dump_json(indent=2))
print("=" * 80)

"""
WHAT YOU JUST LEARNED:

1. Responses API can parse directly to a pydantic model.
2. Structured outputs reduce brittle string parsing.
3. Typed outputs make downstream code safer and easier to debug.
"""
