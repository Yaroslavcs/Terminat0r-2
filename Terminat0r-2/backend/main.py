from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.database.init_db import init_db, get_db
from backend.api import quest, user, job, analyze, game, shop


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(title="Terminat0r-2", lifespan=lifespan)

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
app.include_router(game.router, prefix="/api/game", tags=["game"])
app.include_router(shop.router, prefix="/api/shop", tags=["shop"])


@app.get("/")
def root():
    return {"app": "terminat0r2", "status": "ok"}
