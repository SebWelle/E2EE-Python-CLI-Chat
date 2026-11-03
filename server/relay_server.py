import asyncio
import websockets

connected_clients = set()


async def handle_client(websocket):
    connected_clients.add(websocket)

    try:
        async for message in websocket:
            for client in connected_clients:
                if client != websocket:
                    await client.send(message)
                    
    finally:
        
        connected_clients.remove(websocket)              


async def main():
    async with websockets.serve(handle_client, "localhost", 8765):
        print("WebSocket is running on ws://localhost:8765")#

        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())