from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import socketio
from src.database import engine, Base
from src.routes.session import router as session_router
from src.routes.course import router as course_router
from src.routes.registration import router as registration_router

sio = socketio.AsyncServer(async_mode="asgi", cors_allowed_origins="*")
app = FastAPI()

socket_app = socketio.ASGIApp(sio, app)

@app.on_event("startup")
async def startup_event():
    async with engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

app.include_router(session_router, prefix="/session")
app.include_router(course_router, prefix="/course")
app.include_router(registration_router, prefix="/registration")

# Add CORS middleware if needed
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace "*" with your allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define Socket.IO events
@sio.event
async def connect(sid, environ):
    print(f"Client connected: {sid}")
    await sio.emit("message", {"data": "Welcome!"}, to=sid)

@sio.event
async def disconnect(sid):
    print(f"Client disconnected: {sid}")

@sio.event
async def message(sid, data):
    print(f"Message from {sid}: {data}")
    await sio.emit("response", {"data": f"Server received: {data}"}, to=sid)
