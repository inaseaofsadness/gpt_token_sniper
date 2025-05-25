import asyncio
import random
from playwright.async_api import async_playwright
import html2text

import json

class CleanHTML2Text(html2text.HTML2Text):
    def __init__(self):
        super().__init__()
        self.ignore_links = True  # Does not always affect emojis/images
        self.ignore_images = True
        self.body_width = 0  # Don't wrap lines

    def handle_tag(self, tag, attrs, start):
        if tag == "img":
            return  # Nuke images from orbit
        return super().handle_tag(tag, attrs, start)
    
with open('./browser/pc.json') as pc_agents:
    pc = json.load(pc_agents)
    
with open('./browser/mobile.json') as mobile_agents:
    mobile = json.load(mobile_agents)
    
async def get_html(link_type, id):
    try:
        async with async_playwright() as playwright:
            chromium = playwright.chromium
            
            slowmo = random.randint(200,800)
            
            browser = await chromium.launch(headless=True, slow_mo=slowmo)
            
            is_mobile = random.choice([True, False])
            
            if is_mobile is True:
                agent,port = random.choice(list(mobile.items()))
            else:
                agent,port = random.choice(list(pc.items()))
            
            context = await browser.new_context(user_agent=agent, viewport=port, java_script_enabled=True)
            
            page = await context.new_page()
            
            if link_type == 'community':
                url = f'https://x.com/i/communities/{id}'
            else:
                url = f'https://x.com/{id}'
                
            await page.goto(url=url)
            
            await page.wait_for_load_state('networkidle')
            num_articles = 5
             
            tweets = []
            
            for i in range(1, num_articles + 1):
                
                selector = f"article:nth-of-type({i})"
                
                article = await page.query_selector(selector)
                if not article:
                    break
                
                raw_html = await article.inner_html()
                h = CleanHTML2Text()
                
                parsed = h.handle(raw_html)
                
                if 'reposted' in parsed.lower():
                    continue
                
                tweet = f"--- ✦ TWEET BREAK ✦ ---\n {parsed.strip()}"
                tweets.append(tweet)
             
            if tweets != []:
                print(tweets)
                
            
    
    except Exception as e:
        print(f"Error {e}")