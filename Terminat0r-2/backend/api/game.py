import hashlib
import json
import random
from datetime import date
from pathlib import Path

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from backend.database.init_db import get_db
from backend.database.models import User, RoutineCompletion

router = APIRouter()

DATA_DIR = Path(__file__).resolve().parent.parent.parent / "data"

DAILY_BONUS_XP = 25
DAILY_BONUS_GOLD = 15
WEEKLY_BONUS_XP = 50
WEEKLY_BONUS_GOLD = 30
ROUTINES_PER_DAY = 5
ROUTINES_PER_WEEK = 5


def _period_keys():
    today = date.today()
    daily_key = today.isoformat()
    iso = today.isocalendar()
    weekly_key = f"{iso[0]}-W{iso[1]:02d}"
    return daily_key, weekly_key


def _period_seed(period_key: str) -> int:
    return int(hashlib.md5(period_key.encode()).hexdigest()[:8], 16)


def _pick_mixed(items: list, n: int, seed: int) -> list:
    """Обирає n елементів з різних категорій (мікс)."""
    rng = random.Random(seed)
    by_cat: dict[str, list] = {}
    for item in items:
        c = item.get("category", "other")
        by_cat.setdefault(c, []).append(item)
    cat_keys = [c for c in by_cat if by_cat[c]]
    rng.shuffle(cat_keys)
    result = []
    for c in cat_keys:
        if len(result) >= n:
            break
        pool = [i for i in by_cat[c] if i not in result]
        if pool:
            result.append(rng.choice(pool))
    remaining = [i for items in by_cat.values() for i in items if i not in result]
    while len(result) < n and remaining:
        result.append(rng.choice(remaining))
        remaining = [i for i in remaining if i not in result]
    return result[:n]


def _load_json(name: str) -> list:
    path = DATA_DIR / name
    if not path.exists():
        return []
    return json.loads(path.read_text(encoding="utf-8"))


@router.get("/effects")
def get_effects(event_type: str | None = None):
    effects = _load_json("effects.json")
    if event_type:
        effects = [e for e in effects if e.get("event_type") == event_type]
    if not effects:
        return []
    return effects[:5]


@router.get("/effects/random")
def get_random_effect(event_type: str | None = None):
    effects = _load_json("effects.json")
    if event_type:
        effects = [e for e in effects if e.get("event_type") == event_type]
    if not effects:
        return {"emoji": "✨", "label": "Bonus", "event_type": "general"}
    return effects[0]


@router.get("/levels")
def get_levels():
    return _load_json("levels.json")


@router.get("/levels/{level}")
def get_level(level: int):
    levels = _load_json("levels.json")
    for lv in levels:
        if lv.get("level") == level:
            return lv
    return {"level": level, "theme": "unknown", "title": f"Level {level}", "xp_required": level * 100}


@router.get("/events")
def get_events(event_type: str | None = None, limit: int = 50):
    events = _load_json("events.json")
    if event_type:
        events = [e for e in events if e.get("event_type") == event_type]
    return random.sample(events, min(limit, len(events))) if events else []


@router.get("/first-launch")
def get_first_launch():
    path = DATA_DIR / "first-launch-event.json"
    if not path.exists():
        return {"event_type": "first_launch", "title": "Ласкаво просимо", "reward_xp": 50, "reward_gold": 25}
    return json.loads(path.read_text(encoding="utf-8"))


@router.get("/mascot/{level}")
def get_mascot_for_level(level: int):
    mascots = _load_json("level-mascots.json")
    for m in mascots:
        if m.get("level") == level:
            return m
    return {"level": level, "theme": "starter", "image": "mascot-01-starter.png", "costume": "basic"}


@router.get("/coop-tips")
def get_coop_tips():
    """Поради для спільної гри коли два пристрої поруч"""
    path = DATA_DIR / "coop-tips.json"
    if not path.exists():
        return {"tips": [], "event_type": "nearby_coop"}
    data = json.loads(path.read_text(encoding="utf-8"))
    tips = data.get("tips", [])
    return {"tips": tips, "tip": random.choice(tips) if tips else None, "event_type": "nearby_coop"}


@router.get("/routines")
def get_routines(
    device_id: str = Query(""),
    frequency: str | None = None,
    db: Session = Depends(get_db),
):
    """Повертає 5 щоденних + 5 тижневих справ на день, мікс категорій, зі статусом виконання."""
    path = DATA_DIR / "routine-events.json"
    if not path.exists():
        return {"daily": [], "weekly": [], "categories": {}, "daily_completed": [], "weekly_completed": [], "daily_reward_claimed": False, "weekly_reward_claimed": False}
    data = json.loads(path.read_text(encoding="utf-8"))
    daily_pool = data.get("daily", [])
    weekly_pool = data.get("weekly", [])
    categories = data.get("categories", {})
    daily_key, weekly_key = _period_keys()
    seed_daily = _period_seed(daily_key)
    seed_weekly = _period_seed(weekly_key)
    daily = _pick_mixed(daily_pool, ROUTINES_PER_DAY, seed_daily)
    weekly = _pick_mixed(weekly_pool, ROUTINES_PER_WEEK, seed_weekly)
    daily_completed = []
    weekly_completed = []
    daily_reward_claimed = False
    weekly_reward_claimed = False
    if device_id:
        completions = (
            db.query(RoutineCompletion)
            .filter(RoutineCompletion.device_id == device_id)
            .all()
        )
        for c in completions:
            if c.frequency == "daily" and c.period_key == daily_key:
                daily_completed.append(c.routine_id)
                if c.reward_claimed:
                    daily_reward_claimed = True
            elif c.frequency == "weekly" and c.period_key == weekly_key:
                weekly_completed.append(c.routine_id)
                if c.reward_claimed:
                    weekly_reward_claimed = True
    if frequency == "daily":
        return {"daily": daily, "weekly": [], "categories": categories, "daily_completed": daily_completed, "weekly_completed": [], "daily_reward_claimed": daily_reward_claimed, "weekly_reward_claimed": False}
    if frequency == "weekly":
        return {"daily": [], "weekly": weekly, "categories": categories, "daily_completed": [], "weekly_completed": weekly_completed, "daily_reward_claimed": False, "weekly_reward_claimed": weekly_reward_claimed}
    return {
        "daily": daily,
        "weekly": weekly,
        "categories": categories,
        "daily_completed": daily_completed,
        "weekly_completed": weekly_completed,
        "daily_reward_claimed": daily_reward_claimed,
        "weekly_reward_claimed": weekly_reward_claimed,
        "period_daily": daily_key,
        "period_weekly": weekly_key,
    }


def _get_or_create_user(db: Session, device_id: str) -> User:
    user = db.query(User).filter(User.device_id == device_id).first()
    if not user:
        user = User(device_id=device_id)
        db.add(user)
        db.commit()
        db.refresh(user)
    return user


def _level_up(user: User) -> None:
    while user.xp >= user.level * 100:
        user.xp -= user.level * 100
        user.level += 1


@router.post("/routines/complete")
def complete_routine(
    device_id: str = Query(...),
    routine_id: str = Query(...),
    frequency: str = Query(..., regex="^(daily|weekly)$"),
    db: Session = Depends(get_db),
):
    """Позначити справу виконаною, нарахувати XP і Gold."""
    path = DATA_DIR / "routine-events.json"
    if not path.exists():
        return {"ok": False, "error": "routines not found"}
    data = json.loads(path.read_text(encoding="utf-8"))
    pool = data.get("daily", []) if frequency == "daily" else data.get("weekly", [])
    item = next((r for r in pool if r.get("id") == routine_id), None)
    if not item:
        return {"ok": False, "error": "routine not found"}
    daily_key, weekly_key = _period_keys()
    period_key = daily_key if frequency == "daily" else weekly_key
    existing = (
        db.query(RoutineCompletion)
        .filter(
            RoutineCompletion.device_id == device_id,
            RoutineCompletion.routine_id == routine_id,
            RoutineCompletion.frequency == frequency,
            RoutineCompletion.period_key == period_key,
        )
        .first()
    )
    if existing:
        return {"ok": True, "already_completed": True, "xp": 0, "gold": 0}
    user = _get_or_create_user(db, device_id)
    xp = int(item.get("xp", 5))
    gold = int(item.get("gold", 3))
    user.xp += xp
    user.gold += gold
    _level_up(user)
    rec = RoutineCompletion(
        device_id=device_id,
        routine_id=routine_id,
        frequency=frequency,
        period_key=period_key,
        reward_claimed=0,
    )
    db.add(rec)
    db.commit()
    return {"ok": True, "xp": xp, "gold": gold, "total_xp": user.xp, "total_gold": user.gold, "level": user.level}


@router.post("/routines/claim-reward")
def claim_routine_reward(
    device_id: str = Query(...),
    frequency: str = Query(..., regex="^(daily|weekly)$"),
    db: Session = Depends(get_db),
):
    """Отримати бонус за виконання всіх 5 щоденних або тижневих справ."""
    daily_key, weekly_key = _period_keys()
    period_key = daily_key if frequency == "daily" else weekly_key
    completions = (
        db.query(RoutineCompletion)
        .filter(
            RoutineCompletion.device_id == device_id,
            RoutineCompletion.frequency == frequency,
            RoutineCompletion.period_key == period_key,
        )
        .all()
    )
    completed_ids = {c.routine_id for c in completions}
    reward_claimed = any(c.reward_claimed for c in completions)
    path = DATA_DIR / "routine-events.json"
    if path.exists():
        data = json.loads(path.read_text(encoding="utf-8"))
        pool = data.get("daily", []) if frequency == "daily" else data.get("weekly", [])
        expected_ids = {r["id"] for r in _pick_mixed(pool, ROUTINES_PER_DAY if frequency == "daily" else ROUTINES_PER_WEEK, _period_seed(period_key))}
    else:
        expected_ids = set()
    if reward_claimed:
        return {"ok": False, "error": "reward_already_claimed", "xp": 0, "gold": 0}
    if completed_ids != expected_ids or len(completed_ids) < (ROUTINES_PER_DAY if frequency == "daily" else ROUTINES_PER_WEEK):
        return {"ok": False, "error": "not_all_completed", "completed": len(completed_ids), "required": ROUTINES_PER_DAY if frequency == "daily" else ROUTINES_PER_WEEK}
    user = _get_or_create_user(db, device_id)
    xp = DAILY_BONUS_XP if frequency == "daily" else WEEKLY_BONUS_XP
    gold = DAILY_BONUS_GOLD if frequency == "daily" else WEEKLY_BONUS_GOLD
    user.xp += xp
    user.gold += gold
    _level_up(user)
    for c in completions:
        c.reward_claimed = 1
    db.commit()
    return {"ok": True, "xp": xp, "gold": gold, "total_xp": user.xp, "total_gold": user.gold, "level": user.level}
