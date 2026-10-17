from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers.applications import router as applications_router
from app.routers.auth import router as auth_router
from app.routers.events import router as events_router
from app.routers.stats import router as stats_router

app = FastAPI(
    title="Job Tracker API",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(applications_router)
app.include_router(events_router)
app.include_router(stats_router)


@app.get("/health", tags=["health"])
def health_check() -> dict[str, str]:
    return {"status": "ok"}
