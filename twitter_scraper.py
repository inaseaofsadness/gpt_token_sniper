import asyncio
from aiohttp import ClientSession
import os

from pumpportal import subscribe

API_KEY = os.getenv('SOCIALDATA_API_KEY')

async def get_links(metadata_func):
    try:

        metadata, mint = await metadata_func()

        token_img = metadata.get('image', None)
        twitter_link = metadata.get('twitter', None)

        if (twitter_link == None) or (token_img == None):
            return
        
        return token_img,twitter_link,mint
    
    except Exception as e:
        print(f"Error getting metadata links: {e}")


async def twitter_scrape(get_links_func, subscribe_func):
    try:
        async with ClientSession() as session:

            res = await get_links_func(subscribe_func)
            if res == None:
                return
            
            twitter_link = res[1]

            mint = res[2]

            parts = twitter_link.split('/')
            
            if parts == [''] or parts == None or 'status' in parts:
                return
            elif 'communities' in parts:
                community = parts[-1]
                url = f'https://api.socialdata.tools/twitter/community/{community}'

                headers = {
                    'Authorization': f'Bearer {API_KEY}',
                    'Accept': 'application/json'
                }

                params = {
                    'count': 15,
                }

                response = await session.get(url, headers=headers, params=params)
                response.raise_for_status()
                community_info = await response.json()

                if community_info['member_count'] <= 40:
                    return
            else:
                username = parts[-1]
                url = f'https://api.socialdata.tools/twitter/user/{username}'

                headers = {
                    'Authorization': f'Bearer {API_KEY}',
                    'Accept': 'application/json'
                }

                response = await session.get(url, headers=headers)
                response.raise_for_status()
                profile_info = await response.json()
                follower_count = profile_info['followers_count']
                user_id = profile_info['id']

                if follower_count <= 40:
                    return
                
                url = f'https://api.socialdata.tools/twitter/user/{user_id}/tweets'

                headers = {
                    'Authorization': f'Bearer {API_KEY}',
                    'Accept': 'application/json'
                }

                response = await session.get(url, headers=headers)
                response.raise_for_status()
                tweets = await response.json()
                return tweets, mint
            
    except Exception as e:
        print(f"Error scraping twitter: {e}")



if __name__ == '__main__':
    try:
        while True:
            asyncio.run(twitter_scrape(get_links_func=get_links,subscribe_func=subscribe))
            #asyncio.run(get_links(metadata_func=subscribe))
    except KeyboardInterrupt:
        print("Keyboard interrupt detected. Loop closing")
        exit()