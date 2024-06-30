from typing import Annotated

from fastapi import APIRouter, Header, Depends, HTTPException, status, Response
from sqlmodel import Session, select

from ...models.user import UserIn, UserOut
from ...models.session import SessionOut
from ...dependencies import SessionCookie, UserAgentHeader
from ...database import engine, Users, Sessions
from ...utils import create_uuid_v4, create_session_id, unix_time
from ...crypto import hash_password, verify_hashed_password
from ...config import SESSION_DURATION


router = APIRouter(prefix="/v1/auth", tags=["auth"])


@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(
    user_agent_header: Annotated[UserAgentHeader, Depends()],
    user_in: UserIn,
    response: Response,
) -> None:
    """
    Registers a new user.
    Sets session ID in a cookie.
    """
    # check if username is already taken
    statement = select(Users.username).where(Users.username == user_in.username)
    with Session(engine) as session:
        if session.exec(statement).first():
            raise HTTPException(
                status.HTTP_409_CONFLICT, detail="This username is already taken"
            )

    # register a new user
    new_user_entry = Users(
        user_id=create_uuid_v4(),
        username=user_in.username,
        password=hash_password(user_in.password),
        created_at=unix_time(),
    )
    session_id = create_session_id()
    new_session_entry = Sessions(
        session_id=session_id,
        user_id=new_user_entry.user_id,
        user_agent=user_agent_header.user_agent,
        created_at=unix_time(),
        expires_at=unix_time() + SESSION_DURATION,
    )
    with Session(engine) as session:
        session.add(new_user_entry)
        session.add(new_session_entry)
        session.commit()

    # set session-id cookie
    response.set_cookie(
        key="session-id",
        value=session_id,
        samesite="strict",
        httponly=True,
        secure=True,
    )

    return None


@router.post("/login", status_code=status.HTTP_200_OK)
def login(
    user_agent_header: Annotated[UserAgentHeader, Depends()],
    user_in: UserIn,
    response: Response,
) -> None:
    """
    Logs an existing user in.
    Sets session ID in a cookie.
    """
    # check if user exists
    statement = select(Users).where(Users.username == user_in.username)
    user_entry: Users = None
    with Session(engine) as session:
        user_entry = session.exec(statement).first()
        if not user_entry:
            raise HTTPException(
                status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password"
            )

    # verify password
    # hashed_password = hash_password(user_in.password)
    is_verified = verify_hashed_password(user_in.password, user_entry.password)
    if not is_verified:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password"
        )

    # verified, create new session
    session_id = create_session_id()
    new_session_entry = Sessions(
        session_id=session_id,
        user_id=user_entry.user_id,
        user_agent=user_agent_header.user_agent,
        created_at=unix_time(),
        expires_at=unix_time() + SESSION_DURATION,
    )
    with Session(engine) as session:
        session.add(new_session_entry)
        session.commit()

    # set session-id cookie
    response.set_cookie(
        key="session-id",
        value=session_id,
        samesite="strict",
        httponly=True,
        secure=True,
    )

    return None


@router.get("/sessions")
def get_sessions(
    session_cookie: Annotated[SessionCookie, Depends()]
) -> list[SessionOut]:
    """Returns all active sessions"""
    ...


@router.patch("/sessions")
def patch_session(session_cookie: Annotated[SessionCookie, Depends()]) -> None:
    """Updates session expiration time"""
    ...


@router.delete("/sessions")
def delete_session(session_cookie: Annotated[SessionCookie, Depends()]) -> None:
    """Deletes session"""
    ...
