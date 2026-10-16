from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.dependencies.auth import CurrentUser
from app.models import ApplicationEvent
from app.routers.applications import get_owned_application
from app.schemas.events import ApplicationEventRead

router = APIRouter(
    prefix="/applications/{application_id}/events",
    tags=["application history"],
)


@router.get("", response_model=list[ApplicationEventRead])
def list_application_events(
    application_id: int,
    current_user: CurrentUser,
    db: Annotated[Session, Depends(get_db)],
) -> list[ApplicationEvent]:
    application = get_owned_application(application_id, current_user.id, db)
    return list(
        db.scalars(
            select(ApplicationEvent)
            .where(ApplicationEvent.application_id == application.id)
            .order_by(ApplicationEvent.created_at, ApplicationEvent.id)
        ).all()
    )
