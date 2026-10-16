from pydantic import BaseModel

from app.models import ApplicationStatus
from app.schemas.application import ApplicationRead


class StatusCount(BaseModel):
    status: ApplicationStatus
    count: int


class FollowUpItem(BaseModel):
    application: ApplicationRead
    days_since_applied: int


class ResponseMetrics(BaseModel):
    total_applications: int
    responded_applications: int
    response_rate: float
    average_time_to_first_response_days: float | None


class PlatformMetrics(ResponseMetrics):
    platform: str


class DashboardSummary(ResponseMetrics):
    by_status: list[StatusCount]
    upcoming_followups: list[FollowUpItem]
    may_be_ghosted: list[FollowUpItem]
