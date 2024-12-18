from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import socketio
from src.database import engine, Base
from src.routes.session import router as session_router
from src.routes.course import router as course_router
from src.routes.contact import router as contact_router
from.routes.participant import router as participant_router
from src.sio import sio

app = FastAPI()

socket_app = socketio.ASGIApp(sio, app)

# @app.on_event("startup")
# async def startup_event():
#     async with engine.begin() as conn:
#         # await conn.run_sync(Base.metadata.drop_all)
#         await conn.run_sync(Base.metadata.create_all)

app.include_router(session_router, prefix="/session")
app.include_router(course_router, prefix="/course")
app.include_router(contact_router, prefix="/contact")
app.include_router(participant_router, prefix="/participant")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://funnel-frontend-b539334e0613.herokuapp.com/"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(socket_app, host="0.0.0.0", port=8000)