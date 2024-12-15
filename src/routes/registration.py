from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from src.database import get_db
from src.models import FunnelRegistrations, FunnelSessions

router = APIRouter()

@router.get("/contact/{token}")
async def get_contact(token: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(FunnelRegistrations.name, FunnelRegistrations.email, FunnelRegistrations.phone)
        .join(FunnelSessions, FunnelRegistrations.session_id == FunnelSessions.id)
        .where(FunnelSessions.token == token)
    )
    registrations = result.all()
    return {"registrations": registrations}