from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update
from src.database import get_db, get_db_session
from src.models import FunnelSessions, FunnelRegistrations
from src.sio import sio

router = APIRouter()

@router.get("/participants/{token}")
async def get_participants(token: str, db: AsyncSession = Depends(get_db_session)):
    result = await db.execute(
        select(FunnelRegistrations.adults_count, FunnelRegistrations.children_count)
        .join(FunnelSessions, FunnelRegistrations.session_id == FunnelSessions.id)
        .where(FunnelSessions.token == token)
    )

    participants = result.fetchone()

    if not participants:
        raise HTTPException(status_code=404, detail=f"/participants/{token}: no participants found for session with token:{token}")

    return {"adults": participants.adults_count, "children": participants.children_count}

@sio.on("adults")
async def handle_adults(sid, data):
    adults = data.get("adults")
    token = data.get("token")

    if not token:
        print("No token provided.")
        return

    async with get_db() as db:
        # Query session ID using the token
        session_id_query = select(FunnelSessions.id).where(FunnelSessions.token == token)
        result = await db.execute(session_id_query)
        session_id = result.scalar()

        if session_id:
            # Update adults count
            await db.execute(
                update(FunnelRegistrations)
                .where(FunnelRegistrations.session_id == session_id)
                .values(adults_count=adults)
            )
            print(f"Adults count updated to {adults} for session with token: {token}")
        else:
            print(f"No session found for token: {token}")

@sio.on("children")
async def handle_children(sid, data):
    children = data.get("children")
    token = data.get("token")

    if not token:
        print("No token provided.")
        return

    async with get_db() as db:
        # Query session ID using the token
        session_id_query = select(FunnelSessions.id).where(FunnelSessions.token == token)
        result = await db.execute(session_id_query)
        session_id = result.scalar()

        if session_id:
            # Update children count
            await db.execute(
                update(FunnelRegistrations)
                .where(FunnelRegistrations.session_id == session_id)
                .values(children_count=children)
            )
            print(f"Children count updated to {children} for session with token: {token}")
        else:
            print(f"No session found for token: {token}")