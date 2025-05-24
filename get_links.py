import asyncio
import os

from pumpportal import subscribe

async def get_links():
    try:

        mint, name, metadata = await subscribe()

        token_img = metadata.get('image', None)
        twitter_link = metadata.get('twitter', None)

        if (twitter_link is None) or (token_img is None):
            return None
        
        return mint, name, twitter_link
    
    except Exception as e:
        print(f"Error getting metadata links: {e}")
        return None


async def link_parse():
    try:
            res = await get_links()
            if res is None:
                return None
            
            mint = res[0]
            name = res[1]
            twitter_link = res[2]

            parts = twitter_link.split('/')
            
            if parts == [''] or parts is None or 'status' in parts:
                return None
            elif 'communities' in parts:
                community = parts[-1]
                print(f"Community: {community}, Mint: {mint}")
                return name, mint, community
            else:
                username = parts[-1]
                print(f"Username: {username}, Mint: {mint}")
                return name, mint, username
            
    except Exception as e:
        print(f"Error scraping twitter: {e}")
        return None



if __name__ == '__main__':
    try:
        while True:
            asyncio.run(link_parse())
            #asyncio.run(get_links(metadata_func=subscribe))
    except KeyboardInterrupt:
        print("Keyboard interrupt detected. Loop closing")
        exit()