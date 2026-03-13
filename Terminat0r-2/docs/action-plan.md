# action plan

## hours 1–2

| task | who | deliverable |
|------|-----|-------------|
| architecture, mvp, features | both | start-here.md |
| git, branches, api keys | 1 | repo, env.example |

checklist:
- [ ] git repo
- [ ] branches main, develop, feature
- [ ] keys gemini/openai
- [ ] env.example

---

## hours 3–14 backend

| task | who | deliverable |
|------|-----|-------------|
| backend, sqlite | 1 | backend/ |
| prompts, json test | 1 | words-for-ai.md |
| ai api quests | 1 | quest_generator |
| api endpoints | 1 | rest ready |

structure:
```
backend/
├── main.py
├── config.py
├── database/
├── services/
├── api/
└── prompts/
```

checklist:
- [ ] post /api/quest/generate
- [ ] post /api/quest/verify
- [ ] get /api/user/{id}/stats

---

## hours 3–14 mobile app

| task | who | deliverable |
|------|-----|-------------|
| expo init, screens | 2 | app shell |
| camera integration | 2 | capture for verify |
| quest ui, buttons | 2 | create, complete |
| api integration | 2 | full flow |

structure:
```
app/
├── App.tsx
├── app.json
├── screens/
├── components/
├── services/
└── package.json
```

checklist:
- [ ] home screen
- [ ] quest create → api generate
- [ ] camera → photo → api verify
- [ ] stats display

---

## hours 15–20

| task | who | deliverable |
|------|-----|-------------|
| app ↔ api integration | 2 | full flow |
| e2e test | both | bug report |
| debug | both | release candidate |

scenario:
1. open app
2. create quest (clean room)
3. camera photo → verify → reward
4. stats

---

## hours 21–24

| task | who | deliverable |
|------|-----|-------------|
| refactor, readme | 1 | clean repo |
| presentation, demo | 2 | slides |
| pitch rehearsal | both | ready |

---

## parallel work

```
1-2:   [1.1][1.2]
3-6:   [2.1][2.2]  | [3.1]
7-10:  [2.3]       | [3.2]
11-14: [2.4]       | [3.3]
15-20: [4.1][4.2][4.3]
21-24: [5.1][5.2][5.3]
```

---

## critical path

1.2 → 2.1 → 2.2 → 2.3 → 2.4 → 4.1 → 4.2 → 4.3 → 5.1/5.2 → 5.3

---

## plan b

| risk | plan b |
|------|--------|
| api down | mock json |
| camera blocked | text confirm only |
| no time for vision | text only |
