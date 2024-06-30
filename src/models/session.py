from typing import Annotated

from pydantic import BaseModel, Field


class Session(BaseModel):
    # log2(62) * 48 = 286 bits of entropy
    session_id: Annotated[
        str, Field(min_length=48, max_length=48, pattern=r"^[A-Za-z0-9]{48,48}$")
    ]


class SessionOut(Session):
    user_agent: str | None = None
    created_at: int
    expires_at: int
