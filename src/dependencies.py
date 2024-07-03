from typing import Annotated
from uuid import UUID

from fastapi import Cookie, Header


class UserAgentHeader:
    def __init__(self, user_agent: Annotated[str | None, Header()] = None):
        self.user_agent = user_agent


class SessionCookie:
    def __init__(self, session_id: Annotated[str, Cookie()]):
        self.session_id = session_id
