from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.database import get_db
from src.models import FunnelSessions
from src.functions.token import create_token, token_exists

router = APIRouter()

@router.get("/check/{token}")
async def check_token(token: str, db: AsyncSession = Depends(get_db)):
    print(f"Type of db: {type(db)}")
    exists = await token_exists(token, db)
    return {"exists": exists}


@router.post("/create")
async def create_session(db: AsyncSession = Depends(get_db)):
    token = await create_token(db)
    
    new_session = FunnelSessions(token=token)
    db.add(new_session)
    await db.commit()
    
    return {"token": token}