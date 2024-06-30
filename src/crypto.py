from argon2 import PasswordHasher
from argon2.exceptions import Argon2Error


ph = PasswordHasher(memory_cost=19456, time_cost=2, parallelism=1)


def hash_password(password: str) -> str:
    return ph.hash(password)


def verify_hashed_password(password: str, hashed_password: str) -> bool:
    try:
        ph.verify(hashed_password, password)
        return True
    except Argon2Error:
        return False
