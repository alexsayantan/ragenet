from pydantic import BaseModel
from datetime import datetime


class UserDetailResponse(BaseModel):
    uuid: str
    username: str
    created_at: datetime


class UserProfileUpdate(BaseModel):
    avatar: str | None = None
    avatar_blurhash: str | None = None
    bio: str | None = None
    timezone: str | None = None


class UserProfileResponse(BaseModel):
    id: str
    avatar: str | None
    avatar_blurhash: str | None
    bio: str | None
    timezone: str | None
