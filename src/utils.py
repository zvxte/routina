from string import ascii_letters, digits
from secrets import choice
from uuid import uuid4, UUID
from time import time


def create_uuid_v4() -> UUID:
    return uuid4()


def create_session_id() -> str:
    return "".join(choice(ascii_letters + digits) for i in range(48))


def unix_time() -> int:
    return int(time())
