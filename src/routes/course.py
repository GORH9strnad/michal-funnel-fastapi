from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update
from src.database import get_db_session
from src.models import FunnelCourses, FunnelSessions, FunnelRegistrations

router = APIRouter()

@router.get("/courses")
async def get_courses(db: AsyncSession = Depends(get_db_session)):
    courses = await db.execute(select(FunnelCourses))
    courses = courses.scalars().all()
    return {"courses": courses}

@router.get("/selected/{token}")
async def get_selected_course(token: str, db: AsyncSession = Depends(get_db_session)):
    result = await db.execute(
        select(FunnelCourses)
        .join(FunnelRegistrations, FunnelCourses.id == FunnelRegistrations.course_id)
        .join(FunnelSessions, FunnelRegistrations.session_id == FunnelSessions.id)
        .where(FunnelSessions.token == token)
    )
    course = result.scalar()

    if course is None:
        raise HTTPException(status_code=404, detail=f"/selected/{token}: no course selected for session with token:{token}")

    return {"course": course}

@router.put("/select/{token}/{course_id}")
async def select_course(token: str, course_id: int, db: AsyncSession = Depends(get_db_session)):
    result = await db.execute(
        select(FunnelSessions)
        .where(FunnelSessions.token == token)
    )
    session = result.scalar()
    
    if session is None:
        raise HTTPException(status_code=404, detail=f"/select/invalid_token/{course_id}: session with token:{token} does not exist")
    
    result = await db.execute(
        select(FunnelCourses)
        .where(FunnelCourses.id == course_id)
    )
    course = result.scalar()
    
    if course is None:
        raise HTTPException(status_code=404, detail=f"/select/{token}/invalid_id: course with id:{course_id} does not exist")
    
    update_result = await db.execute(
        update(FunnelRegistrations)
        .where(FunnelRegistrations.session_id == session.id)
        .values(course_id=course_id)
    )
    
    await db.commit()
    
    if update_result.rowcount == 0:
        raise HTTPException(status_code=404, detail=f"/select/{token}/{course_id}: no registrations found for session with token:{token}")
    
    return {"success": True}