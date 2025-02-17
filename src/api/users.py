from fastapi import APIRouter, Depends, Request
from src.schemas.users import User
from src.services.auth import get_current_user
from slowapi import Limiter
from slowapi.util import get_remote_address

router = APIRouter(prefix="/users", tags=["users"])
limiter = Limiter(key_func=get_remote_address)


@router.get("/me", response_model=User)
@limiter.limit("10/minute")
async def me(
    request: Request,
    user: User = Depends(get_current_user),
):
    return user
