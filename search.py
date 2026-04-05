from utils import client, generator, load_config
from duckduckgo_search import DDGS

config = load_config()
model = config["llm"]["model"]
provider = config["search"]["provider"]

def run_search(query):
    if provider == "none":
        return "Search disabled."

    if client and provider == "openai":
        response = client.responses.create(
        model=model,
        input=f"""
        Use the web_search tool to find information about: "{query}".
        Return ONLY raw JSON search results. Do not summarize.
        """,
        tools=[{"type": "web_search"}],
              # Force tool to run
    )
        return response.output_text
    else:
        # Use DuckDuckGo search
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=5))
            # Format as simple text results
            formatted_results = "\n".join([f"Title: {r['title']}\nBody: {r['body']}\nURL: {r['href']}\n" for r in results])
            return formatted_results

    raise ValueError(f"Unknown search provider: {provider}")
