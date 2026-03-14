import json
import base64
from pathlib import Path

from backend.config import settings

FACTS_PATH = Path(__file__).resolve().parent.parent.parent / "data" / "interesting-facts.txt"
ROUTINES_PATH = Path(__file__).resolve().parent.parent.parent / "data" / "routine-events.json"

# AI keywords → routine-events category
KEYWORD_TO_ROUTINE_CAT = {
    "desk": "room_workspace", "table": "room_workspace", "laptop": "room_workspace",
    "computer": "room_workspace", "papers": "room_workspace", "monitor": "room_workspace",
    "room": "room_workspace", "indoor": "room_workspace", "floor": "room_workspace",
    "wall": "room_workspace", "furniture": "room_workspace", "bed": "room_workspace",
    "water": "health_selfcontrol", "glass": "health_selfcontrol", "bottle": "health_selfcontrol",
    "cup": "kitchen_household", "drink": "health_selfcontrol",
    "food": "kitchen_household", "plate": "kitchen_household", "meal": "kitchen_household",
    "eating": "kitchen_household", "kitchen": "kitchen_household", "sink": "kitchen_household",
    "book": "room_workspace", "books": "room_workspace", "reading": "room_workspace",
    "plant": "room_workspace", "plants": "room_workspace",
    "person": "health_selfcontrol", "human": "health_selfcontrol",
    "exercise": "health_selfcontrol", "sport": "health_selfcontrol", "running": "health_selfcontrol",
    "phone": "things_care", "mobile": "things_care", "clothes": "things_care",
    "bathroom": "hygiene_health", "teeth": "hygiene_health", "brush": "hygiene_health",
}

# routine category → event_type for effects
CAT_TO_EVENT_TYPE = {
    "hygiene_health": "hygiene", "kitchen_household": "cleaning",
    "room_workspace": "organization", "things_care": "organization",
    "health_selfcontrol": "health",
}


def _load_facts() -> list[tuple[str, str]]:
    facts = []
    if not FACTS_PATH.exists():
        return []
    for line in FACTS_PATH.read_text(encoding="utf-8").strip().split("\n"):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "|" in line:
            cat, fact = line.split("|", 1)
            facts.append((cat.strip(), fact.strip()))
    return facts


def _load_routines() -> dict:
    if not ROUTINES_PATH.exists():
        return {"daily": [], "weekly": [], "categories": {}}
    return json.loads(ROUTINES_PATH.read_text(encoding="utf-8"))


def _get_templates_for_category(category: str, routines: dict, facts: list[tuple[str, str]], max_tasks: int = 5, max_facts: int = 5) -> list[str]:
    """Повертає шаблони (завдання + факти) для категорії — ШІ генерує пораду на їх основі."""
    templates = []
    daily = routines.get("daily", [])
    weekly = routines.get("weekly", [])
    for item in daily + weekly:
        if item.get("category") == category and len(templates) < max_tasks:
            t = item.get("title")
            if t:
                templates.append(t)
    fact_cat_map = {"room_workspace": "room", "kitchen_household": "food", "hygiene_health": "room",
                    "health_selfcontrol": "water", "things_care": "room"}
    fact_cat = fact_cat_map.get(category, "room")
    for cat, fact in facts:
        if cat == fact_cat and len(templates) < max_tasks + max_facts:
            templates.append(fact)
    return templates


def _get_fact_for_category(category: str, facts: list[tuple[str, str]]) -> str | None:
    """Повертає перший факт для категорії (детерміновано, без random)."""
    for cat, fact in facts:
        if cat == category:
            return fact
    return None


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


def _call_groq_analyze(image_b64: str) -> str:
    from openai import OpenAI

    client = OpenAI(api_key=settings.groq_api_key, base_url="https://api.groq.com/openai/v1")
    prompt = """Describe what you see in this image in 3-5 keywords. Focus on: objects, room type, activities, items on surfaces.
Reply with ONLY a comma-separated list of keywords in English. Example: desk, laptop, papers, indoor, office
Keywords:"""
    response = client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        messages=[
            {"role": "user", "content": [
                {"type": "text", "text": prompt},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_b64}"}},
            ]},
        ],
    )
    return response.choices[0].message.content.strip().lower()


def _call_groq_generate_advice(image_b64: str, keywords: list[str], templates: list[str]) -> str:
    from openai import OpenAI

    client = OpenAI(api_key=settings.groq_api_key, base_url="https://api.groq.com/openai/v1")
    tpl = templates[1:10] if len(templates) > 1 else templates[:10]
    templates_text = "\n".join(f"- {t}" for t in tpl) if tpl else "- Наведи порядок у просторі"
    prompt = f"""Подивись на фото. Шаблони для натхнення:
{templates_text}

Напиши ОДИН розгорнутий цікавий факт українською: 2-4 речення одним абзацем. Поєднай пораду (що зробити зараз) з корисним фактом. Без списків, без маркери. Тільки суцільний текст."""
    response = client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        messages=[
            {"role": "user", "content": [
                {"type": "text", "text": prompt},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_b64}"}},
            ]},
        ],
    )
    return response.choices[0].message.content.strip().strip('"')


def _call_openai_generate_advice(image_b64: str, keywords: list[str], templates: list[str]) -> str:
    from openai import OpenAI

    client = OpenAI(api_key=settings.openai_api_key)
    templates_text = "\n".join(f"- {t}" for t in templates[:10]) if templates else "- Зробіть невеликий крок для порядку."
    prompt = f"""Подивись на фото. Шаблони для натхнення:
{templates_text}

Напиши ОДИН цікавий факт українською: 2-4 речення одним абзацем. Порада + корисний факт. Без списків. Тільки суцільний текст."""
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "user", "content": [
                {"type": "text", "text": prompt},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_b64}"}},
            ]},
        ],
    )
    return response.choices[0].message.content.strip().strip('"')


def _call_gemini_generate_advice(image_b64: str, keywords: list[str], templates: list[str]) -> str:
    import google.generativeai as genai

    genai.configure(api_key=settings.gemini_api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")
    templates_text = "\n".join(f"- {t}" for t in templates[:10]) if templates else "- Зробіть невеликий крок для порядку."
    prompt = f"""Подивись на фото. Шаблони для натхнення:
{templates_text}

Напиши ОДИН цікавий факт українською: 2-4 речення одним абзацем. Порада + корисний факт. Без списків. Тільки суцільний текст."""
    image_data = base64.b64decode(image_b64)
    image_part = {"mime_type": "image/jpeg", "data": image_data}
    response = model.generate_content([prompt, image_part])
    return response.text.strip().strip('"')


def analyze_and_pick_fact(image_b64: str) -> dict:
    """Аналіз фото через AI. ШІ генерує пораду на основі шаблонів (routine-events + facts)."""
    if not image_b64:
        raise ValueError("image_b64 is required")

    facts = _load_facts()
    routines = _load_routines()

    if settings.ai_provider == "groq" and settings.groq_api_key:
        keywords = _call_groq_analyze(image_b64)
    elif settings.ai_provider == "openai" and settings.openai_api_key:
        keywords = _call_openai_analyze(image_b64)
    elif settings.gemini_api_key:
        keywords = _call_gemini_analyze(image_b64)
    else:
        raise ValueError("No AI provider configured. Set GROQ_API_KEY, OPENAI_API_KEY or GEMINI_API_KEY in .env")

    kw_list = [w.strip() for w in keywords.replace(",", " ").split() if w.strip()]

    category = None
    for w in kw_list:
        if w in KEYWORD_TO_ROUTINE_CAT:
            category = KEYWORD_TO_ROUTINE_CAT[w]
            break

    if not category:
        category = "room_workspace"

    templates = _get_templates_for_category(category, routines, facts)

    if settings.ai_provider == "groq" and settings.groq_api_key:
        advice = _call_groq_generate_advice(image_b64, kw_list, templates)
    elif settings.ai_provider == "openai" and settings.openai_api_key:
        advice = _call_openai_generate_advice(image_b64, kw_list, templates)
    elif settings.gemini_api_key:
        advice = _call_gemini_generate_advice(image_b64, kw_list, templates)
    else:
        advice = templates[0] if templates else "Зробіть невеликий крок для порядку."

    if not advice or not advice.strip():
        advice = templates[0] if templates else "Зробіть невеликий крок для порядку."

    event_type = CAT_TO_EVENT_TYPE.get(category, "fact_show")

    return {
        "fact": advice,
        "help": advice,
        "display_type": "fact",
        "category": category,
        "keywords": kw_list,
        "event_type": event_type,
    }
