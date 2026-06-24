from auth.config import create_access_token, verify_password
from fastapi import Depends, FastAPI, HTTPException, status
from auth.schemas import TokenResponse, UserSignin
from common.database import get_session
from sqlmodel import Session, select
from common.models.user import User
from mangum import Mangum

app = FastAPI()


@app.post("/signin", response_model=TokenResponse)
async def signin(body: UserSignin, session: Session = Depends(get_session)):
    user = session.exec(select(User).where(User.username == body.username)).first()
    if not user or not verify_password(body.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )

    access_token = create_access_token(data={"sub": user.username})
    return TokenResponse(access_token=access_token)


handler = Mangum(app)
