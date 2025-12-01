import requests
from bs4 import BeautifulSoup
from typing import List, Dict
from infra.logger import get_logger

logger = get_logger("google_search_tool")

def simple_duckduckgo_search(query: str, max_results: int = 3) -> List[Dict]:
    """
    Minimal web-scraper using DuckDuckGo HTML search.
    Returns top results with title, href, and snippet.
    """
    url = "https://html.duckduckgo.com/html/"
    params = {"q": query}

    try:
        resp = requests.post(url, data=params, timeout=10)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")

        results = []
        for a in soup.select(".result__a")[:max_results]:
            title = a.get_text()
            href = a.get("href")
            snippet_tag = a.find_parent().select_one(".result__snippet")
            snippet = snippet_tag.get_text() if snippet_tag else ""
            results.append({"title": title, "href": href, "snippet": snippet})

        logger.info(f"[GoogleSearchTool] Fetched {len(results)} results for query: '{query}'")
        return results

    except Exception as e:
        logger.error(f"[GoogleSearchTool] Search failed for query '{query}': {e}")
        return [{"title": "search_error", "href": "", "snippet": str(e)}]

def search(query: str, max_results: int = 3) -> List[Dict]:
    return simple_duckduckgo_search(query, max_results)