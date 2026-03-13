# api keys — шляхи та місця використання

## де зберігати ключі

файл: `.env` (в корені проєкту, створюється з env.example)

приклад: `c:\Terminat0r-2\.env`

---

## змінні оточення

| змінна | призначення | де використовується |
|--------|-------------|---------------------|
| GEMINI_API_KEY | ключ Google Gemini | backend |
| OPENAI_API_KEY | ключ OpenAI | backend |
| EXPO_PUBLIC_API_URL | url бекенду для додатку | app |

---

## backend

### config (завантаження з .env)

шлях: `backend/config.py`

рядки 11–12:
```python
gemini_api_key: str = ""
openai_api_key: str = ""
```

рядки 15–17:
```python
env_file = Path(__file__).resolve().parent.parent / ".env"
```

### quest_generator

шлях: `backend/services/quest_generator.py`

рядок 17: `genai.configure(api_key=settings.gemini_api_key)`
рядок 27: `client = OpenAI(api_key=settings.openai_api_key)`
рядки 47–50: перевірка `settings.ai_provider`, `settings.openai_api_key`, `settings.gemini_api_key`

### vision_verifier

шлях: `backend/services/vision_verifier.py`

рядок 18: `genai.configure(api_key=settings.gemini_api_key)`
рядок 34: `client = OpenAI(api_key=settings.openai_api_key)`
рядки 63–66: перевірка `settings.ai_provider`, `settings.openai_api_key`, `settings.gemini_api_key`

### scene_analyzer

шлях: `backend/services/scene_analyzer.py`

рядок 29: `genai.configure(api_key=settings.gemini_api_key)`
рядок 43: `client = OpenAI(api_key=settings.openai_api_key)`
рядки 75–78: перевірка `settings.ai_provider`, `settings.openai_api_key`, `settings.gemini_api_key`

---

## app (mobile)

### api service

шлях: `app/services/api.ts`

рядок 1: `process.env.EXPO_PUBLIC_API_URL`

для expo: створити `app/.env` або змінну в app.json:
```
EXPO_PUBLIC_API_URL=http://192.168.1.x:8000
```

---

## env.example

шлях: `env.example`

рядки 1–2:
```
GEMINI_API_KEY=
OPENAI_API_KEY=
```

---

## docs

шлях: `docs/get-going.md`

рядки 51–52: згадка змінних в інструкції

---

## повний список шляхів

```
c:\Terminat0r-2\.env
c:\Terminat0r-2\env.example
c:\Terminat0r-2\backend\config.py
c:\Terminat0r-2\backend\services\quest_generator.py
c:\Terminat0r-2\backend\services\vision_verifier.py
c:\Terminat0r-2\backend\services\scene_analyzer.py
c:\Terminat0r-2\app\services\api.ts
c:\Terminat0r-2\docs\get-going.md
```

---

## де отримати ключі

- gemini: https://aistudio.google.com/apikey
- openai: https://platform.openai.com/api-keys
