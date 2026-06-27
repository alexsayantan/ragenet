from fastapi import Depends, FastAPI, HTTPException, status
from auth.schemas import UserResponse, UserSignup
from common.security import hash_password
from common.database import get_session
from sqlmodel import Session, select
from common.models.user import User
from mangum import Mangum


app = FastAPI()


@app.post("/signup", response_model=UserResponse)
async def signup(body: UserSignup, session: Session = Depends(get_session)):
    existing = session.exec(select(User).where(User.username == body.username)).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username already exists")

    user = User(email=body.email, username=body.username, password=hash_password(body.password))
    session.add(user)
    session.commit()
    session.refresh(user)

    return UserResponse(username=user.username)


handler = Mangum(app)
