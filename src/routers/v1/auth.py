from fastapi import APIRouter

from ...models.user import UserIn, UserOut


router = APIRouter(prefix="/v1/auth", tags=["auth"])


@router.post("/register")
def register(_user_in: UserIn) -> UserOut:
    return ...


@router.post("/login")
def login(user_in: UserIn) -> UserOut:
    return ...
