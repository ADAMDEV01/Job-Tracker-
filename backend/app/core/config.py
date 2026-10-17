import os


DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./job_tracker.db")
JWT_SECRET = os.getenv("JWT_SECRET")
ACCESS_TOKEN_EXPIRE_MINUTES = 30
