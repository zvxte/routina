from typing import Annotated

from fastapi import APIRouter, status, Depends
from sqlmodel import Session, select

from ...dependencies import SessionCookie
from ...models.user import UserOut
from ...database import engine, Users, Sessions


router = APIRouter(prefix="/v1/user", tags=["user"])


@router.get("", status_code=status.HTTP_200_OK, response_model=UserOut)
async def get_user(session_cookie: Annotated[SessionCookie, Depends()]) -> UserOut:
    """Returns user data"""
    with Session(engine) as session:
        statement = select(Sessions.user_id).where(
            Sessions.session_id == session_cookie.session_id
        )
        user_id = session.exec(statement).first()

        statement = select(Users).where(Users.user_id == user_id)
        return session.exec(statement).first()


@router.delete("", status_code=status.HTTP_200_OK)
async def delete_user(session_cookie: Annotated[SessionCookie, Depends()]) -> None:
    """Deletes user"""
    with Session(engine) as session:
        statement = select(Sessions.user_id).where(
            Sessions.session_id == session_cookie.session_id
        )
        user_id = session.exec(statement).first()

        statement = select(Users).where(Users.user_id == user_id)
        user_entry = session.exec(statement).first()
        session.delete(user_entry)
        session.commit()

    return None
