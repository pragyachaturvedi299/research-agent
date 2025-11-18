from utils import client, load_config

config = load_config()
model = config["llm"]["model"]
provider = config["search"]["provider"]

def run_search(query):
    if provider == "none":
        return "Search disabled."

    if provider == "openai":
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

    raise ValueError(f"Unknown search provider: {provider}")
