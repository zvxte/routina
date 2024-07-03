from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from pydantic import ValidationError
from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
from sqlmodel import Session as SQLSession, select

from .database import engine, Sessions
from .models.session import Session
from .utils import unix_time


class ValidateSession(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        session_id = request.cookies.get("session_id")
        if session_id:
            try:
                Session(session_id=session_id)
            except ValidationError:
                return JSONResponse(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    content={"message": "Invalid session"},
                )
            statement = select(Sessions).where(Sessions.session_id == session_id)
            with SQLSession(engine) as session:
                session_entry: Sessions = session.exec(statement).first()
                if not session_entry:
                    return JSONResponse(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        content={"message": "Invalid session"},
                    )
                if unix_time() > session_entry.expires_at:
                    session.delete(session_entry)
                    session.commit()
                    response = JSONResponse(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        content={"message": "Session expired"},
                    )
                    response.delete_cookie(
                        key="session_id",
                        samesite="strict",
                        httponly=True,
                        secure=True,
                    )
                    return response

        response = await call_next(request)
        return response
