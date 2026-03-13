# screen events

## idea

popup messages on phone screen
living game world simulation

---

## options

**in-app overlay**
- modal or toast over current screen
- rpg card style
- 5–10 sec display

**notification**
- push when app in background
- quick action to open

**full screen event**
- dedicated event screen
- after quest, level up, etc.

mvp tip: in-app overlay + notification

---

## event source

- schedule (cron)
- triggers (quest > 2 hr)
- after quest done

api: get /api/events/next?user_id=...

---

## look

- rpg card, dark theme
- 300x120 px
- bottom or center
- 5–10 sec
- fade in/out
