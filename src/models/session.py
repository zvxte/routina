from typing import Annotated

from pydantic import BaseModel, Field


class Session(BaseModel):
    session_id: Annotated[
        str, Field(min_length=32, max_length=32, pattern=r"^[A-Za-z0-9]{32,32}$")
    ]


class SessionOut(Session):
    user_agent: str | None = None
    created_at: int
    expires_at: int
