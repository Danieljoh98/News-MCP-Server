from typing import Any
import httpx
import os
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

# Laster inn .env-filen
load_dotenv()

# Starter MCP-server
mcp = FastMCP("news")

# Henter nøkler fra miljøvariabler
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY")

# Define base URLs and headers
NEWS_API_BASE = "https://newsapi.org/v2"
CLAUDE_API_BASE = "https://api.anthropic.com/v1/chat/completions"
USER_AGENT = "news-app/1.0"


# 🔍 Hent artikler
async def fetch_news(query: str) -> list[dict[str, Any]]:
    url = f"{NEWS_API_BASE}/everything"
    headers = {
        "Authorization": NEWS_API_KEY,
        "User-Agent": USER_AGENT
    }
    params = {
        "q": query,
        "language": "en",
        "pageSize": 10
    }
    async with httpx.AsyncClient() as client:
        resp = await client.get(url, headers=headers, params=params, timeout=30.0)
        resp.raise_for_status()
        data = resp.json()
        return data.get("articles", [])

# 🧠 Send tekst til Claude
async def analyze_with_claude(text: str, prompt: str) -> str:
    headers = {
        "x-api-key": CLAUDE_API_KEY,
        "Content-Type": "application/json",
        "Anthropic-Version": "2023-06-01"
    }

    payload = {
        "model": "claude-3-haiku-20240307",
        "max_tokens_to_sample": 700,
        "messages": [{"role": "user", "content": f"{prompt}\n\n{text}"}]
    }

    async with httpx.AsyncClient() as client:
        resp = await client.post(CLAUDE_API_BASE, headers=headers, json=payload, timeout=40.0)
        try:
            resp.raise_for_status()
            data = resp.json()
            return data["choices"][0]["message"]["content"]
        except Exception:
            return "❌ Klarte ikke analysere med Claude."

# 🔎 MCP Tool 1: Vis nyhetsartikler med sammendrag og lenker
@mcp.tool()
async def get_news(topic: str) -> str:
    articles = await fetch_news(topic)
    if not articles:
        return f"Fant ingen artikler for temaet '{topic}'."

    results = []
    for article in articles:
        content = article.get("content") or article.get("description") or ""
        summary = await analyze_with_claude(content, "Lag et kort sammendrag av denne artikkelen.")

        title = article.get("title", "Uten tittel")
        url = article.get("url", "Ingen URL")
        results.append(f"### {title}\n[Les artikkelen]({url})\n\n**Sammendrag:** {summary}\n---")

    return "\n\n".join(results)

# ✅ MCP Tool 2: Lag fordeler og ulemper-liste
@mcp.tool()
async def generate_pros_cons(topic: str) -> str:
    articles = await fetch_news(topic)
    if not articles:
        return f"Fant ingen artikler om '{topic}'."

    combined_text = ""
    for article in articles:
        content = article.get("content") or article.get("description") or ""
        combined_text += f"{content}\n\n"

    prompt = (
        f"Basert på disse nyhetsartiklene om '{topic}', lag en liste med:\n"
        "- Fordeler (Pros)\n- Ulemper (Cons)\n"
        "Svar som en punktliste med klar og tydelig struktur."
    )

    result = await analyze_with_claude(combined_text, prompt)
    return f"# ✅ Fordeler og ulemper for '{topic}':\n\n{result}"

# 📅 MCP Tool 3: Lag en tidslinje basert på hendelser
@mcp.tool()
async def build_timeline(topic: str) -> str:
    articles = await fetch_news(topic)
    if not articles:
        return f"Fant ingen artikler om '{topic}'."

    combined_text = ""
    for article in articles:
        content = article.get("content") or article.get("description") or ""
        combined_text += f"{content}\n\n"

    prompt = (
        f"Basert på disse artiklene om '{topic}', lag en tidslinje med dato og hendelse der det er mulig. "
        f"Strukturen skal være:\n- [Dato]: [Hendelse]"
    )

    result = await analyze_with_claude(combined_text, prompt)
    return f"# 🕓 Tidslinje over hendelser relatert til '{topic}':\n\n{result}"

# 🏁 Start MCP-serveren
if __name__ == "__main__":
    mcp.run(transport="stdio")
