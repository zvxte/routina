from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from sqlmodel import Session, select

from ...models.activity import ActivityIn, ActivityOut, ActivityUpdate
from ...dependencies import SessionCookie, ActivityPath, YearPath, MonthPath, DayPath
from ...database import Sessions, Activities, Histories, engine
from ...utils import create_uuid_v4, unix_time


router = APIRouter(prefix="/v1/activities", tags=["activities"])


@router.get("", status_code=status.HTTP_200_OK, response_model=list[ActivityOut])
async def get_activities(
    session_cookie: Annotated[SessionCookie, Depends()]
) -> list[ActivityOut]:
    """Returns all activities"""
    with Session(engine) as session:
        statement = select(Sessions.user_id).where(
            Sessions.session_id == session_cookie.session_id
        )
        user_id = session.exec(statement).first()

        statement = select(Activities).where(Activities.user_id == user_id)
        return session.exec(statement).all()


@router.post("", status_code=status.HTTP_200_OK, response_model=ActivityOut)
async def post_activities(
    session_cookie: Annotated[SessionCookie, Depends()],
    activity_in: ActivityIn,
) -> ActivityOut:
    """Creates new activity"""
    with Session(engine) as session:
        statement = select(Sessions.user_id).where(
            Sessions.session_id == session_cookie.session_id
        )
        user_id = session.exec(statement).first()

        new_activity_entry = Activities(
            activity_id=create_uuid_v4(),
            user_id=user_id,
            title=activity_in.title,
            description=activity_in.description,
            created_at=unix_time(),
            ended_at=None,
        )

        session.add(new_activity_entry)
        session.commit()
        session.refresh(new_activity_entry)
        return new_activity_entry


@router.patch("/{activity_id}", status_code=status.HTTP_200_OK)
async def patch_activity(
    session_cookie: Annotated[SessionCookie, Depends()],
    activity_path: Annotated[ActivityPath, Depends()],
    activity_update: ActivityUpdate,
) -> None:
    """Updates activity"""
    with Session(engine) as session:
        statement = select(Sessions.user_id).where(
            Sessions.session_id == session_cookie.session_id
        )
        user_id = session.exec(statement).first()

        statement = select(Activities).where(
            Activities.activity_id == activity_path.activity_id
        )
        activity_entry: Activities | None = session.exec(statement).first()

        if not activity_entry:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Activity not found")

        if not activity_entry.user_id == user_id:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Unathorized")

        if activity_update.title:
            activity_entry.title = activity_update.title
        if activity_update.description:
            activity_entry.description = activity_update.description
        if activity_update.end:
            if activity_update.end is True:
                activity_entry.ended_at = unix_time()

        session.add(activity_entry)
        session.commit()

    return None


@router.delete("/{activity_id}", status_code=status.HTTP_200_OK)
async def delete_activity(
    session_cookie: Annotated[SessionCookie, Depends()],
    activity_path: Annotated[ActivityPath, Depends()],
) -> None:
    """Deletes activity"""
    with Session(engine) as session:
        statement = select(Sessions.user_id).where(
            Sessions.session_id == session_cookie.session_id
        )
        user_id = session.exec(statement).first()

        statement = select(Activities).where(
            Activities.activity_id == activity_path.activity_id
        )
        activity_entry: Activities | None = session.exec(statement).first()

        if not activity_entry:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Activity not found")

        if not activity_entry.user_id == user_id:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Unathorized")

        session.delete(activity_entry)
        session.commit()

    return None


@router.get(
    "/{activity_id}/{year}/{month}",
    status_code=status.HTTP_200_OK,
    response_model=list[int],
)
async def get_activity_history(
    session_cookie: Annotated[SessionCookie, Depends()],
    activity_path: Annotated[ActivityPath, Depends()],
    year_path: Annotated[YearPath, Depends()],
    month_path: Annotated[MonthPath, Depends()],
) -> list[int]:
    """Returns activity history"""
    days_bitmap: int | None = None
    with Session(engine) as session:
        statement = select(Sessions.user_id).where(
            Sessions.session_id == session_cookie.session_id
        )
        user_id = session.exec(statement).first()

        statement = select(Histories.days).where(
            Histories.activity_id == activity_path.activity_id,
            Histories.year == year_path.year,
            Histories.month == month_path.month,
        )
        days_bitmap: int | None = session.exec(statement).first()

    if not days_bitmap:
        return []

    days: [int] = []
    for i in range(days_bitmap.bit_length()):
        day = (days_bitmap >> i) & 1
        if day == 1:
            days.append(i + 1)
    return days


@router.patch("/{activity_id}/{year}/{month}/{day}", status_code=status.HTTP_200_OK)
async def patch_activity_history(
    session_cookie: Annotated[SessionCookie, Depends()],
    activity_path: Annotated[ActivityPath, Depends()],
    year_path: Annotated[YearPath, Depends()],
    month_path: Annotated[MonthPath, Depends()],
    day_path: Annotated[DayPath, Depends()],
) -> None:
    """Updates activity history"""
    with Session(engine) as session:
        statement = select(Sessions.user_id).where(
            Sessions.session_id == session_cookie.session_id
        )
        user_id = session.exec(statement).first()

        statement = select(Histories).where(
            Histories.activity_id == activity_path.activity_id,
            Histories.year == year_path.year,
            Histories.month == month_path.month,
        )
        history_entry: Histories | None = session.exec(statement).first()

        if not history_entry:
            days = 1 << day_path.day - 1
            new_history_entry = Histories(
                history_id=create_uuid_v4(),
                activity_id=activity_path.activity_id,
                year=year_path.year,
                month=month_path.month,
                days=days,
            )
            session.add(new_history_entry)
            session.commit()
        else:
            history_entry.days = history_entry.days ^ 1 << day_path.day - 1
            session.add(history_entry)
            session.commit()

    return None
