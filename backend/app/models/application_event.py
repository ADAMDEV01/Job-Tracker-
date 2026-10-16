from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING

from sqlalchemy import Enum as SQLAlchemyEnum, ForeignKey, Index, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.db.types import UTCDateTime
from app.models.application import ApplicationStatus, status_enum

if TYPE_CHECKING:
    from app.models.application import Application


class ApplicationEventType(str, Enum):
    CREATED = "created"
    STATUS_CHANGED = "status_changed"
    UPDATED = "updated"


class ApplicationEvent(Base):
    __tablename__ = "application_events"
    __table_args__ = (
        Index(
            "ix_application_events_application_created_at",
            "application_id",
            "created_at",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    application_id: Mapped[int] = mapped_column(
        ForeignKey("applications.id", ondelete="CASCADE"),
        nullable=False,
    )
    previous_status: Mapped[ApplicationStatus | None] = mapped_column(
        status_enum("event_previous_status"),
    )
    new_status: Mapped[ApplicationStatus | None] = mapped_column(
        status_enum("event_new_status"),
    )
    event_type: Mapped[ApplicationEventType] = mapped_column(
        SQLAlchemyEnum(
            ApplicationEventType,
            values_callable=lambda event_types: [
                event_type.value for event_type in event_types
            ],
            native_enum=False,
            create_constraint=True,
            validate_strings=True,
            name="application_event_type",
        ),
        nullable=False,
        default=ApplicationEventType.STATUS_CHANGED,
        server_default=ApplicationEventType.STATUS_CHANGED.value,
    )
    created_at: Mapped[datetime] = mapped_column(
        UTCDateTime(),
        nullable=False,
        server_default=func.now(),
    )
    note: Mapped[str | None] = mapped_column(Text)

    application: Mapped["Application"] = relationship(back_populates="events")
