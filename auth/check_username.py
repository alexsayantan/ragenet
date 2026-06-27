from fastapi import Depends, FastAPI, Query
from sqlmodel import Session, select

from common.database import get_session
from common.models.user import User
from mangum import Mangum


app = FastAPI()


@app.get("/check-username")
async def check_username(
    username: str = Query(min_length=1),
    session: Session = Depends(get_session),
):
    existing = session.exec(select(User).where(User.username == username)).first()
    return {"available": existing is None}


handler = Mangum(app)
