from fastapi import APIRouter, Depends

from src.db import User
from src.users import current_active_user

router = APIRouter()


@router.get("/profile")
async def authenticated_route(user: User = Depends(current_active_user)):
    return {"message": f"Hello {user.username}!"}
