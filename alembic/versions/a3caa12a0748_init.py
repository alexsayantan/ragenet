"""init

Revision ID: a3caa12a0748
Revises: 
Create Date: 2026-06-24 20:42:37.346744

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


revision: str = 'a3caa12a0748'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("username", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("hashed_password", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("username"),
    )
    op.create_index(op.f("ix_users_username"), "users", ["username"])


def downgrade() -> None:
    op.drop_index(op.f("ix_users_username"), table_name="users")
    op.drop_table("users")
