import asyncio
import websockets
import json
from aiohttp import ClientSession


from get_links import get_links
from get_html import get_html

async def subscribe():
    try:
        uri = "wss://pumpportal.fun/api/data"
        async with websockets.connect(uri) as websocket:
            
            async def keepalive():
                while True:
                    try:
                        await websocket.ping()
                        await asyncio.sleep(5)  # ping every 20 seconds
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

                        token = json.loads(message)
                        
                        market_cap = token.get('marketCapSol', 0)
                        
                        #if market_cap <= 30:
                            #continue
                        
                        mint = token.get('mint', None)
                        
                        if mint is None:
                            continue
                        
                        name = token.get('name')

                        token_metadata_uri = token.get('uri')
                        
                        try:
                            res = await session.get(token_metadata_uri)
                            token_metadata = await res.json()
                        except Exception as e:
                            #metadata links often replaced with image links. clear cut rugs
                            continue
                        
                        description = token_metadata.get('description')
                        
                        if description == '':
                            continue
                        
                        link_info = await get_links(token_metadata)
                    
                        if link_info is None:
                            continue
                        else:
                            link_type = link_info[0]
                            id = link_info[1]
                            
                        tweets = await get_html(link_type=link_type, id=id)
                        
                        if tweets is not None:
                            print(f"Coin: {name}, Tweets: {tweets}")
            finally:
                keepalive_task.cancel()

    except Exception as e:
        print(f"Error subscribing to new token creation logs: {e}")

if __name__ == '__main__':
    try:
        while True:
            asyncio.run(subscribe())
    except KeyboardInterrupt:
        print('Keyboard interrupt detected. Exiting')