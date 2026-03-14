# Terminat0r-2

Мобільний додаток: AI аналізує камеру в фоні, показує цікаві факти, ефекти, квести та щоденні справи.

## можливості

- **Камера + AI** — кожні 45 сек аналіз сцени → релевантний факт з `data/interesting-facts.txt`
- **Візуальні ефекти** — 500+ ефектів з `data/effects.json`
- **Квести** — генерація з рутини, верифікація фото
- **100 рівнів** — теми та маскоти в костюмах (`data/levels.json`)
- **Щоденні справи** — гігієна, кухня, кімната, здоров'я (`data/routine-events.json`)
- **Івент першого запуску** — маскот рівня, нагороди
- **Режим поруч** — Bluetooth, два єноти, 50 порад для спільної гри (`data/coop-tips.json`)

## запуск

### backend

```powershell
.\run-backend.ps1
```

або вручну:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r backend\requirements.txt
cp env.example .env
# Відредагуй .env: GROQ_API_KEY, AI_PROVIDER=groq (або gemini/openai)
uvicorn backend.main:app --reload --port 8000
```

### app

```powershell
.\run-app.ps1
```

або:

```powershell
cd app
npm install
npx expo start
```

**На пристрої:** встанови `EXPO_PUBLIC_API_URL` на IP твоєї машини (наприклад `http://192.168.1.100:8000`).

## android apk

```powershell
cd app
npm install
npx eas login
npm run build:apk
```

Завантаж APK з посилання → встанови на телефон. Детально: `docs/android-install.md`

## структура

```
├── app/           # Expo React Native
├── backend/       # FastAPI, AI (Groq/Gemini/OpenAI)
├── data/          # факти, ефекти, рівні, івенти, справи
├── docs/          # документація
└── venv/          # Python
```

## дані

| файл | опис |
|------|------|
| `interesting-facts.txt` | факти по категоріях для AI |
| `effects.json` | візуальні ефекти |
| `levels.json` | 100 рівнів з темами |
| `events.json` | івенти для гри |
| `routine-events.json` | щоденні та тижневі справи |
| `level-mascots.json` | костюми маскота |
| `coop-tips.json` | 50 порад для спільної гри (режим поруч) |
| `ai-prompt-two-player-games.md` | AI промт для генерації ігор удвох |
