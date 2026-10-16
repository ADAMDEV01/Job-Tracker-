"""Add follow-up dates and event types.

Revision ID: 0002_followups_and_event_types
Revises: 0001_initial_schema
Create Date: 2026-10-16
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "0002_followups_and_event_types"
down_revision: Union[str, None] = "0001_initial_schema"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


event_type = sa.Enum(
    "created",
    "status_changed",
    "updated",
    name="application_event_type",
    native_enum=False,
    create_constraint=True,
)


def upgrade() -> None:
    with op.batch_alter_table("applications") as batch_op:
        batch_op.add_column(
            sa.Column("follow_up_at", sa.DateTime(timezone=True), nullable=True)
        )
    op.create_index(
        "ix_applications_user_follow_up_at",
        "applications",
        ["user_id", "follow_up_at"],
    )

    with op.batch_alter_table("application_events") as batch_op:
        batch_op.add_column(
            sa.Column(
                "event_type",
                event_type,
                server_default="status_changed",
                nullable=False,
            )
        )


def downgrade() -> None:
    with op.batch_alter_table("application_events") as batch_op:
        batch_op.drop_constraint(
            op.f("ck_application_events_application_event_type"),
            type_="check",
        )
        batch_op.drop_column("event_type")
    op.drop_index(
        "ix_applications_user_follow_up_at",
        table_name="applications",
    )
    with op.batch_alter_table("applications") as batch_op:
        batch_op.drop_column("follow_up_at")
