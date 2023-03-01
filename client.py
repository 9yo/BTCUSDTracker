import asyncio
import json
import websockets

async def receive_data():
    async with websockets.connect("ws://localhost:9000/test") as websocket:
        while True:
            message = await websocket.recv()
            print(message)
            data = json.loads(message)
            print(f"Received data: {data}")

asyncio.run(receive_data())
