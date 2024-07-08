from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, Field


class Activity(BaseModel):
    title: Annotated[
        str,
        Field(min_length=4, max_length=16, pattern=r"^[A-Za-z0-9\_\-\.\,\!\ ]{4,16}$"),
    ]
    description: Annotated[
        str | None,
        Field(
            default=None,
            min_length=4,
            max_length=128,
            pattern=r"^[A-Za-z0-9\_\-\.\,\!\ ]{4,128}$",
        ),
    ] = None


class ActivityIn(Activity):
    pass


class ActivityOut(Activity):
    activity_id: UUID
    created_at: int
    ended_at: int | None = None


class ActivityUpdate(BaseModel):
    title: Annotated[
        str | None,
        Field(
            default=None,
            min_length=4,
            max_length=16,
            pattern=r"^[A-Za-z0-9\_\-\.\,\!\ ]{4,16}$",
        ),
    ] = None
    description: Annotated[
        str | None,
        Field(
            default=None,
            min_length=4,
            max_length=128,
            pattern=r"^[A-Za-z0-9\_\-\.\,\!\ ]{4,128}$",
        ),
    ] = None
    end: bool | None = None
