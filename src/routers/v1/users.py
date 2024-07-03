from typing import Annotated

from fastapi import APIRouter, status, Depends

from ...dependencies import UserPath, SessionCookie
from ...models.user import UserOut


router = APIRouter(prefix="/v1/users", tags=["users"])


@router.get("/{user_id}", status_code=status.HTTP_200_OK, response_model=UserOut)
def get_user(
    session_cookie: Annotated[SessionCookie, Depends()],
    user_path: Annotated[UserPath, Depends()],
) -> UserOut: ...


""" TODO """
# @router.patch("/{user_id}", status_code=status.HTTP_200_OK)
# def patch_user(
#     session_cookie: Annotated[SessionCookie, Depends()],
#     user_path: Annotated[UserPath, Depends()],
#     #  and some requst body in json
# ): ...


# @router.delete("/{user_id}", status_code=status.HTTP_200_OK)
# def delete_user(
#     session_cookie: Annotated[SessionCookie, Depends()],
#     user_path: Annotated[UserPath, Depends()],
# ): ...
