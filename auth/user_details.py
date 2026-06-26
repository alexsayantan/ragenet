from fastapi import Depends, FastAPI

from auth.schemas import UserDetail
from common.models.user import User
from common.security import get_current_user
from mangum import Mangum


app = FastAPI()


@app.get("/user-details", response_model=UserDetail)
async def user_details(current_user: User = Depends(get_current_user)):
    return UserDetail(
        id=current_user.id,
        username=current_user.username,
        created_at=current_user.created_at,
    )


handler = Mangum(app)
