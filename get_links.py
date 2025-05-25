import asyncio
import os

#from pumpportal import subscribe

async def get_links(metadata):
    try:
        token_img = metadata.get('image', None)
        twitter_link = metadata.get('twitter', None)

        if (twitter_link is None) or (token_img is None):
            return None
        
        parts = twitter_link.split('/')
            
        if parts == [''] or parts is None or 'status' in parts:
            return None
        elif 'communities' in parts:
            link_type = 'community link'
            community = parts[-1]
            return link_type, community
        elif 'username' in parts:
            link_type = 'user link'
            username = parts[-1]
            return link_type, username
    
    except Exception as e:
        print(f"Error getting metadata links: {e}")
        return None


if __name__ == '__main__':
    try:
        while True:
            asyncio.run(get_links())
    except Exception as e:
        print("Keyboard interrupt detected. Loop closing")
        exit()