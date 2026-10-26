from fastapi import APIRouter
from fastapi.params import Depends

from common.dependencies import get_user_service
from models.user import UserResponse, UserLoginRequest
from services.user_service import UserService

router = APIRouter(
    prefix="/user",
    tags=["User"]
)

@router.post("/login", response_model=UserResponse)
def login(req: UserLoginRequest, svc: UserService = Depends(get_user_service)):

    user = svc.login(req)
    redirect_url = "/admin" if user.role == "admin" else "/home"
    return UserResponse(
        uid=user.uid, email=user.email, role=user.role, redirect_url=redirect_url
    )