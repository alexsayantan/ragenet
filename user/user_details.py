from user.schemas import UserDetailResponse, UserProfileResponse, UserProfileUpdate
from common.models.user import User, UserDetail
from common.security import get_current_user
from common.database import get_session
from fastapi import Depends, FastAPI
from sqlmodel import Session, select
from mangum import Mangum

app = FastAPI()


@app.get("/user-details", response_model=UserDetailResponse)
async def get_user_details(current_user: User = Depends(get_current_user)):
    return UserDetailResponse(
        uuid=str(current_user.id),
        username=current_user.username,
        created_at=current_user.created_at,
    )


@app.put("/user-details", response_model=UserProfileResponse)
async def update_user_details(
    body: UserProfileUpdate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    detail = session.exec(
        select(UserDetail).where(UserDetail.user_id == current_user.id)
    ).first()
    if detail:
        detail.avatar = body.avatar
        detail.avatar_blurhash = body.avatar_blurhash
        detail.bio = body.bio
        detail.timezone = body.timezone
    else:
        detail = UserDetail(
            user_id=current_user.id,
            avatar=body.avatar,
            avatar_blurhash=body.avatar_blurhash,
            bio=body.bio,
            timezone=body.timezone,
        )
        session.add(detail)
    session.commit()
    session.refresh(detail)
    return UserProfileResponse(
        id=str(detail.id),
        avatar=detail.avatar,
        avatar_blurhash=detail.avatar_blurhash,
        bio=detail.bio,
        timezone=detail.timezone,
    )


handler = Mangum(app)
