from common.security import get_current_user, hash_password, verify_password
from fastapi import Depends, FastAPI, HTTPException, status
from common.database import get_session
from auth.schemas import ChangePassword
from common.models.user import User
from sqlmodel import Session
from mangum import Mangum


app = FastAPI()


@app.put("/change-password")
async def change_password(
    body: ChangePassword,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    if not verify_password(body.old_password, current_user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect password"
        )

    current_user.password = hash_password(body.new_password)
    session.add(current_user)
    session.commit()

    return {"message": "Password updated successfully"}


handler = Mangum(app)
