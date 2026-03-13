from fastapi import APIRouter, BackgroundTasks
from pydantic import BaseModel

from backend.services.job_store import create_job, set_result, set_error
from backend.services.scene_analyzer import analyze_and_pick_fact

router = APIRouter()


class AnalyzeRequest(BaseModel):
    image_b64: str


def _run_analyze(job_id: str, image_b64: str):
    try:
        result = analyze_and_pick_fact(image_b64)
        set_result(job_id, result)
    except Exception as e:
        set_error(job_id, str(e))


@router.post("")
def analyze(req: AnalyzeRequest, background_tasks: BackgroundTasks):
    job_id = create_job()
    background_tasks.add_task(_run_analyze, job_id, req.image_b64)
    return {"job_id": job_id, "status": "processing"}
