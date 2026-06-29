from common.models.user import User, UserDetail
from common.security import get_current_user
from common.database import get_session
from common.utils.cloudflare_utils import r2_client
from fastapi import Depends, FastAPI, HTTPException, UploadFile, File, status
from sqlmodel import Session, select
from mangum import Mangum

app = FastAPI()


@app.put("/avatar")
async def update_avatar(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only image files are allowed",
        )

    content = await file.read()
    file_ext = (
        file.filename.rsplit(".", 1)[-1]
        if file.filename and "." in file.filename
        else "png"
    )
    file_name = f"avatars/{current_user.id}.{file_ext}"

    url = r2_client.upload_file(file_name, content, file.content_type)

    detail = session.exec(
        select(UserDetail).where(UserDetail.user_id == current_user.id)
    ).first()

    if detail:
        old_avatar = detail.avatar
        detail.avatar = url
        if old_avatar:
            old_key = old_avatar.replace(f"{r2_client.public_url}/", "")
            r2_client.delete_file(old_key)
    else:
        detail = UserDetail(user_id=current_user.id, avatar=url)
        session.add(detail)

    session.commit()
    session.refresh(detail)

    return {"url": url, "id": str(detail.id)}


@app.delete("/avatar")
async def remove_avatar(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    detail = session.exec(
        select(UserDetail).where(UserDetail.user_id == current_user.id)
    ).first()

    if not detail or not detail.avatar:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Avatar not found",
        )

    key = detail.avatar.replace(f"{r2_client.public_url}/", "")
    r2_client.delete_file(key)

    detail.avatar = None
    session.commit()
    session.refresh(detail)

    return {"detail": "Avatar removed successfully"}


handler = Mangum(app)
