import json
import re
import base64
from pathlib import Path

from backend.config import settings

VERIFY_PROMPT_PATH = Path(__file__).resolve().parent.parent / "prompts" / "verify.txt"


def _load_prompt() -> str:
    return VERIFY_PROMPT_PATH.read_text(encoding="utf-8")


def _call_gemini_vision(task: str, hint: str, image_b64: str) -> str:
    import google.generativeai as genai

    genai.configure(api_key=settings.gemini_api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")
    prompt = (
        _load_prompt()
        .replace("{task_description}", task)
        .replace("{verification_hint}", hint)
    )
    image_data = base64.b64decode(image_b64)
    image_part = {"mime_type": "image/jpeg", "data": image_data}
    response = model.generate_content([prompt, image_part])
    return response.text.strip()


def _call_openai_vision(task: str, hint: str, image_b64: str) -> str:
    from openai import OpenAI

    client = OpenAI(api_key=settings.openai_api_key)
    prompt = (
        _load_prompt()
        .replace("{task_description}", task)
        .replace("{verification_hint}", hint)
    )
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "user", "content": [
                {"type": "text", "text": prompt},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_b64}"}},
            ]},
        ],
    )
    return response.choices[0].message.content.strip()


def _parse_json(text: str) -> dict:
    text = text.strip()
    text = re.sub(r"^```(?:json)?\s*", "", text)
    text = re.sub(r"\s*```$", "", text)
    return json.loads(text)


def verify_photo(task_description: str, verification_hint: str, image_b64: str) -> dict:
    if not image_b64:
        return {"verified": True, "confidence": 0.5, "message": "No photo — trust mode", "reward_multiplier": 0.8}

    if settings.ai_provider == "openai" and settings.openai_api_key:
        raw = _call_openai_vision(task_description, verification_hint, image_b64)
    else:
        if not settings.gemini_api_key:
            return {"verified": True, "confidence": 0.7, "message": "Photo received (mock)", "reward_multiplier": 1.0}
        raw = _call_gemini_vision(task_description, verification_hint, image_b64)

    data = _parse_json(raw)
    return {
        "verified": bool(data.get("verified", False)),
        "confidence": float(data.get("confidence", 0.5)),
        "message": str(data.get("message", "")),
        "reward_multiplier": float(data.get("reward_multiplier", 0.5 if not data.get("verified") else 1.0)),
    }
