import socketio

sio = socketio.AsyncServer(async_mode="asgi", cors_allowed_origins=["https://funnel-frontend-b539334e0613.herokuapp.com", "http://localhost:3000"])