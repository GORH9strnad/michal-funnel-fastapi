from fastapi import FastAPI
from src.database import engine, Base
from src.routes.session import router as session_router

app = FastAPI()

# @app.on_event("startup")
# async def startup_event():
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.drop_all)
#         await conn.run_sync(Base.metadata.create_all)

app.include_router(session_router, prefix="/session")