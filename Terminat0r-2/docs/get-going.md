# get going

## need

- python 3.10+
- node 18+
- git
- gemini or openai key

---

## clone

```bash
git clone <repo_url>
cd Terminat0r-2
```

---

## backend

```powershell
.\run-backend.ps1
```

або вручну:
```powershell
py -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r backend\requirements.txt
python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000
```

---

## mobile app

```bash
cd app
npm install
npx expo start
```

scan qr with Expo Go on phone

---

## setup

copy env.example to .env in project root

```env
GEMINI_API_KEY=
OPENAI_API_KEY=
API_BASE_URL=http://localhost:8000
```

for mobile: set API_BASE_URL to your machine ip (e.g. http://192.168.1.x:8000) when testing on device

---

## keys

- gemini: aistudio.google.com/apikey
- openai: platform.openai.com/api-keys
