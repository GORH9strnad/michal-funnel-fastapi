from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from src.database import get_db
from src.models import FunnelRegistrations, FunnelSessions
from src.functions.contact import validate_name, validate_email, validate_phone
from src.sio import sio

router = APIRouter()

@router.get("/contact/{token}")
async def get_contact(token: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(FunnelRegistrations.name, FunnelRegistrations.email, FunnelRegistrations.phone)
        .join(FunnelSessions, FunnelRegistrations.session_id == FunnelSessions.id)
        .where(FunnelSessions.token == token)
    )
    contact = result.all()

    if not contact:
        HTTPException(status_code=404, detail=f"/contact/contact/{token}: no contact found for session with token:{token}")

    return {"contact": contact}

@sio.on("validate-name")
async def handle_validate_name(sid, name):
    try:
        validate_name(name.strip())
        await sio.emit("validate-name", {"valid": True}, to=sid)
    except ValueError as e:
        await sio.emit("validate-name", {"valid": False, "error": str(e)}, to=sid)

@sio.on("validate-email")
async def handle_validate_email(sid, email):
    try:
        validate_email(email.strip())
        await sio.emit("validate-email", {"valid": True}, to=sid)
    except ValueError as e:
        await sio.emit("validate-email", {"valid": False, "error": str(e)}, to=sid)

@sio.on("validate-phone")
async def handle_validate_phone(sid, phone):
    try:
        validate_phone(phone.replace(" ", ""))
        await sio.emit("validate-phone", {"valid": True}, to=sid)
    except ValueError as e:
        await sio.emit("validate-phone", {"valid": False, "error": str(e)}, to=sid)