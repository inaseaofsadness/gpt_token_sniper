import asyncio
import os

from pumpportal import subscribe

async def get_links():
    try:

        metadata, mint = await subscribe()

        token_img = metadata.get('image', None)
        twitter_link = metadata.get('twitter', None)

        if (twitter_link is None) or (token_img is None):
            return None
        
        return token_img,twitter_link,mint
    
    except Exception as e:
        print(f"Error getting metadata links: {e}")
        return None


async def link_parse():
    try:
            res = await get_links()
            if res is None:
                return None
            
            twitter_link = res[1]

            mint = res[2]

            parts = twitter_link.split('/')
            
            if parts == [''] or parts is None or 'status' in parts:
                return None
            elif 'communities' in parts:
                community = parts[-1]
                print(community, mint)
                return community
            else:
                username = parts[-1]
                print(username, mint)
                return username
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