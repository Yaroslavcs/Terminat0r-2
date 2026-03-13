from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.database.init_db import init_db, get_db
from backend.api import quest, user, job, analyze


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(title="lifehack", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(quest.router, prefix="/api/quest", tags=["quest"])
app.include_router(user.router, prefix="/api/user", tags=["user"])
app.include_router(job.router, prefix="/api/job", tags=["job"])
app.include_router(analyze.router, prefix="/api/analyze", tags=["analyze"])


@app.get("/")
def root():
    return {"app": "lifehack", "status": "ok"}
