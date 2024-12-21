from src.sio import sio
from src.functions.price import calculate_price

@sio.on("price")
async def handle_price(sid, data):
    adults = data.get("adults")
    children = data.get("children")
    
    price = calculate_price(adults, children)

    print(f"Price calculated: {price}")

    await sio.emit("price", {"price": price}, to=sid)