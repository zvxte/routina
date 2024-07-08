from typing import Annotated
from uuid import UUID

from fastapi import Cookie, Header, Path

from .utils import current_year


class UserAgentHeader:
    def __init__(self, user_agent: Annotated[str | None, Header()] = None):
        self.user_agent = user_agent


class SessionCookie:
    def __init__(self, session_id: Annotated[str, Cookie()]):
        self.session_id = session_id


class ActivityPath:
    def __init__(self, activity_id: Annotated[UUID, Path()]):
        self.activity_id = activity_id


class YearPath:
    def __init__(self, year: Annotated[int, Path(ge=2000, le=current_year())]):
        self.year = year


class MonthPath:
    def __init__(self, month: Annotated[int, Path(ge=1, le=12)]):
        self.month = month


class DayPath:
    def __init__(self, day: Annotated[int, Path(ge=1, le=31)]):
        self.day = day
