import json
import re
import base64
import random
from pathlib import Path

from backend.config import settings

FACTS_PATH = Path(__file__).resolve().parent.parent.parent / "data" / "interesting-facts.txt"


def _load_facts() -> list[tuple[str, str]]:
    facts = []
    if not FACTS_PATH.exists():
        return [("general", "Кожен момент — можливість зробити крок вперед.")]
    for line in FACTS_PATH.read_text(encoding="utf-8").strip().split("\n"):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "|" in line:
            cat, fact = line.split("|", 1)
            facts.append((cat.strip(), fact.strip()))
    return facts


def _call_gemini_analyze(image_b64: str) -> str:
    import google.generativeai as genai

    genai.configure(api_key=settings.gemini_api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")
    prompt = """Describe what you see in this image in 3-5 keywords. Focus on: objects, room type, activities, items on surfaces.
Reply with ONLY a comma-separated list of keywords in English. Example: desk, laptop, papers, indoor, office
Keywords:"""
    image_data = base64.b64decode(image_b64)
    image_part = {"mime_type": "image/jpeg", "data": image_data}
    response = model.generate_content([prompt, image_part])
    return response.text.strip().lower()


def _call_openai_analyze(image_b64: str) -> str:
    from openai import OpenAI

    client = OpenAI(api_key=settings.openai_api_key)
    prompt = """Describe what you see in this image in 3-5 keywords. Focus on: objects, room type, activities, items on surfaces.
Reply with ONLY a comma-separated list of keywords in English. Example: desk, laptop, papers, indoor, office
Keywords:"""
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "user", "content": [
                {"type": "text", "text": prompt},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_b64}"}},
            ]},
        ],
    )
    return response.choices[0].message.content.strip().lower()


def _match_category(keywords: str, facts: list[tuple[str, str]]) -> list[str]:
    kw = set(w.strip() for w in keywords.replace(",", " ").split())
    matches = []
    for cat, fact in facts:
        cat_words = set(cat.lower().split())
        if kw & cat_words or any(w in cat for w in kw):
            matches.append(fact)
    return matches


def analyze_and_pick_fact(image_b64: str) -> dict:
    facts = _load_facts()
    if not image_b64:
        fact = random.choice([f for _, f in facts])
        return {"fact": fact, "category": "general", "keywords": []}

    if settings.ai_provider == "openai" and settings.openai_api_key:
        keywords = _call_openai_analyze(image_b64)
    else:
        if not settings.gemini_api_key:
            fact = random.choice([f for _, f in facts])
            return {"fact": fact, "category": "general", "keywords": ["mock"]}
        keywords = _call_gemini_analyze(image_b64)

    kw_list = [w.strip() for w in keywords.replace(",", " ").split() if w.strip()]
    matches = _match_category(keywords, facts)

    keyword_to_cat = {
        "desk": "desk", "table": "desk", "laptop": "desk", "computer": "desk", "papers": "desk",
        "room": "room", "indoor": "room", "floor": "room", "wall": "room", "furniture": "room",
        "book": "book", "books": "book", "reading": "book", "paper": "book",
        "water": "water", "glass": "water", "bottle": "water", "cup": "water", "drink": "water",
        "food": "food", "plate": "food", "meal": "food", "eating": "food",
        "phone": "phone", "mobile": "phone", "smartphone": "phone",
        "plant": "nature", "tree": "nature", "outdoor": "nature", "green": "nature",
        "person": "person", "human": "person", "sitting": "person", "standing": "person",
        "exercise": "exercise", "sport": "exercise", "running": "exercise",
        "bed": "sleep", "sleeping": "sleep", "dark": "sleep",
        "light": "light", "window": "light", "sun": "light",
        "object": "object", "items": "object", "things": "object",
        "monitor": "screen", "display": "screen", "tv": "screen",
    }

    for w in kw_list:
        if w in keyword_to_cat:
            cat = keyword_to_cat[w]
            cat_facts = [f for c, f in facts if c == cat]
            if cat_facts:
                return {"fact": random.choice(cat_facts), "category": cat, "keywords": kw_list}

    if matches:
        return {"fact": random.choice(matches), "category": "matched", "keywords": kw_list}

    fact = random.choice([f for _, f in facts])
    return {"fact": fact, "category": "general", "keywords": kw_list}
