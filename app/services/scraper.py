from duckduckgo_search import DDGS

async def fetch_market_news(sector: str):
    try:
        with DDGS() as ddgs:
            query = f"current trade opportunities {sector} India 2025"
            results = ddgs.text(query, max_results=5)
            return "\n".join([f"Source: {r['title']}\nInfo: {r['body']}" for r in results])
    except Exception as e:
        return f"Scraper error: {str(e)}"