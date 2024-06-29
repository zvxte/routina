from typing import Annotated

from fastapi import APIRouter, Header

from ...models.user import UserIn, UserOut
from ...models.session import SessionOut


router = APIRouter(prefix="/v1/auth", tags=["auth"])


@router.post("/register")
def register(user_in: UserIn):
    """
    Registers new user.
    Returns new session ID in response headers.
    """
    ...


@router.post("/login")
def login(user_in: UserIn):
    """
    Logs existing user in.
    Returns new session ID in response headers.
    """
    ...


@router.get("/sessions")
def get_sessions(session_id: Annotated[str, Header()]) -> list[SessionOut]:
    """Returns all active sessions"""
    ...


@router.patch("/sessions")
def patch_session(session_id: Annotated[str, Header()]) -> None:
    """Updates session expiration time"""
    ...


@router.delete("/sessions")
def delete_session(session_id: Annotated[str, Header()]) -> None:
    """Deletes session"""
    ...
