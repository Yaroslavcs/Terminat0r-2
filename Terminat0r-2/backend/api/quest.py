import json
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from pydantic import BaseModel

from backend.database.init_db import get_db, SessionLocal
from backend.database.models import User, Quest
from backend.services.quest_generator import generate_quest
from backend.services.vision_verifier import verify_photo
from backend.services.job_store import create_job, set_result, set_error

router = APIRouter()


class GenerateRequest(BaseModel):
    task: str
    device_id: str


class VerifyRequest(BaseModel):
    quest_id: int
    device_id: str
    image_b64: str | None = None


def _get_or_create_user(db: Session, device_id: str) -> User:
    user = db.query(User).filter(User.device_id == device_id).first()
    if not user:
        user = User(device_id=device_id)
        db.add(user)
        db.commit()
        db.refresh(user)
    return user


@router.get("/{quest_id}")
def get_quest(quest_id: int, device_id: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.device_id == device_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="user not found")
    quest = db.query(Quest).filter(Quest.id == quest_id, Quest.user_id == user.id).first()
    if not quest:
        raise HTTPException(status_code=404, detail="quest not found")
    data = json.loads(quest.generated_json)
    return {
        "quest_id": quest.id,
        "title": data["title"],
        "monster": data["monster"],
        "backstory": data["backstory"],
        "reward_gold": data["reward_gold"],
        "reward_xp": data["reward_xp"],
        "verification_hint": data["verification_hint"],
        "status": quest.status,
    }


@router.post("/generate")
def generate(req: GenerateRequest, db: Session = Depends(get_db)):
    user = _get_or_create_user(db, req.device_id)
    try:
        data = generate_quest(req.task)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    quest = Quest(
        user_id=user.id,
        prompt=req.task,
        generated_json=json.dumps(data),
        status="pending",
    )
    db.add(quest)
    db.commit()
    db.refresh(quest)

    return {
        "quest_id": quest.id,
        "title": data["title"],
        "monster": data["monster"],
        "backstory": data["backstory"],
        "reward_gold": data["reward_gold"],
        "reward_xp": data["reward_xp"],
        "verification_hint": data["verification_hint"],
    }


def _run_verify(job_id: str, quest_id: int, device_id: str, image_b64: str | None):
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.device_id == device_id).first()
        if not user:
            set_error(job_id, "user not found")
            return
        quest = db.query(Quest).filter(Quest.id == quest_id, Quest.user_id == user.id).first()
        if not quest:
            set_error(job_id, "quest not found")
            return
        if quest.status != "pending":
            set_error(job_id, "quest already completed")
            return

        data = json.loads(quest.generated_json)
        result = verify_photo(quest.prompt, data.get("verification_hint", ""), image_b64 or "")

        gold = int(data.get("reward_gold", 50) * result["reward_multiplier"])
        xp = int(data.get("reward_xp", 25) * result["reward_multiplier"])

        user.gold += gold
        user.xp += xp
        while user.xp >= user.level * 100:
            user.xp -= user.level * 100
            user.level += 1

        quest.status = "completed"
        db.commit()

        set_result(job_id, {
            "verified": result["verified"],
            "message": result["message"],
            "gold_earned": gold,
            "xp_earned": xp,
            "total_gold": user.gold,
            "total_xp": user.xp,
            "level": user.level,
        })
    except Exception as e:
        set_error(job_id, str(e))
    finally:
        db.close()


@router.post("/verify")
def verify(req: VerifyRequest, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.device_id == req.device_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="user not found")

    quest = db.query(Quest).filter(Quest.id == req.quest_id, Quest.user_id == user.id).first()
    if not quest:
        raise HTTPException(status_code=404, detail="quest not found")
    if quest.status != "pending":
        raise HTTPException(status_code=400, detail="quest already completed")

    if req.image_b64:
        job_id = create_job()
        background_tasks.add_task(
            _run_verify,
            job_id,
            req.quest_id,
            req.device_id,
            req.image_b64,
        )
        return {"job_id": job_id, "status": "processing"}
    else:
        data = json.loads(quest.generated_json)
        result = verify_photo(quest.prompt, data.get("verification_hint", ""), "")
        gold = int(data.get("reward_gold", 50) * result["reward_multiplier"])
        xp = int(data.get("reward_xp", 25) * result["reward_multiplier"])
        user.gold += gold
        user.xp += xp
        while user.xp >= user.level * 100:
            user.xp -= user.level * 100
            user.level += 1
        quest.status = "completed"
        db.commit()
        return {
            "verified": result["verified"],
            "message": result["message"],
            "gold_earned": gold,
            "xp_earned": xp,
            "total_gold": user.gold,
            "total_xp": user.xp,
            "level": user.level,
        }
