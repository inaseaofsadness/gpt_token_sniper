import asyncio
import websockets
import json
from aiohttp import ClientSession

from process_message import process_token_message
from version import __version__

async def subscribe():
    try:
        uri = "wss://pumpportal.fun/api/data"
        async with websockets.connect(uri) as websocket:
            
            async def keepalive():
                while True:
                    try:
                        await websocket.ping()
                        await asyncio.sleep(2) 
                    except Exception:
                        break
            
            keepalive_task = asyncio.create_task(keepalive())
            
            try:
                async with ClientSession() as session:
            
                # Subscribing to token creation events
                    payload = {
                        "method": "subscribeNewToken",
                    }
                    await websocket.send(json.dumps(payload))
                    async for message in websocket:
                        asyncio.create_task(process_token_message(message, session))       
            finally:
                keepalive_task.cancel()

    except Exception as e:
        print(f"Error subscribing to new token creation logs: {e}")

if __name__ == '__main__':
    try:
        print(f"Running sniper version {__version__}")
        while True:
            asyncio.run(subscribe())
    except KeyboardInterrupt:
        print('Keyboard interrupt detected. Exiting')