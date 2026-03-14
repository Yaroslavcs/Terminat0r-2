import json
import random
from pathlib import Path

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from backend.database.init_db import get_db
from backend.database.models import User, UserSkin

router = APIRouter()
DATA_DIR = Path(__file__).resolve().parent.parent.parent / "data"


def _load_skins():
    path = DATA_DIR / "skins.json"
    if not path.exists():
        return {"skins": [], "wheel_skins": [2, 3, 4, 5, 6, 7]}
    return json.loads(path.read_text(encoding="utf-8"))


def _get_or_create_user(db: Session, device_id: str) -> User:
    user = db.query(User).filter(User.device_id == device_id).first()
    if not user:
        user = User(device_id=device_id)
        db.add(user)
        db.commit()
        db.refresh(user)
    return user


@router.get("/skins")
def get_shop_skins():
    """Список скінів для магазину."""
    data = _load_skins()
    return {"skins": data.get("skins", []), "wheel_skins": data.get("wheel_skins", [2, 3, 4, 5, 6, 7])}


@router.get("/wheel-skins")
def get_wheel_skins():
    """6 випадкових скінів на колесі фортуни."""
    data = _load_skins()
    wheel_ids = data.get("wheel_skins", list(range(2, 21)))
    skins = {s["id"]: s for s in data.get("skins", [])}
    chosen = random.sample(wheel_ids, min(6, len(wheel_ids)))
    return [{"id": i, "theme": skins.get(i, {}).get("theme", ""), "title": skins.get(i, {}).get("title", f"Skin {i}")} for i in chosen]


@router.post("/wheel/spin")
def wheel_spin(
    device_id: str = Query(...),
    skin_ids: str | None = Query(None, description="Comma-separated IDs of 6 skins on wheel"),
    db: Session = Depends(get_db),
):
    """Крутити колесо. Якщо skin_ids задано — виграш з цих 6, інакше з усіх."""
    data = _load_skins()
    if skin_ids:
        ids = [int(x.strip()) for x in skin_ids.split(",") if x.strip()]
        pool = ids if len(ids) >= 6 else ids * (6 // len(ids) + 1)
        skin_id = random.choice(pool[:6])
    else:
        wheel_ids = data.get("wheel_skins", list(range(2, 21)))
        skin_id = random.choice(wheel_ids)
    user = _get_or_create_user(db, device_id)
    existing = db.query(UserSkin).filter(UserSkin.device_id == device_id, UserSkin.skin_id == skin_id).first()
    if not existing:
        us = UserSkin(device_id=device_id, skin_id=skin_id, source="wheel")
        db.add(us)
        db.commit()
    skins = {s["id"]: s for s in data.get("skins", [])}
    s = skins.get(skin_id, {})
    return {"skin_id": skin_id, "theme": s.get("theme", ""), "title": s.get("title", f"Skin {skin_id}"), "new": not existing}


@router.post("/purchase")
def purchase_skin(
    device_id: str = Query(...),
    skin_id: int = Query(...),
    db: Session = Depends(get_db),
):
    """Купити скін за золото."""
    data = _load_skins()
    skins = {s["id"]: s for s in data.get("skins", [])}
    skin = skins.get(skin_id)
    if not skin or skin.get("starter") or skin.get("price", 0) <= 0:
        return {"ok": False, "error": "invalid_skin"}
    user = db.query(User).filter(User.device_id == device_id).first()
    if not user:
        return {"ok": False, "error": "user_not_found"}
    if user.gold < skin["price"]:
        return {"ok": False, "error": "not_enough_gold", "required": skin["price"]}
    existing = db.query(UserSkin).filter(UserSkin.device_id == device_id, UserSkin.skin_id == skin_id).first()
    if existing:
        return {"ok": False, "error": "already_owned"}
    user.gold -= skin["price"]
    us = UserSkin(device_id=device_id, skin_id=skin_id, source="purchase")
    db.add(us)
    db.commit()
    return {"ok": True, "skin_id": skin_id, "gold_left": user.gold}


@router.post("/purchase-transfer")
def purchase_skin_by_transfer(
    device_id: str = Query(...),
    skin_id: int = Query(...),
    db: Session = Depends(get_db),
):
    """Купівля скіна після переказу на карту. source=support."""
    data = _load_skins()
    skins = {s["id"]: s for s in data.get("skins", [])}
    skin = skins.get(skin_id)
    if not skin or skin.get("starter") or skin_id == 1:
        return {"ok": False, "error": "invalid_skin"}
    user = _get_or_create_user(db, device_id)
    existing = db.query(UserSkin).filter(UserSkin.device_id == device_id, UserSkin.skin_id == skin_id).first()
    if existing:
        return {"ok": False, "error": "already_owned"}
    us = UserSkin(device_id=device_id, skin_id=skin_id, source="support")
    db.add(us)
    db.commit()
    return {"ok": True, "skin_id": skin_id}


@router.get("/owned")
def get_owned_skins(device_id: str = Query(...), db: Session = Depends(get_db)):
    """Скіни, що належать користувачу."""
    data = _load_skins()
    skins_map = {s["id"]: s for s in data.get("skins", [])}
    owned = db.query(UserSkin).filter(UserSkin.device_id == device_id).all()
    result = []
    seen = set()
    for us in owned:
        if us.skin_id in seen:
            continue
        seen.add(us.skin_id)
        s = skins_map.get(us.skin_id, {})
        result.append({
            "skin_id": us.skin_id,
            "theme": s.get("theme", ""),
            "title": s.get("title", f"Skin {us.skin_id}"),
            "source": us.source,
        })
    starter_id = 1
    if starter_id not in seen:
        s = skins_map.get(starter_id, {})
        result.insert(0, {"skin_id": starter_id, "theme": s.get("theme", "starter"), "title": s.get("title", "Starter"), "source": "starter"})
    return {"skins": sorted(result, key=lambda x: x["skin_id"])}
