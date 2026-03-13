from fastapi import APIRouter, HTTPException

from backend.services.job_store import get_job

router = APIRouter()


@router.get("/{job_id}")
def job_status(job_id: str):
    job = get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="job not found")
    return job
