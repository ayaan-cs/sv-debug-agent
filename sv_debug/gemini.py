"""Live Gemini path. Only used when DEMO_MODE is off and a real key exists."""

from __future__ import annotations

from google import genai
from google.genai import types

from .config import require_api_key
from .helpers import TOOLS


def gemini_debug_systemverilog(user_input: str) -> str:
    """Send debugging input to Gemini and return the diagnosis."""
    client = genai.Client(api_key=require_api_key())

    response = client.models.generate_content(
        model="gemini-flash-latest",
        contents=(
            "A SystemVerilog/FPGA engineer needs help debugging this:\n\n"
            f"{user_input}\n\n"
            "Use your available tools to check for known issues, then give a "
            "clear, concrete explanation of what's likely wrong and how to fix it. "
            "If possible, identify the likely line or section causing the issue. "
            "If nothing looks wrong, say so plainly."
        ),
        config=types.GenerateContentConfig(
            tools=TOOLS,
        ),
    )

    return response.text
