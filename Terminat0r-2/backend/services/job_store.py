import uuid
from threading import Lock
_store: dict[str, dict] = {}
_lock = Lock()


def create_job() -> str:
    with _lock:
        job_id = str(uuid.uuid4())
        _store[job_id] = {"status": "pending", "result": None, "error": None}
        return job_id


def set_result(job_id: str, result: dict):
    with _lock:
        if job_id in _store:
            _store[job_id] = {"status": "completed", "result": result, "error": None}


def set_error(job_id: str, error: str):
    with _lock:
        if job_id in _store:
            _store[job_id] = {"status": "failed", "result": None, "error": error}


def get_job(job_id: str) -> dict | None:
    with _lock:
        return _store.get(job_id)
