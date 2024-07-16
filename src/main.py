from fastapi import FastAPI

from .routers.v1 import auth as v1_auth, user as v1_user, activities as v1_activities
from .middlewares import ValidateSession
from .config import DOCS_URL


app = FastAPI(
    title="routina",
    description="Routines tracker",
    docs_url=DOCS_URL,
)

app.include_router(v1_auth.router)
app.include_router(v1_user.router)
app.include_router(v1_activities.router)

app.add_middleware(ValidateSession)
