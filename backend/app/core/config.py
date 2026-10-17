import os


DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./job_tracker.db")
JWT_SECRET = os.getenv("JWT_SECRET")
ACCESS_TOKEN_EXPIRE_MINUTES = 30
CORS_ORIGINS = [
    origin.strip()
    for origin in os.getenv(
        "CORS_ORIGINS",
        "https://job-tracker-m6s6.vercel.app,http://localhost:5173",
    ).split(",")
    if origin.strip()
]
