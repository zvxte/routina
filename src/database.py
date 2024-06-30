from uuid import UUID

from sqlmodel import SQLModel, Field, create_engine

from .config import DATABASE_URL, DATABASE_ECHO


class Users(SQLModel, table=True):
    user_id: UUID = Field(primary_key=True, index=True)
    username: str = Field(index=True)
    password: str
    created_at: int


class Sessions(SQLModel, table=True):
    session_id: str = Field(primary_key=True, index=True)
    user_id: UUID = Field(foreign_key="users.user_id")
    user_agent: str | None = Field(default=None)
    created_at: int
    expires_at: int


class Activities(SQLModel, table=True):
    activity_id: UUID = Field(primary_key=True)
    user_id: UUID = Field(foreign_key="users.user_id", index=True)
    title: str
    description: str | None = Field(default=None)
    created_at: int
    ended_at: int | None = Field(default=None)


class Histories(SQLModel, table=True):
    history_id: UUID = Field(primary_key=True, index=True)
    activity_id: UUID = Field(foreign_key="activities.activity_id", index=True)
    year: int = Field(index=True)
    month: int = Field(index=True)
    days: int


engine = create_engine(DATABASE_URL, echo=DATABASE_ECHO)


if __name__ == "__main__":
    # create tables
    SQLModel.metadata.create_all(engine)
