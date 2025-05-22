import asyncio

from twitter_scraper import get_links, twitter_scrape
from pumpportal import subscribe

async def get_data():
    try:
        scraped_data = await twitter_scrape(get_links_func=get_links,subscribe_func=subscribe)
        if scraped_data == None:
            return
        tweets, mint = scraped_data
        print(tweets)
    except Exception as e:
        print(f"Error fetching tweet data: {e}")

try:
    while True:
        asyncio.run(get_data())
except KeyboardInterrupt:
    print("Keyboard interrupt detected. Exiting")