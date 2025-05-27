# Solana Token Sniper

This project is an automated tool for monitoring new Solana token launches, scraping their social media activity, and using an LLM to analyze sentiment and engagement.

## Features

1. **Connects to PumpPortal**  
   Subscribes to real-time token creation events via the PumpPortal websocket API.

2. **Fetches Token Social Links**  
   Retrieves token metadata, including Twitter/social links, from the token’s metadata URI.

3. **Scrapes Token Socials**  
   Uses Playwright to scrape recent tweets or community posts from the token’s social accounts.

4. **LLM Analysis**  
   Feeds the scraped social data into a local LLM (Ollama) to determine sentiment and likelihood of success.

5. **Prints Verdict**  
   Outputs the LLM’s verdict (e.g., “pump” or “dump”) along with relevant tweet data.

## Usage

1. **Install dependencies**  
   ```powershell
   pip install -r requirements.txt
   ```

2. **Set up Playwright**  
   ```powershell
   playwright install
   ```

3. **Run the script**  
   ```powershell
   python main.py
   ```

## File Overview

- `main.py` — Main event loop: connects to PumpPortal, fetches token metadata, orchestrates scraping and LLM analysis.
- `get_links.py` — Extracts social links (e.g., Twitter) from token metadata.
- `get_html.py` — Scrapes recent tweets or community posts using Playwright.
- `llm.py` — Sends tweet data to an LLM (Ollama) and interprets the result.
- `sys_msgs.py` — Contains the system prompt for the LLM.

## Requirements

- Python 3.10+
- Playwright
- Ollama (for local LLM inference)
- aiohttp, websockets, html2text

## Notes

- The tool is designed for Solana memecoins and expects specific metadata fields.
- The LLM verdict is based on tweet content, engagement, and address matching.
- This was built using very fragile web scraping system (basically using random user agents and viewports to avoid detection) but getting blocked is to be expected. I'll review if adding proxies is feasible
