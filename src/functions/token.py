import secrets
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.models import FunnelSessions

async def token_exists(token: str, db: AsyncSession) -> bool:
    result = await db.execute(select(FunnelSessions).where(FunnelSessions.token == token))
    return result.scalar() is not None

async def create_token(db: AsyncSession) -> str:
    token = secrets.token_urlsafe(8)
    while await token_exists(token, db):
        token = secrets.token_urlsafe(8)
    return token
