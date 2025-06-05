from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("news")

NEWS_API_KEY = "f2fd9770865f459082ca1ae2fd940572"
CLAUDE_API_KEY = "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"

NEWS_API_BASE = "https://newsapi.org/v2"
CLAUDE_API_BASE = "https://api.anthropic.com/v1/chat/completions"
USER_AGENT = "news-app/1.0"

async def fetch_news(query: str) -> list[dict[str, Any]]:
    url = f"{NEWS_API_BASE}/everything"
    headers = {
        "Authorization": NEWS_API_KEY,
        "User-Agent": USER_AGENT
    }
    params = {
        "q": query,
        "language": "en",
        "pageSize": 5
    }
    async with httpx.AsyncClient() as client:
        resp = await client.get(url, headers=headers, params=params, timeout=30.0)
        resp.raise_for_status()
        data = resp.json()
        return data.get("articles", [])

async def analyze_with_claude(text: str) -> str:
    if not text:
        return "Ingen innhold å analysere."

    headers = {
        "x-api-key": CLAUDE_API_KEY,
        "Content-Type": "application/json",
        "Anthropic-Version": "2023-06-01"
    }

    payload = {
        "model": "claude-3-haiku-20240307",
        "max_tokens_to_sample": 500,
        "messages": [
            {"role": "user", "content": f"Analyser denne nyhetsartikkelen og gi en oppsummering:\n\n{text}"}
        ]
    }

    async with httpx.AsyncClient() as client:
        resp = await client.post(CLAUDE_API_BASE, headers=headers, json=payload, timeout=30.0)
        try:
            resp.raise_for_status()
            data = resp.json()
            choices = data.get("choices")
            if choices and isinstance(choices, list):
                return choices[0].get("message", {}).get("content", "Claude ga ikke noe svar.")
            else:
                return f"Claude ga ikke forventet svar: {data}"
        except Exception:
            return "Klarte ikke analysere med Claude."

@mcp.tool()
async def get_news(topic: str) -> str:
    articles = await fetch_news(topic)
    if not articles:
        return f"Fant ingen artikler for temaet '{topic}'."

    results = []
    for article in articles:
        content = article.get("content") or article.get("description") or ""
        summary = await analyze_with_claude(content)

        title = article.get("title", "Uten tittel")
        url = article.get("url", "Ingen URL")
        results.append(f"Title: {title}\nSummary: {summary}\nURL: {url}\n---")

    return "\n\n".join(results)

if __name__ == "__main__":
    mcp.run(transport="stdio")
