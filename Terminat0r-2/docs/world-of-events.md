# world of events

## types

1. quest — from routine via ai
2. screen — popup messages
3. recognition — camera + vision
4. life — situation simulation

---

## quest events

| type | example |
|------|---------|
| monster slayer | essay → procrastination |
| treasure hunt | clean desk → crystal of order |
| rescue | drink water → flower |
| boss | exam → dragon |
| side quest | dishes → sacred cup |

```json
{
  "event_type": "quest_generated",
  "quest_id": "uuid",
  "title": "string",
  "monster": "string",
  "backstory": "string",
  "reward_gold": 100,
  "reward_xp": 50,
  "verification_hint": "string"
}
```

---

## screen events

| name | trigger | example |
|------|---------|---------|
| npc hint | 30–60 min | mage whispers about water |
| critical hit | quest > 2 hr | procrastination attacks |
| treasure | after quest | +50 gold |
| nearby quest | no active | traveler offers |
| weather | random | rain, time to read |
| tavern | 45 min work | 5 min break |
| level up | xp reached | new title |
| rare | 1% every 2 hr | dragon offers trade |

---

## recognition events

| name | checks | success | fail |
|------|--------|---------|------|
| room check | room | +100 gold | monster still there |
| water check | glass | +30 gold | drink water |
| exercise check | movement | +50 xp | do exercises |
| desk check | desk | +40 gold | sort papers |
| study check | text | +60 xp | open book |
| meal check | food | +35 gold | eat something |

---

## life events

| name | condition | behavior |
|------|-----------|----------|
| companion | has quests | happy or sad |
| encounter | random | npc offers quest |
| curse/blessing | completion | ±xp, ±gold |
| daily event | once per day | double xp |
| minigame | 3 quests | find treasure |
| epic | 5 in a row | new portal |
| social | has friends | leaderboard |
| timer | 1 hr before | event announcement |

---

## mvp priority

must: qe-01–05, rv-01–02
nice: so-01–03
simplified: le-01, le-04

---

## log format

```json
{
  "id": "uuid",
  "user_id": "discord_id",
  "event_type": "string",
  "event_name": "string",
  "payload": {},
  "created_at": "ISO8601"
}
```
