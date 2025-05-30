import asyncio
import random
from playwright.async_api import async_playwright
import html2text
import os
import json
from datetime import datetime, timezone

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
    tweets = []
    proxy_list = []
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
            
            safe_agent_name = agent.replace("/", "_").replace(";", "").replace("(", "").replace(")", "").replace(" ", "_").replace(":","")
            storage_state_path = f"./agents/{safe_agent_name}.json"
            
            if not os.path.exists("./agents"):
                os.mkdir("./agents")
            
            if os.path.exists(storage_state_path):
                context = await browser.new_context(
                    storage_state=storage_state_path,
                    user_agent=agent,
                    viewport=port,
                    java_script_enabled=True
                    )
            else:
                context = await browser.new_context(
                    user_agent=agent,
                    viewport=port,
                    java_script_enabled=True,
                    )
                await context.storage_state(path=storage_state_path)
                
            page = await context.new_page()
            
            if link_type == 'community':
                url = f'https://x.com/i/communities/{id}'
            else:
                url = f'https://x.com/{id}'
                
            await page.goto(url=url)
            await page.wait_for_load_state('networkidle')
            
            articles = await page.query_selector_all('article')
            
            if articles == []:
                return None
            
            i = 0
            
            for article in articles:
                time_elem = await article.query_selector("time")
                if time_elem:
                    timestamp = await time_elem.get_attribute("datetime")
                    tweet_time = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
                    now = datetime.now(timezone.utc)
                    age_minutes = (now - tweet_time).total_seconds() / 60
                    if age_minutes >= 10:
                        break
                else:
                    break
                    
                raw_html = await article.inner_html()
                raw_html = await article.inner_html()
                h = CleanHTML2Text()
                parsed = h.handle(raw_html)
                
                if 'reposted' in parsed.lower():
                    continue
                
                tweet_text = f"""
                --- ✦ TWEET BREAK ✦ ---
                {link_type} tweet:
                {parsed.strip()}
                """    
                tweets.append(tweet_text)
                
                i += 1
                
                if i == 3:
                    break
            
            if tweets == []:
                return None
            
            return tweets
            
    except Exception as e:
        pass       
if __name__ == "__main__":
    link_type = "user"
    id = "solana"
    asyncio.run(get_html(link_type= link_type, id= id))