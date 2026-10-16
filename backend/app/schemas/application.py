from datetime import datetime
from enum import Enum

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    HttpUrl,
    field_validator,
    model_validator,
)

from app.models.application import ApplicationStatus


class ApplicationCreate(BaseModel):
    company: str = Field(min_length=1, max_length=200)
    role: str = Field(min_length=1, max_length=200)
    platform: str = Field(min_length=1, max_length=100)
    url: HttpUrl | None = Field(default=None, max_length=2048)
    follow_up_at: datetime | None = None
    status: ApplicationStatus = ApplicationStatus.APPLIED
    applied_at: datetime | None = None
    notes: str | None = None

    @field_validator("company", "role", "platform")
    @classmethod
    def strip_required_text(cls, value: str) -> str:
        normalized = value.strip()
        if not normalized:
            raise ValueError("This field cannot be blank.")
        return normalized


class ApplicationUpdate(BaseModel):
    company: str | None = Field(default=None, min_length=1, max_length=200)
    role: str | None = Field(default=None, min_length=1, max_length=200)
    platform: str | None = Field(default=None, min_length=1, max_length=100)
    url: HttpUrl | None = Field(default=None, max_length=2048)
    follow_up_at: datetime | None = None
    status: ApplicationStatus | None = None
    applied_at: datetime | None = None
    notes: str | None = None

    @field_validator("company", "role", "platform")
    @classmethod
    def strip_required_text(cls, value: str | None) -> str | None:
        if value is None:
            return None
        normalized = value.strip()
        if not normalized:
            raise ValueError("This field cannot be blank.")
        return normalized

    @model_validator(mode="after")
    def reject_null_for_required_fields(self) -> "ApplicationUpdate":
        if not self.model_fields_set:
            raise ValueError("At least one field must be provided.")
        nullable_fields = {"url", "follow_up_at", "notes"}
        for field_name in self.model_fields_set - nullable_fields:
            if getattr(self, field_name) is None:
                raise ValueError(f"{field_name} cannot be null.")
        return self


class ApplicationRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    company: str
    role: str
    platform: str
    url: str | None
    follow_up_at: datetime | None
    status: ApplicationStatus
    applied_at: datetime
    last_update_at: datetime
    notes: str | None
    created_at: datetime


class ApplicationSort(str, Enum):
    APPLIED_AT = "applied_at"
    COMPANY = "company"
    LAST_UPDATE_AT = "last_update_at"


class SortOrder(str, Enum):
    ASC = "asc"
    DESC = "desc"


class ApplicationPage(BaseModel):
    items: list[ApplicationRead]
    total: int
    page: int
    page_size: int
    pages: int
