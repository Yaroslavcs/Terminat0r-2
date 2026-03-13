from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.database.init_db import get_db
from backend.database.models import User

router = APIRouter()


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
