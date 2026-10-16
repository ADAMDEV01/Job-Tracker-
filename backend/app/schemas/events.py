from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.models import ApplicationEventType, ApplicationStatus


class ApplicationEventRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    application_id: int
    previous_status: ApplicationStatus | None
    new_status: ApplicationStatus | None
    event_type: ApplicationEventType
    created_at: datetime
    note: str | None
