from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.database import get_db
from src.models import FunnelSessions, FunnelRegistrations
from src.functions.token import create_token, token_exists
from typing import Dict, Any

router = APIRouter()

@router.get("/check/{token}")
async def check_token(token: str, db: AsyncSession = Depends(get_db)):
    print(f"Type of db: {type(db)}")
    exists = await token_exists(token, db)
    return {"exists": exists}


@router.post("/create")
async def create_session(data: Dict[str, Any] = None, db: AsyncSession = Depends(get_db)):
    token = await create_token(db)

    name = data.get("name")
    email = data.get("email")
    phone = data.get("phone")
    children_count = data.get("childrenCount")
    adults_count = data.get("adultsCount")
    selected_course = data.get("selectedCourse")
    
    new_session = FunnelSessions(token=token)
    db.add(new_session)
    await db.commit()
    new_registration = FunnelRegistrations(session_id=new_session.id, course_id=selected_course["id"], name=name.strip(), email=email.strip(), phone=phone.strip(), children_count=children_count, adults_count=adults_count)
    db.add(new_registration)
    await db.commit()
    
    return {"token": token}