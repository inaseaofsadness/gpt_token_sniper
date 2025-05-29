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
            return

        name = token.get('name')
        token_metadata_uri = token.get('uri')

        try:
            res = await session.get(token_metadata_uri)
            token_metadata = await res.json()
        except Exception:
            print(f"'{name}' (CA: {mint}) failed rug check")
            return

        description = token_metadata.get('description')
        if description == '':
            print(f"'{name}' (CA: {mint}) failed rug check")
            return

        link_info = await get_links(token_metadata)
        if link_info is None:
            print(f"'{name}' (CA: {mint}) failed rug check")
            return

        link_type = link_info[0]
        id = link_info[1]

        
        tweets = await get_html(link_type=link_type, id=id)
        await get_html.browser.close()
        if tweets is not None:
            print(f"{name} (CA: {mint}) passed basic rug test. Fetching community tweets...")
            ai_sentiment = await prompt(tweets=tweets)
            print(f"AI processing '{name}' tweets currently. CA: {mint}")
            print(f"Coin: {name}. Tweets: {tweets}. AI sentiment: {ai_sentiment}")
    except Exception as e:
        print(f"'{name}' (CA: {mint}) failed rug check")
        pass
