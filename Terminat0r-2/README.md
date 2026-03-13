# lifehack

mobile app: ai analyzes camera in background, shows relevant interesting facts on screen.

## flow

- camera runs (can hide)
- every 45 sec: capture → api/analyze → ai picks fact from data/interesting-facts.txt
- fact appears as overlay on screen

## run

### backend

```bash
python -m venv venv
venv\Scripts\activate
pip install -r backend/requirements.txt
cp env.example .env
uvicorn backend.main:app --reload --port 8000
```

### app

```bash
cd app
npm install
npx expo start
```

set EXPO_PUBLIC_API_URL to your machine ip when testing on device

## data

data/interesting-facts.txt — curated facts by category. add more to expand.
