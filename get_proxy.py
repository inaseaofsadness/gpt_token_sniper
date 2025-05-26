import asyncio
import requests
from bs4 import BeautifulSoup

async def get_free_proxies():
    url = "https://free-proxy-list.net/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    proxies = []
    for row in soup.find("table", class_="table table-striped table-bordered").tbody.find_all("tr"):
        cols = row.find_all("td")
        ip = cols[0].text
        port = cols[1].text
        https = cols[6].text
        if https == "yes":
            proxies.append(f"http://{ip}:{port}")
    return proxies

if __name__ == "__main__":
    asyncio.run(get_free_proxies())