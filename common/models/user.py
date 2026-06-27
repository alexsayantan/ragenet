from datetime import datetime, timezone
from sqlmodel import Field, SQLModel
from uuid import UUID
import os
import time


def uuid7() -> UUID:
    timestamp_ms = int(time.time() * 1000)
    rand = int.from_bytes(os.urandom(10))
    rand_a = (rand >> 62) & 0xFFF
    rand_b = rand & 0x3FFFFFFFFFFFFFFF
    uuid_int = (timestamp_ms & 0xFFFFFFFFFFFF) << 80
    uuid_int |= 0x7 << 76
    uuid_int |= rand_a << 64
    uuid_int |= 0x2 << 62
    uuid_int |= rand_b
    return UUID(int=uuid_int)


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: UUID = Field(default_factory=uuid7, primary_key=True)
    email: str = Field(unique=True, index=True, nullable=False)
    username: str = Field(unique=True, index=True, nullable=False)
    first_name: str | None = Field(default=None)
    last_name: str | None = Field(default=None)
    password: str = Field(nullable=False)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column_kwargs={"onupdate": lambda: datetime.now(timezone.utc)},
    )
    deleted_at: datetime | None = Field(default=None)


class UserDetail(SQLModel, table=True):
    __tablename__ = "user_details"

    id: UUID = Field(default_factory=uuid7, primary_key=True)
    avatar: str | None = Field(default=None)
    avatar_blurhash: str | None = Field(default=None)
    bio: str | None = Field(default=None)
    timezone: str | None = Field(default=None)
