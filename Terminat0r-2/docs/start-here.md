# lifehack — idea and goals

## what it is

reality-integrated mobile app:
- camera runs in background, ai analyzes scene
- ai picks relevant interesting fact from curated database
- facts appear on screen as overlay
- quests and verification as secondary features

---

## stack

| part | tech |
|------|------|
| backend | python (fastapi) |
| db | sqlite |
| ai | gemini / openai |
| client | mobile app (expo) |
| camera | device camera, periodic capture |
| facts | data/interesting-facts.txt |

---

## flow

```
camera (background) → capture → api/analyze → ai vision
                                    ↓
                         data/interesting-facts.txt
                                    ↓
                         fact on screen (overlay)
```

---

## main features

**primary**
- background camera analysis
- ai matches scene to fact category
- overlay with interesting facts on screen

**secondary**
- quest generation from routine
- photo verification for quests
- stats (gold, xp, level)

---

## data

data/interesting-facts.txt — large curated list
format: category|fact
categories: room, desk, book, water, food, phone, nature, exercise, sleep, light, person, object, screen
