from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update
from sqlalchemy.orm import joinedload
from src.database import get_db_session
from src.models import FunnelRegistrations, FunnelSessions
from src.functions.contact import validate_name, validate_email, validate_phone
from src.sio import sio

router = APIRouter()

@router.get("/contact/{token}")
async def get_contact(token: str, db: AsyncSession = Depends(get_db_session)):
    result = await db.execute(
        select(FunnelRegistrations.name, FunnelRegistrations.email, FunnelRegistrations.phone)
        .join(FunnelSessions, FunnelRegistrations.session_id == FunnelSessions.id)
        .where(FunnelSessions.token == token)
    )
    contact = result.fetchone()

    if not contact:
        raise HTTPException(status_code=404, detail=f"/contact/contact/{token}: no contact found for session with token:{token}")

    return {"contact": {
        "name": contact.name,
        "email": contact.email,
        "phone": contact.phone,
    }}

@sio.on("name")
async def handle_validate_name(sid, data, db: AsyncSession = None):
    if db is None:
        db = await get_db_session().__anext__()

    name = data.get("name")
    token = data.get("token")

    try:
        validate_name(name.strip())
        await sio.emit("name", {"valid": True}, to=sid)

        if token:
            subquery = (
                select(FunnelSessions.id)
                .where(FunnelSessions.token == token)
                .scalar_subquery()
            )
            await db.execute(
                update(FunnelRegistrations)
                .where(FunnelRegistrations.session_id == subquery)
                .values(name=name.strip())
            )

            await db.commit()

    except ValueError as e:
        await sio.emit("name", {"valid": False, "error": str(e)}, to=sid)

@sio.on("email")
async def handle_validate_email(sid, data, db: AsyncSession = None):
    if db is None:
        db = await get_db_session().__anext__()

    email = data.get("email")
    token = data.get("token")

    try:
        validate_email(email.strip())
        await sio.emit("email", {"valid": True}, to=sid)

        if token:
            await db.execute(
                update(FunnelRegistrations)
                .where(
                    FunnelRegistrations.session_id == select(FunnelSessions.id)
                    .where(FunnelSessions.token == token)
                    .scalar_subquery()
                )
                .values(email=email.strip())
            )
            await db.commit()
    except ValueError as e:
        await sio.emit("email", {"valid": False, "error": str(e)}, to=sid)


@sio.on("phone")
async def handle_validate_phone(sid, data, db: AsyncSession = None):
    if db is None:
        db = await get_db_session().__anext__()

    phone = data.get("phone")
    token = data.get("token")

    try:
        validate_phone(phone.replace(" ", ""))
        await sio.emit("phone", {"valid": True}, to=sid)

        if token:
            await db.execute(
                update(FunnelRegistrations)
                .where(
                    FunnelRegistrations.session_id == select(FunnelSessions.id)
                    .where(FunnelSessions.token == token)
                    .scalar_subquery()
                )
                .values(phone=phone.replace(" ", ""))
            )
            await db.commit()
    except ValueError as e:
        await sio.emit("phone", {"valid": False, "error": str(e)}, to=sid)
