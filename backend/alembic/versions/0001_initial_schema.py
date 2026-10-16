"""Create users, applications, and application events.

Revision ID: 0001_initial_schema
Revises:
Create Date: 2026-10-16
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "0001_initial_schema"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

application_status = sa.Enum(
    "applied",
    "replied",
    "interview",
    "offer",
    "rejected",
    "ghosted",
    name="application_status",
    native_enum=False,
    create_constraint=True,
)
event_previous_status = sa.Enum(
    "applied",
    "replied",
    "interview",
    "offer",
    "rejected",
    "ghosted",
    name="event_previous_status",
    native_enum=False,
    create_constraint=True,
)
event_new_status = sa.Enum(
    "applied",
    "replied",
    "interview",
    "offer",
    "rejected",
    "ghosted",
    name="event_new_status",
    native_enum=False,
    create_constraint=True,
)


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(length=320), nullable=False),
        sa.Column("password_hash", sa.String(length=255), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_users")),
        sa.UniqueConstraint("email", name="uq_users_email"),
    )
    op.create_table(
        "applications",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("company", sa.String(length=200), nullable=False),
        sa.Column("role", sa.String(length=200), nullable=False),
        sa.Column("platform", sa.String(length=100), nullable=False),
        sa.Column("url", sa.String(length=2048), nullable=True),
        sa.Column(
            "status",
            application_status,
            server_default="applied",
            nullable=False,
        ),
        sa.Column(
            "applied_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column(
            "last_update_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
            name=op.f("fk_applications_user_id_users"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_applications")),
    )
    op.create_index(
        "ix_applications_user_applied_at",
        "applications",
        ["user_id", "applied_at"],
    )
    op.create_index(
        "ix_applications_user_status",
        "applications",
        ["user_id", "status"],
    )
    op.create_table(
        "application_events",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("application_id", sa.Integer(), nullable=False),
        sa.Column("previous_status", event_previous_status, nullable=True),
        sa.Column("new_status", event_new_status, nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column("note", sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(
            ["application_id"],
            ["applications.id"],
            name=op.f("fk_application_events_application_id_applications"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_application_events")),
    )
    op.create_index(
        "ix_application_events_application_created_at",
        "application_events",
        ["application_id", "created_at"],
    )


def downgrade() -> None:
    op.drop_index(
        "ix_application_events_application_created_at",
        table_name="application_events",
    )
    op.drop_table("application_events")
    op.drop_index("ix_applications_user_status", table_name="applications")
    op.drop_index("ix_applications_user_applied_at", table_name="applications")
    op.drop_table("applications")
    op.drop_table("users")
