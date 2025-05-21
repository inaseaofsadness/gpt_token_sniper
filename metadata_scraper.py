import asyncio
from crawl4ai import *

from pumpportal import subscribe

async def get_links(metadata_func):
    try:

        metadata, mint = await metadata_func()

        token_img = metadata.get('image', None)
        twitter_link = metadata.get('twitter', None)
        website_link  = metadata.get('website',None)

        if (twitter_link == None) or (token_img == None) or (website_link == None):
            return
        
        print(mint)
        return token_img,twitter_link,website_link,mint
    
    except Exception as e:
        print(f"Error getting metadata links: {e}")


async def twitter_scrape(get_links_func, metadata_func):
    res = await get_links_func(metadata_func)
    if res == None:
        return
    
    twitter_link = res[1]
    mint = res[3]
    
    async with AsyncWebCrawler() as crawler:
        res = await crawler.arun(
            url = twitter_link
        )
        print(res.markdown)


if __name__ == '__main__':
    try:
        while True:
            asyncio.run(twitter_scrape(get_links_func=get_links,metadata_func=subscribe))
            #asyncio.run(get_links(metadata_func=subscribe))
    except KeyboardInterrupt:
        print("Keyboard interrupt detected. Loop closing")
        exit()