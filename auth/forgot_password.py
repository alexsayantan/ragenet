from auth.schemas import ForgotPasswordRequest, ResetPasswordRequest
from common.security import create_access_token, hash_password
from fastapi import Depends, FastAPI, HTTPException, status
from common.email.sender import send_email
from common.database import get_session
from sqlmodel import Session, select
from common.models.user import User
from common.config import settings
from datetime import timedelta
from jose import JWTError, jwt
from mangum import Mangum

app = FastAPI()


@app.post("/forgot-password")
async def forgot_password(
    body: ForgotPasswordRequest, session: Session = Depends(get_session)
):
    user = session.exec(select(User).where(User.email == body.email)).first()

    if not user:
        return {"message": "If this email exists, a password reset link has been sent."}

    reset_token = create_access_token(
        data={"sub": user.email, "type": "password_reset"},
        expires_delta=timedelta(minutes=15),
    )

    reset_link = f"https://ragenet.app/reset-password?token={reset_token}"
    html_body = f"""<html><body><h2>Password Reset</h2><p>Click <a href="{reset_link}">here</a> to reset your password. This link expires in 15 minutes.</p></body></html>"""

    send_email(
        to_email=user.email,
        subject="Password Reset Request",
        html_body=html_body,
    )

    return {"message": "If this email exists, a password reset link has been sent."}


@app.post("/reset-password")
async def reset_password(
    body: ResetPasswordRequest, session: Session = Depends(get_session)
):
    try:
        payload = jwt.decode(
            body.token, settings.secret_key, algorithms=[settings.algorithm]
        )
        email: str = payload.get("sub")
        token_type: str = payload.get("type")

        if email is None or token_type != "password_reset":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token"
            )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired token",
        )

    user = session.exec(select(User).where(User.email == email)).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token"
        )

    user.password = hash_password(body.new_password)
    session.add(user)
    session.commit()

    return {"message": "Password reset successfully"}


handler = Mangum(app)
