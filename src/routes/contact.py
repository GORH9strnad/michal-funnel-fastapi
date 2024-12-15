from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from src.database import get_db
from src.models import FunnelRegistrations, FunnelSessions
from src.schemas import Name, Email, Phone
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
async def set_name(sid, name):
    try:
        validated_name = Name(name=name)
        await sio.emit("name-valid", {}, to=sid)
    except ValueError as e:
        await sio.emit("name-invalid", {"validation": str(e)}, to=sid)