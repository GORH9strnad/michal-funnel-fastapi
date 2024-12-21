from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update
from src.database import get_db
from src.models import FunnelSessions, FunnelRegistrations
from src.sio import sio

router = APIRouter()

@router.get("/participants/{token}")
async def get_participants(token: str, db: AsyncSession = Depends(get_db)):
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

    if token:
        db = await anext(get_db())
        session_id_query = (
            select(FunnelSessions.id)
            .where(FunnelSessions.token == token)
        )
        session_id = await db.execute(session_id_query)
        session_id = session_id.scalar()
        if session_id:
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

    if token:
        db = await anext(get_db())
        session_id_query = (
            select(FunnelSessions.id)
            .where(FunnelSessions.token == token)
        )
        session_id = await db.execute(session_id_query)
        session_id = session_id.scalar()
            
        if session_id:
            async with db.begin():
                await db.execute(
                    update(FunnelRegistrations)
                    .where(FunnelRegistrations.session_id == session_id)
                    .values(children_count=children)
                )
                print(f"Children count updated to {children} for session with token: {token}")
        else:
            print(f"No session found for token: {token}")
