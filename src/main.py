from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import socketio
import os
import src.routes.price
from src.database import engine, Base
from src.routes.session import router as session_router
from src.routes.course import router as course_router
from src.routes.contact import router as contact_router
from src.routes.participant import router as participant_router
from src.sio import sio

app = FastAPI()

socket_app = socketio.ASGIApp(sio, app)

app.include_router(session_router, prefix="/session")
app.include_router(course_router, prefix="/course")
app.include_router(contact_router, prefix="/contact")
app.include_router(participant_router, prefix="/participant")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://funnel-frontend-b539334e0613.herokuapp.com", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@sio.event
async def connect(sid, environ):
    print("Client connected", sid)

@sio.event
async def disconnect(sid):
    print("Client disconnected", sid)

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(socket_app, host="0.0.0.0", port=port)
