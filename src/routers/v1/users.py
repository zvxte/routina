from typing import Annotated

from fastapi import APIRouter, status, Depends
from sqlmodel import Session, select

from ...dependencies import SessionCookie
from ...models.user import UserOut
from ...database import engine, Users, Sessions


router = APIRouter(prefix="/v1/users", tags=["users"])


@router.get("", status_code=status.HTTP_200_OK, response_model=UserOut)
async def get_user(session_cookie: Annotated[SessionCookie, Depends()]) -> UserOut:
    with Session(engine) as session:
        statement = select(Sessions.user_id).where(
            Sessions.session_id == session_cookie.session_id
        )
        user_id = session.exec(statement).first()

        statement = select(Users).where(Users.user_id == user_id)
        return session.exec(statement).first()


""" TODO """
# @router.patch("", status_code=status.HTTP_200_OK)
# async def patch_user(
#     session_cookie: Annotated[SessionCookie, Depends()]
#     #  and some requst body in json
# ): ...


# @router.delete("", status_code=status.HTTP_200_OK)
# async def delete_user(
#     session_cookie: Annotated[SessionCookie, Depends()]
# ): ...
