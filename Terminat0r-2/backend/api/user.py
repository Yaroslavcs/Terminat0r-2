from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc

from backend.database.init_db import get_db
from backend.database.models import User

router = APIRouter()


def _mask_device_id(device_id: str) -> str:
    if len(device_id) >= 4:
        return f"***{device_id[-4:]}"
    return "****"


@router.get("/leaders/xp")
def leaders_xp(
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    """Топ гравців за XP"""
    users = (
        db.query(User)
        .order_by(desc(User.xp))
        .limit(limit)
        .all()
    )
    return [
        {
            "rank": i + 1,
            "device_id_masked": _mask_device_id(u.device_id),
            "xp": u.xp,
            "level": u.level,
            "gold": u.gold,
        }
        for i, u in enumerate(users)
    ]


@router.get("/{device_id}/stats")
def stats(device_id: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.device_id == device_id).first()
    if not user:
        return {"gold": 0, "xp": 0, "level": 1}

    return {
        "gold": user.gold,
        "xp": user.xp,
        "level": user.level,
    }
