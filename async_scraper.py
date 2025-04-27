import aiohttp
import asyncio
import pandas as pd
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import random
import time
import os

ua = UserAgent()

async def fetch(session, url):
    headers = {"User-Agent": ua.random}
    async with session.get(url, headers=headers) as response:
        return await response.text()

async def scrape_profile(session, name):
    query = f"site:linkedin.com/in/ {name.replace(' ', '%20')}"
    google_url = f"https://www.google.com/search?q={query}"
    try:
        html = await fetch(session, google_url)
        soup = BeautifulSoup(html, "html.parser")
        links = []
        for a in soup.find_all('a', href=True):
            href = a['href']
            if "linkedin.com/in/" in href and "webcache" not in href:
                clean_link = href.split("&")[0].replace("/url?q=", "")
                links.append(clean_link)
        link = links[0] if links else "Not Found"
        await asyncio.sleep(random.uniform(1, 3))  # Random sleep = stealth mode
        return {"Name": name, "LinkedIn Profile": link}
    except Exception as e:
        return {"Name": name, "LinkedIn Profile": f"Error: {str(e)}"}

async def scrape_all(names):
    results = []
    async with aiohttp.ClientSession() as session:
        tasks = [scrape_profile(session, name) for name in names]
        for f in asyncio.as_completed(tasks):
            result = await f
            results.append(result)
    return results

def scrape_linkedin_from_csv(file_path):
    df = pd.read_csv(file_path)
    names = df['Name'].tolist()
    results = asyncio.run(scrape_all(names))
    output_df = pd.DataFrame(results)
    timestamp = pd.Timestamp.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"linkedin_scrape_results_{timestamp}.csv"
    output_df.to_csv(output_file, index=False)
    return output_file
