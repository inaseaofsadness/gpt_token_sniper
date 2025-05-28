import json
from get_links import get_links
from get_html import get_html
from llm import prompt

async def process_token_message(message, session):
    try:
        token = json.loads(message)
        market_cap = token.get('marketCapSol', 0)
        
        # if market_cap <= 30:
        #     return

        mint = token.get('mint', None)
        if mint is None:
            return 0

        name = token.get('name')
        token_metadata_uri = token.get('uri')

        try:
            res = await session.get(token_metadata_uri)
            token_metadata = await res.json()
        except Exception:
            return 0

        description = token_metadata.get('description')
        if description == '':
            return 0

        link_info = await get_links(token_metadata)
        if link_info is None:
            return 0

        link_type = link_info[0]
        id = link_info[1]

        print(f"{name} (CA: {mint}) passed basic rug test. Fetching community tweets...")
        tweets = await get_html(link_type=link_type, id=id)
        if tweets is not None:
            print(f"AI processing '{name}' tweets currently. CA: {mint}")
            ai_sentiment = await prompt(tweets=tweets)
            print(f"Coin: {name}. Tweets: {tweets}. AI sentiment: {ai_sentiment}")
    except Exception as e:
        pass

# ...existing code...