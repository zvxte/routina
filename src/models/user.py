from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, Field


class User(BaseModel):
    username: Annotated[
        str, Field(min_length=4, max_length=16, pattern=r"^[A-Za-z0-9_]{4,16}$")
    ]


class UserIn(User):
    password: Annotated[str, Field(min_length=8, max_length=128)]


class UserOut(User):
    user_id: UUID
    created_at: int
