from pathlib import Path

import pytest
from sqlalchemy import select, text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.db.base import Base
from app.db.database import create_database_engine
from app.models import Application, ApplicationEvent, ApplicationStatus, User


def test_database_constraints_and_delete_cascades(tmp_path: Path) -> None:
    database_path = tmp_path / "models.db"
    engine = create_database_engine(f"sqlite:///{database_path}")
    Base.metadata.create_all(engine)

    with Session(engine) as session:
        user = User(email="person@example.com", password_hash="test-hash")
        application = Application(
            company="Example Co",
            role="Engineer",
            platform="Company website",
            user=user,
        )
        application.events.append(
            ApplicationEvent(
                previous_status=None,
                new_status=ApplicationStatus.APPLIED,
                note="Application created",
            )
        )
        session.add(user)
        session.commit()

        duplicate_email = User(
            email="person@example.com",
            password_hash="another-test-hash",
        )
        session.add(duplicate_email)
        with pytest.raises(IntegrityError):
            session.commit()
        session.rollback()

        session.delete(user)
        session.commit()
        assert session.scalars(select(Application)).all() == []
        assert session.scalars(select(ApplicationEvent)).all() == []

    engine.dispose()


def test_application_status_rejects_values_outside_allowed_set(
    tmp_path: Path,
) -> None:
    database_path = tmp_path / "invalid-status.db"
    engine = create_database_engine(f"sqlite:///{database_path}")
    Base.metadata.create_all(engine)

    with Session(engine) as session:
        user = User(email="person@example.com", password_hash="test-hash")
        session.add(user)
        session.flush()
        with pytest.raises(IntegrityError):
            session.execute(
                text(
                    """
                    INSERT INTO applications (user_id, company, role, platform, status)
                    VALUES (:user_id, 'Example Co', 'Engineer', 'Company website', 'not-a-status')
                    """
                ),
                {"user_id": user.id},
            )

    engine.dispose()
