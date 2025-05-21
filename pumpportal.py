import asyncio
import websockets
import json
from aiohttp import ClientSession

async def subscribe():
    try:
        uri = "wss://pumpportal.fun/api/data"
        async with websockets.connect(uri) as websocket:

            async with ClientSession() as session:
        
            # Subscribing to token creation events
                payload = {
                    "method": "subscribeNewToken",
                }

                await websocket.send(json.dumps(payload))
                async for message in websocket:

                    token = json.loads(message)

                    if token.get('marketCapSol',0) < 10:
                        continue

                    token_metadata_uri = token.get('uri', None)

                    if token_metadata_uri == None:
                        continue

                    res = await session.get(token_metadata_uri)
                    token_metadata = await res.json()
                    return token_metadata, token.get('mint',None)

    except Exception as e:
        print(f"Error subscribing to new token creation logs: {e}")

if __name__ == '__main__':
    try:
        asyncio.run(subscribe())
    except KeyboardInterrupt:
        print('Keyboard interrupt detected. Exiting')