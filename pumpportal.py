import asyncio
import websockets
import json
from aiohttp import ClientSession
from get_links import get_links

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
                    
                    market_cap = token.get('marketCapSol', 0)
                    
                    #if market_cap <= 30:
                        #continue
                    
                    mint = token.get('mint', None)
                    
                    if mint is None:
                        continue
                    
                    name = token.get('name')

                    token_metadata_uri = token.get('uri')
                    

                    res = await session.get(token_metadata_uri)
                    token_metadata = await res.json()
                    
                    description = token_metadata.get('description')
                    
                    if description == '':
                        continue
                    
                    link_info = await get_links(token_metadata)
                
                    if link_info is None:
                        continue
                    else:
                        link_type = link_info[0]
                        id = link_info[1]
                        
                    print(link_type, id)
                    #return mint, name, token_metadata

    except Exception as e:
        print(f"Error subscribing to new token creation logs: {e}")

if __name__ == '__main__':
    try:
        asyncio.run(subscribe())
    except KeyboardInterrupt:
        print('Keyboard interrupt detected. Exiting')