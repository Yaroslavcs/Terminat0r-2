import json
import re
from pathlib import Path

from backend.config import settings

QUEST_PROMPT_PATH = Path(__file__).resolve().parent.parent / "prompts" / "quest.txt"


def _load_prompt() -> str:
    return QUEST_PROMPT_PATH.read_text(encoding="utf-8")


def _call_gemini(user_input: str) -> str:
    import google.generativeai as genai

    genai.configure(api_key=settings.gemini_api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")
    prompt = _load_prompt().replace("{user_input}", user_input)
    response = model.generate_content(prompt)
    return response.text.strip()


def _call_openai(user_input: str) -> str:
    from openai import OpenAI

    client = OpenAI(api_key=settings.openai_api_key)
    prompt = _load_prompt().replace("{user_input}", user_input)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content.strip()


def _parse_json(text: str) -> dict:
    text = text.strip()
    text = re.sub(r"^```(?:json)?\s*", "", text)
    text = re.sub(r"\s*```$", "", text)
    return json.loads(text)


def generate_quest(user_input: str) -> dict:
    if not user_input or len(user_input.strip()) < 2:
        raise ValueError("task too short")

    if settings.ai_provider == "openai" and settings.openai_api_key:
        raw = _call_openai(user_input)
    else:
        if not settings.gemini_api_key:
            return _mock_quest(user_input)
        raw = _call_gemini(user_input)

    data = _parse_json(raw)
    required = ["title", "monster", "backstory", "reward_gold", "reward_xp", "verification_hint"]
    for k in required:
        if k not in data:
            raise ValueError(f"missing field: {k}")
    return data


def _mock_quest(user_input: str) -> dict:
    return {
        "title": f"Complete: {user_input[:40]}",
        "monster": "The Routine Demon",
        "backstory": "Another day, another task. Time to conquer it!",
        "reward_gold": 50,
        "reward_xp": 25,
        "verification_hint": "Photo or confirmation when done",
    }
