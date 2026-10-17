from sqlalchemy.engine import make_url

from app.core.config import normalize_database_url


def test_normalize_postgresql_url_uses_psycopg_driver() -> None:
    normalized = normalize_database_url(
        "postgresql://postgres.example:secret@db.example.com:5432/postgres"
    )

    assert make_url(normalized).drivername == "postgresql+psycopg"


def test_normalize_legacy_postgres_url_uses_psycopg_driver() -> None:
    normalized = normalize_database_url(
        "postgres://postgres:secret@db.example.com:5432/postgres"
    )

    assert make_url(normalized).drivername == "postgresql+psycopg"


def test_normalize_database_url_preserves_other_drivers() -> None:
    normalized = normalize_database_url("sqlite:///./job_tracker.db")

    assert normalized == "sqlite:///./job_tracker.db"
